#!/usr/bin/env python3
"""
Seed script to generate 100+ sample private equity funds with realistic data.
This populates the database for testing and demonstration purposes.
"""
import sys
import os
import random
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.fund import Fund, Investment, FundPerformance

# Sample data for realistic fund generation
STRATEGIES = [
    'Buyout',
    'Growth Equity',
    'Venture Capital',
    'Infrastructure',
    'Real Estate',
    'Distressed/Special Situations',
    'Secondary',
    'Co-Investment'
]

GEOGRAPHIES = [
    'North America',
    'Europe',
    'Asia-Pacific',
    'Global',
    'Emerging Markets',
    'Latin America',
    'Middle East'
]

SECTORS = [
    'Technology',
    'Healthcare',
    'Consumer',
    'Industrials',
    'Financial Services',
    'Energy',
    'Real Estate',
    'TMT',
    'Multi-Sector'
]

FIRM_NAMES = [
    'Blackstone', 'KKR', 'Apollo', 'Carlyle', 'TPG', 'Warburg Pincus',
    'CVC Capital', 'Advent International', 'Bain Capital', 'EQT',
    'Permira', 'Silver Lake', 'Vista Equity', 'Thoma Bravo',
    'General Atlantic', 'Insight Partners', 'Accel', 'Sequoia',
    'Andreessen Horowitz', 'Benchmark', 'Kleiner Perkins', 'NEA',
    'Lightspeed', 'Index Ventures', 'Bessemer', 'FirstMark',
    'Summit Partners', 'TA Associates', 'Providence Equity',
    'Leonard Green', 'Clayton Dubilier', 'BC Partners',
    'PAI Partners', 'Apax Partners', 'Cinven', 'Hellman & Friedman',
    'Francisco Partners', 'Platinum Equity', 'Riverstone',
    'Brookfield', 'Fortress', 'Oaktree', 'Ares', 'Blackrock',
    'Kohlberg Kravis Roberts', 'Welsh Carson', 'Madison Dearborn',
    'GTCR', 'Audax', 'Charlesbank', 'Court Square', 'CCMP'
]

COMPANY_NAMES = [
    'TechCorp', 'DataFlow', 'CloudSystems', 'CyberSecure', 'AIVentures',
    'MedTech Solutions', 'BioPharm Inc', 'HealthWell', 'GeneCure',
    'RetailMax', 'ConsumerBrands', 'FoodCo', 'BeveragePlus',
    'Manufacturing Co', 'IndustrialTech', 'AutoParts Inc',
    'FinServe', 'PaymentTech', 'InsureTech', 'LendingPro',
    'EnergyPlus', 'SolarTech', 'CleanPower', 'OilServices',
    'RealEstate Holdings', 'Property Group', 'REIT Partners',
    'MediaCo', 'Telecom Networks', 'Software Systems',
    'Enterprise Solutions', 'SaaS Platform', 'Mobile Apps',
    'E-commerce Hub', 'Logistics Pro', 'Supply Chain Tech',
    'Education Platform', 'Training Systems', 'HR Solutions',
    'Marketing Tech', 'AdTech Solutions', 'Analytics Pro'
]

FUND_SUFFIXES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']


def random_date(start_year: int, end_year: int) -> datetime:
    """Generate a random date between start_year and end_year."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def generate_fund(vintage_year: int) -> Fund:
    """Generate a realistic private equity fund."""
    strategy = random.choice(STRATEGIES)
    firm_name = random.choice(FIRM_NAMES)
    suffix = random.choice(FUND_SUFFIXES)

    # Generate fund name
    if strategy == 'Buyout':
        fund_name = f"{firm_name} Buyout Fund {suffix}"
    elif strategy == 'Venture Capital':
        fund_name = f"{firm_name} Ventures {suffix}"
    elif strategy == 'Growth Equity':
        fund_name = f"{firm_name} Growth {suffix}"
    else:
        fund_name = f"{firm_name} {strategy} Fund {suffix}"

    # Fund size varies by strategy
    if strategy in ['Buyout', 'Infrastructure', 'Real Estate']:
        fund_size = Decimal(random.uniform(500, 15000))  # $500M - $15B
    elif strategy == 'Growth Equity':
        fund_size = Decimal(random.uniform(300, 5000))   # $300M - $5B
    elif strategy == 'Venture Capital':
        fund_size = Decimal(random.uniform(100, 2000))   # $100M - $2B
    else:
        fund_size = Decimal(random.uniform(200, 8000))   # $200M - $8B

    # Management fee typically 1.5% - 2.5%
    mgmt_fee = Decimal(random.uniform(1.5, 2.5))

    # Carry typically 15% - 30%
    carry = Decimal(random.choice([15, 20, 25, 30]))

    inception_date = random_date(vintage_year - 1, vintage_year)
    final_close_date = inception_date + timedelta(days=random.randint(180, 540))

    # Create fund identifier
    identifier = f"{firm_name.replace(' ', '').upper()}_{strategy.replace(' ', '').upper()}_{vintage_year}_{suffix}"

    fund = Fund(
        id=uuid.uuid4(),
        name=fund_name,
        identifier=identifier,
        vintage_year=vintage_year,
        strategy=strategy,
        geography=random.choice(GEOGRAPHIES),
        sector_focus=random.choice(SECTORS),
        fund_size_usd=fund_size,
        target_size_usd=fund_size * Decimal(random.uniform(0.85, 1.0)),
        committed_capital_usd=fund_size * Decimal(random.uniform(0.95, 1.0)),
        management_fee_pct=mgmt_fee,
        carry_pct=carry,
        inception_date=inception_date.date(),
        final_close_date=final_close_date.date(),
        data_confidence_score=Decimal('1.0'),  # 100% confidence for seed data
        data_source='seed_script'
    )

    return fund


def generate_performance(fund: Fund, db: Session) -> list[FundPerformance]:
    """Generate quarterly performance data for a fund."""
    performances = []

    if not fund.inception_date:
        return performances

    # Calculate fund age in quarters
    start_date = fund.inception_date
    today = datetime.now().date()
    quarters_since_inception = ((today.year - start_date.year) * 4 +
                               (today.month - start_date.month) // 3)

    # Limit to reasonable number of performance records
    num_quarters = min(quarters_since_inception, 40)  # Max 10 years

    if num_quarters <= 0:
        return performances

    # Generate cumulative metrics over time
    cumulative_contributions = 0
    cumulative_distributions = 0

    for quarter in range(1, num_quarters + 1):
        # Calculate date for this quarter
        as_of_date = start_date + timedelta(days=quarter * 90)

        # Contributions taper off over time
        if quarter <= 20:  # Investment period ~5 years
            contribution_rate = fund.fund_size_usd / 20
            contributions = float(contribution_rate) * random.uniform(0.8, 1.2)
            cumulative_contributions += contributions

        # Distributions start after a few years
        if quarter > 8:  # Start distributing after ~2 years
            distribution_rate = cumulative_contributions * 0.15  # 15% per year roughly
            distributions = distribution_rate * random.uniform(0, 0.3)
            cumulative_distributions += distributions

        # NAV = contributions - distributions + unrealized gains
        unrealized_multiple = random.uniform(1.2, 2.5)  # Unrealized gains
        nav = (cumulative_contributions - cumulative_distributions) * unrealized_multiple

        # Calculate performance metrics
        tvpi = (nav + cumulative_distributions) / cumulative_contributions if cumulative_contributions > 0 else 1.0
        dpi = cumulative_distributions / cumulative_contributions if cumulative_contributions > 0 else 0.0
        rvpi = nav / cumulative_contributions if cumulative_contributions > 0 else 1.0

        # IRR calculation (simplified)
        years_elapsed = quarter / 4.0
        if tvpi > 1.0 and years_elapsed > 0:
            irr = ((tvpi ** (1 / years_elapsed)) - 1) * 100
        else:
            irr = 0.0

        # MOIC is similar to TVPI
        moic = tvpi

        # Only create performance records for year-end and recent quarters
        if quarter % 4 == 0 or quarter >= num_quarters - 4:
            performance = FundPerformance(
                id=uuid.uuid4(),
                fund_id=fund.id,
                as_of_date=as_of_date,
                nav_usd=Decimal(str(round(nav, 2))),
                total_contributions_usd=Decimal(str(round(cumulative_contributions, 2))),
                total_distributions_usd=Decimal(str(round(cumulative_distributions, 2))),
                irr_pct=Decimal(str(round(irr, 4))),
                moic=Decimal(str(round(moic, 4))),
                dpi=Decimal(str(round(dpi, 4))),
                rvpi=Decimal(str(round(rvpi, 4))),
                tvpi=Decimal(str(round(tvpi, 4))),
                data_confidence_score=Decimal('1.0')
            )
            performances.append(performance)

    return performances


def generate_investments(fund: Fund, db: Session) -> list[Investment]:
    """Generate sample portfolio companies for a fund."""
    investments = []

    # Number of investments varies by strategy
    if fund.strategy == 'Buyout':
        num_investments = random.randint(5, 15)
    elif fund.strategy == 'Venture Capital':
        num_investments = random.randint(15, 40)
    elif fund.strategy == 'Growth Equity':
        num_investments = random.randint(8, 20)
    else:
        num_investments = random.randint(10, 25)

    # Don't create too many investments
    num_investments = min(num_investments, 20)

    for i in range(num_investments):
        company_name = random.choice(COMPANY_NAMES)

        # Investment dates spread across investment period
        if fund.inception_date:
            investment_date = fund.inception_date + timedelta(days=random.randint(0, 1800))
        else:
            investment_date = datetime.now().date()

        # Some investments have exited
        exited = random.choice([True, False, False, False])  # 25% exit rate
        exit_date = None
        if exited:
            exit_date = investment_date + timedelta(days=random.randint(730, 2190))  # 2-6 years

        # Investment amount
        avg_investment = float(fund.fund_size_usd) / num_investments
        investment_amount = Decimal(avg_investment * random.uniform(0.5, 2.0))

        # Current valuation
        if exited:
            # Exited investments show final valuation
            multiple = random.uniform(0.5, 5.0)  # Some losers, some big winners
            current_valuation = investment_amount * Decimal(multiple)
        else:
            # Active investments show unrealized gains
            multiple = random.uniform(0.8, 3.0)
            current_valuation = investment_amount * Decimal(multiple)

        # Ownership
        ownership = Decimal(random.uniform(10, 60))

        investment = Investment(
            id=uuid.uuid4(),
            fund_id=fund.id,
            company_name=f"{company_name} {random.choice(['Inc', 'LLC', 'Corp', 'Ltd', 'Group'])}",
            company_identifier=f"{company_name.replace(' ', '').upper()}_{random.randint(1000, 9999)}",
            investment_date=investment_date,
            exit_date=exit_date if exited else None,
            investment_amount_usd=investment_amount,
            current_valuation_usd=current_valuation,
            ownership_pct=ownership,
            industry=random.choice(SECTORS),
            geography=fund.geography,  # Same as fund usually
            stage=random.choice(['Seed', 'Series A', 'Series B', 'Growth', 'Late Stage', 'Buyout']),
            status='exited' if exited else 'active',
            data_confidence_score=Decimal('1.0')
        )
        investments.append(investment)

    return investments


def seed_database():
    """Main function to seed the database with sample data."""
    print("Starting database seeding...")

    # Create database session
    db = SessionLocal()

    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.query(FundPerformance).delete()
        db.query(Investment).delete()
        db.query(Fund).delete()
        db.commit()

        # Generate funds across different vintage years
        vintage_years = list(range(2010, 2025))  # 2010-2024
        funds_to_create = 120  # Create 120 funds

        print(f"Generating {funds_to_create} funds...")
        all_funds = []

        for i in range(funds_to_create):
            vintage_year = random.choice(vintage_years)
            fund = generate_fund(vintage_year)
            all_funds.append(fund)

            if (i + 1) % 20 == 0:
                print(f"  Generated {i + 1} funds...")

        # Batch insert funds
        print("Inserting funds into database...")
        db.bulk_save_objects(all_funds)
        db.commit()

        # Generate performance and investments for each fund
        print("Generating performance data and investments...")
        total_investments = 0
        total_performances = 0

        for idx, fund in enumerate(all_funds):
            # Refresh to get the fund ID
            db.refresh(fund)

            # Generate performance data
            performances = generate_performance(fund, db)
            if performances:
                db.bulk_save_objects(performances)
                total_performances += len(performances)

            # Generate investments (only for ~70% of funds to vary data)
            if random.random() < 0.7:
                investments = generate_investments(fund, db)
                if investments:
                    db.bulk_save_objects(investments)
                    total_investments += len(investments)

            if (idx + 1) % 20 == 0:
                print(f"  Processed {idx + 1} funds...")
                db.commit()

        db.commit()

        print("\n" + "="*60)
        print("Database seeding completed successfully!")
        print("="*60)
        print(f"Created {len(all_funds)} funds")
        print(f"Created {total_investments} investments")
        print(f"Created {total_performances} performance records")
        print(f"\nAll data has confidence_score = 1.0 (100%)")
        print("\nYou can now start the FastAPI server and view the data!")
        print("="*60)

    except Exception as e:
        print(f"\nError during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
