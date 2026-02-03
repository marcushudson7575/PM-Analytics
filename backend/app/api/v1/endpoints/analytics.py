"""
Analytics API endpoints for dashboard KPIs.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from app.db.database import get_db
from app.models.fund import Fund

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def get_dashboard_kpis(
    min_confidence: float = Query(0.95, ge=0, le=1, description="Minimum confidence score"),
    db: Session = Depends(get_db)
):
    """
    Get dashboard KPIs:
    - Total number of funds
    - Total AUM
    - Number of strategies represented
    - Average fund size
    - Data quality percentage
    """
    # Total funds (high confidence)
    total_funds = db.query(func.count(Fund.id)).filter(
        Fund.data_confidence_score >= min_confidence
    ).scalar()

    # Total AUM
    total_aum = db.query(func.sum(Fund.fund_size_usd)).filter(
        Fund.data_confidence_score >= min_confidence
    ).scalar()

    # Average fund size
    avg_fund_size = db.query(func.avg(Fund.fund_size_usd)).filter(
        Fund.data_confidence_score >= min_confidence
    ).scalar()

    # Number of unique strategies
    unique_strategies = db.query(func.count(func.distinct(Fund.strategy))).filter(
        Fund.data_confidence_score >= min_confidence
    ).scalar()

    # Number of unique geographies
    unique_geographies = db.query(func.count(func.distinct(Fund.geography))).filter(
        Fund.data_confidence_score >= min_confidence
    ).scalar()

    # Data quality: percentage of funds with 100% confidence
    total_all_funds = db.query(func.count(Fund.id)).scalar()
    high_confidence_funds = db.query(func.count(Fund.id)).filter(
        Fund.data_confidence_score >= 0.95
    ).scalar()

    data_quality_pct = (high_confidence_funds / total_all_funds * 100) if total_all_funds > 0 else 0

    return {
        "total_funds": total_funds or 0,
        "total_aum_usd": float(total_aum) if total_aum else 0,
        "avg_fund_size_usd": float(avg_fund_size) if avg_fund_size else 0,
        "unique_strategies": unique_strategies or 0,
        "unique_geographies": unique_geographies or 0,
        "data_quality_pct": round(data_quality_pct, 2),
        "min_confidence_threshold": min_confidence
    }


@router.get("/aum-by-strategy")
def get_aum_by_strategy(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get AUM distribution by strategy (for pie/donut chart).
    """
    results = db.query(
        Fund.strategy,
        func.sum(Fund.fund_size_usd).label('total_aum'),
        func.count(Fund.id).label('fund_count')
    ).filter(
        Fund.data_confidence_score >= min_confidence
    ).group_by(
        Fund.strategy
    ).all()

    # Calculate total for percentages
    total_aum = sum(float(r[1]) if r[1] else 0 for r in results)

    return {
        "chart_data": [
            {
                "strategy": result[0],
                "aum_usd": float(result[1]) if result[1] else 0,
                "percentage": round((float(result[1]) / total_aum * 100) if total_aum > 0 else 0, 2),
                "fund_count": result[2]
            }
            for result in results
        ],
        "total_aum_usd": total_aum
    }


@router.get("/geography-by-strategy")
def get_geography_by_strategy(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get fund count by strategy and geography (for stacked bar chart).
    """
    results = db.query(
        Fund.strategy,
        Fund.geography,
        func.count(Fund.id).label('count')
    ).filter(
        Fund.data_confidence_score >= min_confidence
    ).group_by(
        Fund.strategy,
        Fund.geography
    ).all()

    # Organize data for charting
    strategy_data = {}
    for strategy, geography, count in results:
        if strategy not in strategy_data:
            strategy_data[strategy] = {}
        strategy_data[strategy][geography] = count

    return {
        "chart_data": [
            {
                "strategy": strategy,
                "geographies": geo_counts
            }
            for strategy, geo_counts in strategy_data.items()
        ]
    }


@router.get("/avg-fees-by-strategy")
def get_avg_fees_by_strategy(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get average management fee by strategy (for bar chart).
    """
    results = db.query(
        Fund.strategy,
        func.avg(Fund.management_fee_pct).label('avg_mgmt_fee'),
        func.avg(Fund.carry_pct).label('avg_carry')
    ).filter(
        Fund.data_confidence_score >= min_confidence,
        Fund.management_fee_pct.isnot(None)
    ).group_by(
        Fund.strategy
    ).all()

    return {
        "chart_data": [
            {
                "strategy": result[0],
                "avg_management_fee_pct": float(result[1]) if result[1] else None,
                "avg_carry_pct": float(result[2]) if result[2] else None
            }
            for result in results
        ]
    }


@router.get("/vintage-year-distribution")
def get_vintage_year_distribution(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get fund count and AUM by vintage year (for timeline chart).
    """
    results = db.query(
        Fund.vintage_year,
        func.count(Fund.id).label('count'),
        func.sum(Fund.fund_size_usd).label('total_aum')
    ).filter(
        Fund.data_confidence_score >= min_confidence,
        Fund.vintage_year.isnot(None)
    ).group_by(
        Fund.vintage_year
    ).order_by(
        Fund.vintage_year
    ).all()

    return {
        "chart_data": [
            {
                "year": result[0],
                "fund_count": result[1],
                "total_aum_usd": float(result[2]) if result[2] else 0
            }
            for result in results
        ]
    }
