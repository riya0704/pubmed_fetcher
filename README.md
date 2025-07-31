# PubMed Fetcher 🧬📄

A Python tool to fetch PubMed articles and identify those with industry affiliations, saving results to CSV or displaying in console.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features ✨

- Search PubMed with advanced query syntax
- Identify papers with industry-affiliated authors
- Filter by pharmaceutical/biotech company affiliations
- Export results to CSV or view in console
- Configurable rate limiting and retry logic
- Detailed debug mode for troubleshooting

## Code Organization 🗂️
pubmed_fetcher/
├── init.py
├── version.py
├── utils.py
│ ├── API request handling
│ ├── XML parsing
│ ├── Affiliation analysis
├── core.py
│ ├── PubMed API interactions
│ ├── Paper processing logic
└── cli.py
│ ├── Argument parsing
│ ├── Output formatting


## Installation 🛠️

### Prerequisites
- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Method 1: Using Poetry (Recommended)

# Clone the repository
git clone https://github.com/yourusername/pubmed-fetcher.git
cd pubmed-fetcher

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
Method 2: Using pip


# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install requests typer lxml python-dotenv
Usage 🚀

# Basic Command

poetry run python -m pubmed_fetcher.cli "your search query" [options]
Options
Flag	Description	Default
-f, --file FILENAME	Save results to CSV file	None
-m, --max INTEGER	Maximum papers to process	100
-d, --debug	Show debug information	False
Examples
Basic search:
poetry run python -m pubmed_fetcher.cli "CRISPR therapy"
Save to CSV:

poetry run python -m pubmed_fetcher.cli "cancer immunotherapy" --file results.csv
Advanced search:

poetry run python -m pubmed_fetcher.cli "(mRNA[Title]) AND (vaccine[Title])" --max 200 --debug

# Configuration ⚙️
For enhanced API access, add an NCBI API key:

Create an NCBI account: Register here

Get your API key: Account Settings

Create a .env file:


echo "NCBI_API_KEY=your_api_key_here" >> .env


# Output Format 📊
CSV/console output includes:

PubmedID: Unique PubMed identifier

Title: Article title

Publication Date: YYYY-MM-DD format

Non-academic Author(s): Industry-affiliated authors

Company Affiliation(s): Pharmaceutical/biotech companies

Corresponding Author Email: Contact email (when available)

# Sample output:

PubmedID: 40739792
Title: Novel CRISPR-based therapy shows promise in clinical trials
Publication Date: 2023-07-15
Non-academic Author(s): John Smith; Jane Doe
Company Affiliation(s): GeneEdit Therapeutics, Inc.; BioCRISPR Labs
Corresponding Author Email: j.smith@genedit.com


# Dependencies 📦
Package	Purpose	Version
Requests	HTTP requests	≥2.25.0
Typer	CLI interface	≥0.4.0
lxml	XML parsing	≥4.6.0
python-dotenv	Environment variables	≥0.19.0


# Development 🛠️
Running Tests
poetry run pytest
Building the Package
poetry build
Publishing to PyPI
poetry publish


## Troubleshooting 🐛


# Common Issues:

API Limit Errors: Add your NCBI API key to .env

XML Parsing Errors: Update lxml with pip install --upgrade lxml

No Results Found: Try a broader search query

# Contributing 🤝
Contributions are welcome! Please:

Fork the repository

Create a feature branch

Submit a pull request

# License 📄
This project is licensed under the MIT License - see the LICENSE file for details.