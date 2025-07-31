import typer
import csv
from typing import Optional
from pathlib import Path
from pubmed_fetcher.core import fetch_pubmed_ids, fetch_paper_details

def main(
    query: str,
    file: Optional[str] = None,
    max_papers: int = 100,
    debug: bool = False
):
    """Main function that handles the actual logic"""
    try:
        print(f"🔍 Searching PubMed for: '{query}'")
        
        pmids = fetch_pubmed_ids(query, retmax=max_papers, debug=debug)
        
        if not pmids:
            print("❌ No papers found matching your query.")
            return
        
        results = []
        for pmid in pmids:
            paper = fetch_paper_details(pmid, debug=debug)
            if paper:
                results.append(paper)
        
        if not results:
            print("⚠️ No papers with industry affiliations found.")
            return
        
        headers = [
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email"
        ]
        
        if file:
            with open(file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)
            print(f"✅ Saved {len(results)} papers to {file}")
        else:
            for paper in results:
                print("\n" + "=" * 60)
                for field in headers:
                    print(f"{field}: {paper[field]}")
            print(f"\n✅ Found {len(results)} relevant papers")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def run():
    """Typer wrapper function"""
    typer.run(main)

if __name__ == "__main__":
    run()