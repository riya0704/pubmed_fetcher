"""
pubmed_fetcher.utils - Utility functions for the PubMed fetcher package
"""

import time
from typing import Optional, Dict, List
import requests
from xml.etree import ElementTree as ET

def make_api_request(url: str, params: Dict, max_retries: int = 3, delay: float = 1.0, debug: bool = False) -> Optional[requests.Response]:
    """Make an API request with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if debug:
                print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
                continue
            if debug:
                print(f"❌ Max retries reached for URL: {url}")
            return None

from typing import Union

def parse_affiliation(affiliation_text: str) -> Dict[str, Union[bool, str]]:
    """Parse an affiliation string to determine if it's academic or industry"""
    aff_text = affiliation_text.lower()
    
    academic_keywords = [
        "university", "college", "institute", "hospital", 
        "school", "academy", "center", "centre", "clinic",
        "medical center", "universität", "université", 
        "universidad", "nih.gov", "inserm", "cnrs", "max planck",
        ".edu", ".ac.", "gov.", "org.", "association", "foundation"
    ]
    
    industry_keywords = [
        "pharma", "biotech", "inc", "ltd", "corp", "llc",
        "therapeutics", "genetics", "vaccin", "bioscience",
        "laboratories", "healthcare", "pharmaceut", "biolog",
        "oncology", "company", "holdings", "ventures", "gmbh"
    ]
    
    is_academic = any(keyword in aff_text for keyword in academic_keywords)
    is_industry = any(keyword in aff_text for keyword in industry_keywords) and not is_academic
    
    return {
        "is_academic": is_academic,
        "is_industry": is_industry,
        "original_text": affiliation_text
    }

def safe_xml_find(element, path: str, default=None):
    """Safely find an XML element with null checks"""
    result = element.find(path)
    return result if result is not None else default

def safe_xml_text(element, default: str = "N/A") -> str:
    """Safely get text from an XML element with null checks"""
    if element is not None and element.text is not None:
        return element.text.strip()
    return default