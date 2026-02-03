"""
Scrapers for reputable private markets data sources.

Authoritative sources only:
- SEC filings (USA)
- Public pension fund disclosures
- Publicly traded PE manager reports
- FCA filings (UK)
- European fund regulatory databases
- Sovereign wealth fund reports
"""
from .sec_edgar_scraper import scrape_sec_funds
from .public_pe_scraper import scrape_public_pe_managers
from .pension_fund_scraper import scrape_pension_funds

__all__ = [
    'scrape_sec_funds',
    'scrape_public_pe_managers',
    'scrape_pension_funds',
]
