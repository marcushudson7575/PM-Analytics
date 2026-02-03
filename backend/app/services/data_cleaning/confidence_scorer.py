"""
Confidence Scoring Service
Calculates data confidence scores (0.0 to 1.0) based on source reliability and completeness.

Only data with confidence >= 1.0 will be displayed in the application.
"""
from decimal import Decimal
from typing import Dict, Optional


class ConfidenceScorer:
    """Calculate confidence scores for fund data"""

    # Source reliability scores (0.0 to 1.0)
    SOURCE_SCORES = {
        # Tier 1: Official regulatory filings (highest confidence)
        'sec_form_d': Decimal('0.95'),
        'sec_10k': Decimal('0.95'),
        'blackstone_10k': Decimal('0.95'),
        'kkr_10k': Decimal('0.95'),
        'apollo_10k': Decimal('0.95'),
        'ares_10k': Decimal('0.95'),
        'carlyle_10k': Decimal('0.95'),

        # Tier 2: Public pension fund disclosures
        'psers_holdings': Decimal('0.90'),
        'calpers_holdings': Decimal('0.90'),
        'washington_sib': Decimal('0.90'),
        'florida_sba': Decimal('0.90'),

        # Tier 3: Fund manager investor reports
        'manager_investor_report': Decimal('0.85'),

        # Tier 4: Manually verified data
        'manual_verified': Decimal('0.85'),

        # Tier 5: Unverified manual entry
        'manual_unverified': Decimal('0.60'),

        # Tier 6: Web scraping (lowest acceptable)
        'web_scrape': Decimal('0.50'),
    }

    # Required fields for 100% confidence
    REQUIRED_FIELDS = [
        'name',
        'strategy',
        'vintage_year',
    ]

    # High-value optional fields
    IMPORTANT_FIELDS = [
        'fund_size_usd',
        'manager',
        'geography',
    ]

    def calculate_score(self, fund_data: Dict, source: str) -> Decimal:
        """
        Calculate confidence score for fund data.

        Args:
            fund_data: Dictionary containing fund information
            source: Data source identifier

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Start with source reliability score (40% weight)
        base_score = self.SOURCE_SCORES.get(source, Decimal('0.50'))
        weighted_score = base_score * Decimal('0.40')

        # Required field completeness (35% weight)
        required_complete = sum(
            1 for field in self.REQUIRED_FIELDS
            if fund_data.get(field)
        ) / len(self.REQUIRED_FIELDS)
        weighted_score += Decimal(str(required_complete)) * Decimal('0.35')

        # Important field completeness (15% weight)
        important_complete = sum(
            1 for field in self.IMPORTANT_FIELDS
            if fund_data.get(field)
        ) / len(self.IMPORTANT_FIELDS)
        weighted_score += Decimal(str(important_complete)) * Decimal('0.15')

        # Validation passing (10% weight)
        if self._passes_validation(fund_data):
            weighted_score += Decimal('0.10')

        return min(weighted_score, Decimal('1.0'))

    def _passes_validation(self, fund_data: Dict) -> bool:
        """
        Check if fund data passes basic validation.

        Args:
            fund_data: Fund data dictionary

        Returns:
            True if data passes validation
        """
        # Check vintage year is reasonable (1990-2030)
        vintage_year = fund_data.get('vintage_year')
        if vintage_year:
            if not (1990 <= vintage_year <= 2030):
                return False

        # Check fund size is reasonable (> $0)
        fund_size = fund_data.get('fund_size_usd')
        if fund_size:
            if fund_size <= 0:
                return False

        # Check management fee is reasonable (0-5%)
        mgmt_fee = fund_data.get('management_fee_pct')
        if mgmt_fee:
            if not (0 <= mgmt_fee <= 5):
                return False

        # Check carry is reasonable (0-50%)
        carry = fund_data.get('carry_pct')
        if carry:
            if not (0 <= carry <= 50):
                return False

        return True

    def requires_manual_review(self, score: Decimal) -> bool:
        """
        Determine if fund data requires manual review before display.

        Args:
            score: Calculated confidence score

        Returns:
            True if manual review is needed
        """
        # Anything below 100% confidence requires review
        return score < Decimal('1.0')


def score_fund_confidence(fund_data: Dict, source: str) -> Decimal:
    """
    Main function to calculate fund data confidence score.

    Args:
        fund_data: Dictionary containing fund information
        source: Data source identifier

    Returns:
        Confidence score between 0.0 and 1.0
    """
    scorer = ConfidenceScorer()
    return scorer.calculate_score(fund_data, source)
