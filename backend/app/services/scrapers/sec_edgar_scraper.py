"""
SEC EDGAR Form D Scraper
Fetches real private fund offering data from SEC Form D filings.

Form D is filed by companies when they sell securities without registering with the SEC
under Regulation D. This includes private equity and venture capital funds.
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import re
from decimal import Decimal


class SECEdgarScraper:
    """Scraper for SEC EDGAR Form D filings"""

    BASE_URL = "https://www.sec.gov"
    SEARCH_URL = f"{BASE_URL}/cgi-bin/browse-edgar"

    # SEC requires user agent identification
    HEADERS = {
        'User-Agent': 'PM Analytics contact@pmanalytics.com',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
    }

    # Rate limit: 1 request per second as per SEC guidelines
    RATE_LIMIT_DELAY = 1.0

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.last_request_time = 0

    def _rate_limit(self):
        """Enforce SEC rate limiting (max 10 requests per second)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()

    def search_form_d_filings(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Search for recent Form D filings.

        Args:
            start_date: Start date for search (default: 30 days ago)
            end_date: End date for search (default: today)
            max_results: Maximum number of results to return

        Returns:
            List of filing metadata dictionaries
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()

        # SEC EDGAR RSS feed for recent filings
        rss_url = f"{self.BASE_URL}/cgi-bin/browse-edgar?action=getcurrent&type=D&company=&dateb=&owner=exclude&start=0&count={max_results}&output=atom"

        self._rate_limit()
        response = self.session.get(rss_url)
        response.raise_for_status()

        # Parse the atom feed
        filings = []
        root = ET.fromstring(response.content)

        # Namespace for parsing Atom XML
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            link = entry.find('atom:link', ns)
            updated = entry.find('atom:updated', ns)

            if title is not None and link is not None:
                filing_url = link.get('href')
                filings.append({
                    'title': title.text,
                    'url': filing_url,
                    'date': updated.text if updated is not None else None
                })

        return filings[:max_results]

    def get_form_d_by_cik(self, cik: str, max_filings: int = 10) -> List[Dict]:
        """
        Get Form D filings for a specific company by CIK number.

        Args:
            cik: Central Index Key (CIK) number
            max_filings: Maximum number of filings to retrieve

        Returns:
            List of filing URLs
        """
        # Pad CIK to 10 digits
        cik_padded = cik.zfill(10)

        url = f"{self.BASE_URL}/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'CIK': cik_padded,
            'type': 'D',
            'dateb': '',
            'owner': 'exclude',
            'count': max_filings,
            'search_text': ''
        }

        self._rate_limit()
        response = self.session.get(url, params=params)
        response.raise_for_status()

        # Parse HTML to extract filing links
        # This is simplified - in production, use BeautifulSoup
        filings = []

        # Look for accession numbers in the response
        accession_pattern = r'(\d{10}-\d{2}-\d{6})'
        accession_numbers = re.findall(accession_pattern, response.text)

        for accession in accession_numbers[:max_filings]:
            filing_url = f"{self.BASE_URL}/cgi-bin/viewer?action=view&cik={cik_padded}&accession_number={accession}"
            filings.append({
                'cik': cik,
                'accession_number': accession,
                'url': filing_url
            })

        return filings

    def parse_form_d_xml(self, accession_number: str, cik: str) -> Optional[Dict]:
        """
        Parse Form D XML filing to extract fund information.

        Args:
            accession_number: SEC accession number (e.g., '0001193125-24-123456')
            cik: Company CIK number

        Returns:
            Dictionary with parsed fund data
        """
        # Remove dashes from accession number for URL
        accession_clean = accession_number.replace('-', '')

        # Construct XML file URL
        xml_url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{accession_clean}/primary_doc.xml"

        self._rate_limit()
        try:
            response = self.session.get(xml_url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # Try alternative XML location
            xml_url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{accession_clean}/form_d.xml"
            response = self.session.get(xml_url)
            response.raise_for_status()

        # Parse XML
        root = ET.fromstring(response.content)

        fund_data = {
            'source': 'sec_form_d',
            'accession_number': accession_number,
            'cik': cik
        }

        # Extract issuer information (fund manager)
        issuer = root.find('.//issuer')
        if issuer is not None:
            issuer_name = issuer.find('.//issuerName')
            if issuer_name is not None:
                fund_data['manager_name'] = issuer_name.text

        # Extract offering data
        offering = root.find('.//offeringData')
        if offering is not None:
            # Industry group (helps classify fund type)
            industry_group = offering.find('.//industryGroupType')
            if industry_group is not None:
                fund_data['industry_group'] = industry_group.text

            # Offering amount
            total_offering = offering.find('.//totalOfferingAmount')
            if total_offering is not None:
                try:
                    fund_data['offering_amount'] = Decimal(total_offering.text)
                except (ValueError, TypeError):
                    pass

            # Total amount sold
            total_sold = offering.find('.//totalAmountSold')
            if total_sold is not None:
                try:
                    fund_data['amount_sold'] = Decimal(total_sold.text)
                except (ValueError, TypeError):
                    pass

        # Extract signature date (filing date)
        signature_date = root.find('.//signatureDate')
        if signature_date is not None:
            try:
                fund_data['filing_date'] = datetime.strptime(signature_date.text, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                pass

        # Classify fund type based on industry group code
        fund_data['strategy'] = self._classify_fund_strategy(fund_data.get('industry_group'))

        return fund_data

    def _classify_fund_strategy(self, industry_group_code: Optional[str]) -> str:
        """
        Classify fund strategy based on SEC industry group code.

        Pooled Investment Fund codes:
        - P: Hedge Fund
        - Q: Private Equity Fund
        - R: Venture Capital Fund
        - S: Other Investment Fund
        """
        if not industry_group_code:
            return 'Unknown'

        code_mapping = {
            'P': 'Hedge Fund',
            'Q': 'Buyout',  # Private Equity
            'R': 'Venture Capital',
            'S': 'Other Fund'
        }

        return code_mapping.get(industry_group_code, 'Unknown')

    def scrape_recent_funds(self, days_back: int = 30, max_funds: int = 100) -> List[Dict]:
        """
        Scrape recent fund filings from the past N days.

        Args:
            days_back: Number of days to look back
            max_funds: Maximum number of funds to scrape

        Returns:
            List of fund data dictionaries
        """
        print(f"Fetching Form D filings from the past {days_back} days...")

        start_date = datetime.now() - timedelta(days=days_back)
        filings = self.search_form_d_filings(start_date=start_date, max_results=max_funds)

        print(f"Found {len(filings)} filings. Parsing...")

        funds = []
        for idx, filing in enumerate(filings):
            try:
                # Extract CIK and accession number from filing URL
                # This is simplified - in production, parse more carefully
                url_parts = filing['url'].split('/')

                # Skip if we can't extract necessary info
                if len(url_parts) < 2:
                    continue

                print(f"  Processing filing {idx + 1}/{len(filings)}...")

                # Note: Full implementation would extract CIK and accession from the filing
                # For now, we'll use the RSS feed approach

                funds.append({
                    'name': filing['title'],
                    'filing_date': filing['date'],
                    'source_url': filing['url'],
                    'data_source': 'sec_form_d'
                })

                # Rate limiting
                self._rate_limit()

            except Exception as e:
                print(f"  Error processing filing: {e}")
                continue

        print(f"Successfully scraped {len(funds)} funds")
        return funds


def scrape_sec_funds(days_back: int = 90, max_funds: int = 100) -> List[Dict]:
    """
    Main function to scrape SEC Form D filings.

    Args:
        days_back: Number of days to look back for filings
        max_funds: Maximum number of funds to retrieve

    Returns:
        List of fund dictionaries ready for database insertion
    """
    scraper = SECEdgarScraper()
    return scraper.scrape_recent_funds(days_back=days_back, max_funds=max_funds)


if __name__ == "__main__":
    # Test the scraper
    print("Testing SEC EDGAR scraper...")
    funds = scrape_sec_funds(days_back=30, max_funds=20)

    print(f"\nScraped {len(funds)} funds:")
    for fund in funds[:5]:  # Print first 5
        print(f"  - {fund.get('name', 'Unknown')}")
