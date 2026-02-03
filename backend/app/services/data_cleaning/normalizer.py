"""
Data Normalization Service
Standardizes and cleans fund data from various sources.
"""
from typing import Dict, Optional
from decimal import Decimal
import re


class DataNormalizer:
    """Normalize and standardize fund data"""

    # Strategy standardization
    STRATEGY_MAPPING = {
        'private equity': 'Buyout',
        'pe': 'Buyout',
        'buyout': 'Buyout',
        'lbo': 'Buyout',
        'venture capital': 'Venture Capital',
        'vc': 'Venture Capital',
        'venture': 'Venture Capital',
        'growth equity': 'Growth Equity',
        'growth': 'Growth Equity',
        'infrastructure': 'Infrastructure',
        'infra': 'Infrastructure',
        'real estate': 'Real Estate',
        'real assets': 'Real Assets',
        'private credit': 'Private Credit',
        'credit': 'Private Credit',
        'distressed': 'Distressed/Special Situations',
        'special situations': 'Distressed/Special Situations',
        'secondary': 'Secondary',
        'secondaries': 'Secondary',
        'co-investment': 'Co-Investment',
        'hedge fund': 'Hedge Fund',
    }

    # Geography standardization
    GEOGRAPHY_MAPPING = {
        'usa': 'North America',
        'us': 'North America',
        'united states': 'North America',
        'north america': 'North America',
        'na': 'North America',
        'europe': 'Europe',
        'eu': 'Europe',
        'emea': 'Europe',
        'uk': 'Europe',
        'united kingdom': 'Europe',
        'asia': 'Asia-Pacific',
        'asia-pacific': 'Asia-Pacific',
        'apac': 'Asia-Pacific',
        'china': 'Asia-Pacific',
        'japan': 'Asia-Pacific',
        'india': 'Asia-Pacific',
        'global': 'Global',
        'worldwide': 'Global',
        'latin america': 'Latin America',
        'latam': 'Latin America',
        'emerging markets': 'Emerging Markets',
        'em': 'Emerging Markets',
        'middle east': 'Middle East',
    }

    def normalize_fund_name(self, name: str) -> str:
        """
        Normalize fund name.

        Args:
            name: Raw fund name

        Returns:
            Cleaned fund name
        """
        if not name:
            return ""

        # Remove extra whitespace
        name = ' '.join(name.split())

        # Remove common suffixes that aren't meaningful
        name = re.sub(r',\s*(L\.P\.|LP|Ltd\.|Limited|LLC)$', '', name, flags=re.IGNORECASE)

        # Capitalize properly
        # Keep Roman numerals uppercase (I, II, III, IV, V, etc.)
        words = name.split()
        normalized_words = []

        for word in words:
            # Check if it's a Roman numeral
            if re.match(r'^[IVX]+$', word, re.IGNORECASE):
                normalized_words.append(word.upper())
            else:
                normalized_words.append(word)

        return ' '.join(normalized_words)

    def normalize_strategy(self, strategy: Optional[str]) -> Optional[str]:
        """
        Normalize fund strategy to standard categories.

        Args:
            strategy: Raw strategy string

        Returns:
            Standardized strategy or None
        """
        if not strategy:
            return None

        strategy_lower = strategy.lower().strip()

        # Check for exact or partial matches
        for key, value in self.STRATEGY_MAPPING.items():
            if key in strategy_lower:
                return value

        # If no match found, return original (capitalized)
        return strategy.title()

    def normalize_geography(self, geography: Optional[str]) -> Optional[str]:
        """
        Normalize geography to standard regions.

        Args:
            geography: Raw geography string

        Returns:
            Standardized geography or None
        """
        if not geography:
            return None

        geography_lower = geography.lower().strip()

        # Check for exact match first
        if geography_lower in self.GEOGRAPHY_MAPPING:
            return self.GEOGRAPHY_MAPPING[geography_lower]

        # Check for partial matches
        for key, value in self.GEOGRAPHY_MAPPING.items():
            if key in geography_lower:
                return value

        # If no match found, return original (title case)
        return geography.title()

    def normalize_fund_size(self, size: any) -> Optional[Decimal]:
        """
        Normalize fund size to USD decimal.

        Args:
            size: Fund size (can be string, float, int, or Decimal)

        Returns:
            Normalized size as Decimal or None
        """
        if size is None:
            return None

        # If already a Decimal, return it
        if isinstance(size, Decimal):
            return size

        # Convert to string first
        size_str = str(size).strip()

        # Remove currency symbols and commas
        size_str = size_str.replace('$', '').replace(',', '').replace('€', '').replace('£', '')

        # Handle magnitude suffixes (B, M, K)
        multiplier = Decimal('1')

        if 'B' in size_str.upper() or 'BN' in size_str.upper():
            multiplier = Decimal('1000000000')
            size_str = re.sub(r'[Bb][Nn]?', '', size_str)
        elif 'M' in size_str.upper() or 'MM' in size_str.upper():
            multiplier = Decimal('1000000')
            size_str = re.sub(r'[Mm]{1,2}', '', size_str)
        elif 'K' in size_str.upper():
            multiplier = Decimal('1000')
            size_str = re.sub(r'[Kk]', '', size_str)

        try:
            value = Decimal(size_str.strip()) * multiplier
            return value if value > 0 else None
        except:
            return None

    def normalize_vintage_year(self, year: any) -> Optional[int]:
        """
        Normalize vintage year to integer.

        Args:
            year: Vintage year (can be string or int)

        Returns:
            Year as integer or None
        """
        if year is None:
            return None

        try:
            year_int = int(year)
            # Sanity check: reasonable range
            if 1990 <= year_int <= 2030:
                return year_int
        except (ValueError, TypeError):
            pass

        return None

    def normalize_fund_data(self, fund_data: Dict) -> Dict:
        """
        Normalize all fields in fund data dictionary.

        Args:
            fund_data: Raw fund data

        Returns:
            Normalized fund data
        """
        normalized = fund_data.copy()

        # Normalize name
        if 'name' in normalized:
            normalized['name'] = self.normalize_fund_name(normalized['name'])

        # Normalize strategy
        if 'strategy' in normalized:
            normalized['strategy'] = self.normalize_strategy(normalized['strategy'])

        # Normalize geography
        if 'geography' in normalized:
            normalized['geography'] = self.normalize_geography(normalized['geography'])

        # Normalize fund size
        if 'fund_size_usd' in normalized:
            normalized['fund_size_usd'] = self.normalize_fund_size(normalized['fund_size_usd'])

        # Normalize commitment (for pension fund data)
        if 'commitment_usd' in normalized and 'fund_size_usd' not in normalized:
            # Use commitment as a proxy for fund size estimation
            # Typically LP commitments are 1-5% of total fund size
            # We'll mark confidence lower for this
            pass

        # Normalize vintage year
        if 'vintage_year' in normalized:
            normalized['vintage_year'] = self.normalize_vintage_year(normalized['vintage_year'])

        return normalized


def normalize_fund(fund_data: Dict) -> Dict:
    """
    Main function to normalize fund data.

    Args:
        fund_data: Raw fund data dictionary

    Returns:
        Normalized fund data
    """
    normalizer = DataNormalizer()
    return normalizer.normalize_fund_data(fund_data)
