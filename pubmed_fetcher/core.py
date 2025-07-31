import os
import time
from typing import List, Dict, Optional
import requests
from xml.etree import ElementTree as ET
from datetime import datetime
from .utils import make_api_request, parse_affiliation, safe_xml_find, safe_xml_text
# Load API key from environment variable
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

def fetch_pubmed_ids(
    query: str,
    retmax: int = 100,
    debug: bool = False,
    delay: float = 0.34
) -> List[str]:
    """Fetch PubMed IDs for a given query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    try:
        if debug:
            print(f"🔍 Search URL: {base_url}?{'&'.join(f'{k}={v}' for k,v in params.items())}")
        
        time.sleep(delay)
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return data.get("esearchresult", {}).get("idlist", [])
    
    except Exception as e:
        if debug:
            print(f"❌ Error fetching PubMed IDs: {str(e)}")
        return []

def fetch_paper_details(
    pmid: str,
    debug: bool = False,
    max_retries: int = 3,
    initial_delay: float = 1.0
) -> Optional[Dict[str, str]]:
    """Fetch detailed information for a single paper with retries."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    for attempt in range(max_retries):
        delay = initial_delay * (attempt + 1)  # Exponential backoff
        
        try:
            if debug:
                print(f"📄 Fetching PMID {pmid} (attempt {attempt + 1})")
            
            time.sleep(delay if attempt > 0 else 0)
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            
            try:
                root = ET.fromstring(response.text)
            except ET.ParseError as e:
                if debug:
                    print(f"❌ Failed to parse XML for PMID {pmid}: {str(e)}")
                continue

            article = root.find(".//PubmedArticle")
            if article is None:
                if debug:
                    print(f"⚠️ No article found for PMID {pmid}")
                continue

            # Extract title with null checks
            title = "N/A"
            title_elem = article.find(".//ArticleTitle")
            if title_elem is not None and title_elem.text is not None:
                title = title_elem.text.strip()

            # Extract publication date with null checks
            date_str = "N/A"
            pub_date = article.find(".//PubDate")
            if pub_date is not None:
                year_elem = pub_date.find("Year")
                year = year_elem.text if year_elem is not None and year_elem.text is not None else "?"
                month_elem = pub_date.find("Month")
                month = month_elem.text if month_elem is not None and month_elem.text is not None else "?"
                day_elem = pub_date.find("Day")
                day = day_elem.text if day_elem is not None and day_elem.text is not None else "?"
                date_str = f"{year}-{month}-{day}"

            # Extract authors and affiliations
            non_academic_authors = []
            company_affiliations = set()
            corresponding_email = "N/A"
            authors = article.findall(".//Author") or []

            for author in authors:
                # Safely get author name
                last_name_elem = author.find("LastName")
                fore_name_elem = author.find("ForeName")
                
                last_name = last_name_elem.text if last_name_elem is not None else None
                fore_name = fore_name_elem.text if fore_name_elem is not None else None
                author_name = f"{fore_name} {last_name}".strip() if fore_name and last_name else None

                # Check affiliations
                affiliations = author.findall(".//Affiliation") or []
                for aff in affiliations:
                    if aff is not None and aff.text is not None:
                        aff_text = aff.text.lower()
                        
                        # Enhanced academic detection
                        is_academic = (
                            any(term in aff_text for term in [
                                "university", "college", "institute", 
                                "hospital", "school", "academy", 
                                "center", "centre", "clinic", "medical center",
                                "universität", "université", "universidad",
                                "research center", "nih.gov", "inserm", "cnrs"
                            ]) or
                            any(term in aff_text for term in [".edu", ".ac.", "gov."])
                        )
                        
                        # Enhanced company detection
                        is_company = (
                            any(term in aff_text for term in [
                                "pharma", "biotech", "inc", "ltd", "corp", "llc",
                                "therapeutics", "genetics", "vaccin", "bioscience",
                                "laboratories", "healthcare", "pharmaceut", "biolog",
                                "oncology", "company", "holdings", "ventures", "gmbh"
                            ]) and 
                            not is_academic
                        )

                        if is_company and author_name:
                            company_affiliations.add(aff.text)
                            non_academic_authors.append(author_name)

                # Check for corresponding author email
                if author.get("ValidYN", "") == "Y":
                    email_elem = author.find(".//Email")
                    if email_elem is not None and email_elem.text is not None:
                        corresponding_email = email_elem.text.strip()

            if not company_affiliations:
                if debug:
                    print(f"⚠️ No verified company affiliations found for PMID {pmid}")
                return None

            return {
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": date_str,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500 and attempt < max_retries - 1:
                if debug:
                    print(f"⚠️ Server error, retrying in {delay:.1f}s...")
                continue
            if debug:
                print(f"❌ HTTP Error for PMID {pmid}: {str(e)}")
            return None

        except Exception as e:
            if debug:
                print(f"❌ Unexpected error for PMID {pmid}: {str(e)}")
            return None

    return None