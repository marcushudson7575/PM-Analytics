#!/usr/bin/env python3
"""
Real Data Ingestion Script
Scrapes real fund data from authoritative sources and populates the database.

Asset Classes Covered:
1. Large PE ($5B+)
2. Small to mid PE ($500M-$5B)
3. Growth Capital
4. Venture Capital
5. Private Debt/Credit
6. Real Estate
7. Infrastructure
8. Hedge Funds

Sources:
- Publicly traded PE managers (Blackstone, KKR, Apollo, Ares, Carlyle)
- Public pension fund disclosures (PSERS, CalPERS, Washington SIB, Florida SBA)
- Official regulatory filings

Only data with confidence score >= 0.90 is inserted into the database.
"""
import sys
import os
from datetime import datetime
from decimal import Decimal
import uuid

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import SessionLocal
from app.models.fund import Fund
from app.services.scrapers.comprehensive_fund_scraper import scrape_comprehensive_funds
from app.services.data_cleaning import normalize_fund, score_fund_confidence


def convert_to_fund_model(fund_data: dict, db: Session) -> Fund:
    """
    Convert scraped fund data to Fund model.

    Args:
        fund_data: Normalized fund data dictionary
        db: Database session

    Returns:
        Fund model instance
    """
    # Generate identifier from name and vintage year
    name_clean = fund_data.get('name', 'Unknown').replace(' ', '_').upper()
    vintage = fund_data.get('vintage_year', 2020)
    identifier = f"{name_clean}_{vintage}"

    # Check if fund already exists
    existing = db.query(Fund).filter(Fund.identifier == identifier).first()
    if existing:
        print(f"  Fund already exists: {fund_data.get('name')}")
        return None

    # Create new fund
    fund = Fund(
        id=uuid.uuid4(),
        name=fund_data.get('name'),
        identifier=identifier,
        vintage_year=fund_data.get('vintage_year'),
        strategy=fund_data.get('strategy'),
        geography=fund_data.get('geography'),
        sector_focus=fund_data.get('sector_focus'),
        fund_size_usd=fund_data.get('fund_size_usd'),
        management_fee_pct=fund_data.get('management_fee_pct'),
        carry_pct=fund_data.get('carry_pct'),
        data_confidence_score=fund_data.get('data_confidence_score', Decimal('0.0')),
        data_source=fund_data.get('data_source', 'unknown')
    )

    return fund


def ingest_comprehensive_funds(db: Session) -> int:
    """
    Ingest fund data across all asset classes from authoritative sources.

    Returns:
        Number of funds inserted
    """
    print("\n" + "="*60)
    print("INGESTING COMPREHENSIVE FUND DATA")
    print("="*60)
    print("Asset classes: Large PE, Mid PE, Growth, VC, Private Debt, RE, Infra, Hedge")
    print("="*60)

    funds_data = scrape_comprehensive_funds()
    inserted_count = 0
    skipped_count = 0

    # Track by strategy
    strategy_counts = {}

    for fund_data in funds_data:
        # Normalize the data
        normalized = normalize_fund(fund_data)

        # Calculate confidence score
        source = normalized.get('data_source', 'unknown')
        confidence = score_fund_confidence(normalized, source)
        normalized['data_confidence_score'] = confidence

        # Only insert if confidence >= 90% (from authoritative sources)
        if confidence >= Decimal('0.90'):
            fund_model = convert_to_fund_model(normalized, db)

            if fund_model:
                db.add(fund_model)
                inserted_count += 1

                # Track by strategy
                strategy = normalized.get('strategy', 'Unknown')
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

                print(f"  ✓ {normalized['strategy']}: {normalized['name']} (confidence: {confidence})")
        else:
            skipped_count += 1
            print(f"  ✗ Skipped: {normalized.get('name')} (low confidence: {confidence})")

    db.commit()

    print(f"\n" + "="*60)
    print(f"Inserted {inserted_count} funds, skipped {skipped_count}")
    print(f"\nBreakdown by strategy:")
    for strategy, count in sorted(strategy_counts.items()):
        print(f"  {strategy}: {count} funds")
    print("="*60)

    return inserted_count


def main():
    """Main ingestion function"""
    print("\n" + "="*60)
    print("COMPREHENSIVE PRIVATE MARKETS DATA INGESTION")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nAsset Classes:")
    print("  1. Large PE ($5B+)")
    print("  2. Small to mid PE ($500M-$5B)")
    print("  3. Growth Capital")
    print("  4. Venture Capital")
    print("  5. Private Debt/Credit")
    print("  6. Real Estate")
    print("  7. Infrastructure")
    print("  8. Hedge Funds")
    print("\nSources:")
    print("  - Publicly traded managers (Blackstone, KKR, Apollo, Ares, Carlyle, etc.)")
    print("  - Public pension fund disclosures (PSERS, CalPERS, Washington SIB, Florida SBA)")
    print("  - Official regulatory filings")
    print("\n" + "="*60)

    # Create database session
    db = SessionLocal()

    try:
        # Ingest comprehensive fund data
        total_inserted = ingest_comprehensive_funds(db)

        # Summary
        print("\n" + "="*60)
        print("INGESTION COMPLETE")
        print("="*60)
        print(f"Total funds inserted: {total_inserted}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Count total funds in database
        total_funds = db.query(Fund).count()
        high_confidence_funds = db.query(Fund).filter(
            Fund.data_confidence_score >= 0.95
        ).count()

        # Count by strategy
        print(f"\nDatabase summary:")
        print(f"  Total funds: {total_funds}")
        print(f"  High confidence (≥95%): {high_confidence_funds}")

        # Strategy breakdown
        print(f"\nFunds by asset class:")
        strategies = db.query(Fund.strategy, func.count(Fund.id)).group_by(Fund.strategy).all()
        for strategy, count in strategies:
            print(f"  {strategy}: {count}")

        print("="*60)

    except Exception as e:
        print(f"\nError during ingestion: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
