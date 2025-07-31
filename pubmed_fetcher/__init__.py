"""
pubmed_fetcher - A package for fetching PubMed articles with industry affiliations
"""

from .version import __version__
from .core import fetch_pubmed_ids, fetch_paper_details
# from .cli import get_papers_list

__all__ = [
    'fetch_pubmed_ids',
    'fetch_paper_details',
    # 'get_papers_list',
    '__version__'
]