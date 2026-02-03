"""
Fund API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

from app.db.database import get_db
from app.models.fund import Fund
from app.schemas.fund_schema import FundResponse, FundListResponse
from app.config import settings

router = APIRouter(prefix="/funds", tags=["funds"])


@router.get("", response_model=FundListResponse)
def list_funds(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    strategy: Optional[str] = Query(None, description="Filter by strategy"),
    vintage_year: Optional[int] = Query(None, description="Filter by vintage year"),
    geography: Optional[str] = Query(None, description="Filter by geography"),
    min_size: Optional[float] = Query(None, description="Minimum fund size (USD)"),
    max_size: Optional[float] = Query(None, description="Maximum fund size (USD)"),
    min_confidence: float = Query(0.95, ge=0, le=1, description="Minimum confidence score"),
    db: Session = Depends(get_db)
):
    """
    List funds with filtering and pagination.

    Default: Only shows funds with confidence >= 95%
    """
    query = db.query(Fund)

    # Always filter by minimum confidence
    query = query.filter(Fund.data_confidence_score >= min_confidence)

    # Apply filters
    if strategy:
        query = query.filter(Fund.strategy == strategy)

    if vintage_year:
        query = query.filter(Fund.vintage_year == vintage_year)

    if geography:
        query = query.filter(Fund.geography == geography)

    if min_size is not None:
        query = query.filter(Fund.fund_size_usd >= min_size)

    if max_size is not None:
        query = query.filter(Fund.fund_size_usd <= max_size)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    funds = query.order_by(Fund.fund_size_usd.desc()).offset(offset).limit(page_size).all()

    return FundListResponse(
        funds=funds,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{fund_id}", response_model=FundResponse)
def get_fund(
    fund_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a specific fund by ID.
    """
    fund = db.query(Fund).filter(Fund.id == fund_id).first()

    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Only return funds with high confidence
    if fund.data_confidence_score < Decimal('0.95'):
        raise HTTPException(
            status_code=403,
            detail="Fund data confidence too low for display"
        )

    return fund


@router.get("/search/", response_model=FundListResponse)
def search_funds(
    q: str = Query(..., min_length=2, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Search funds by name, manager, or identifier.
    """
    search_pattern = f"%{q}%"

    query = db.query(Fund).filter(
        or_(
            Fund.name.ilike(search_pattern),
            Fund.identifier.ilike(search_pattern),
            Fund.data_source.ilike(search_pattern)
        ),
        Fund.data_confidence_score >= min_confidence
    )

    total = query.count()
    offset = (page - 1) * page_size
    funds = query.offset(offset).limit(page_size).all()

    return FundListResponse(
        funds=funds,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/stats/by-strategy")
def get_funds_by_strategy(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get fund count and total AUM by strategy.
    """
    results = db.query(
        Fund.strategy,
        func.count(Fund.id).label('count'),
        func.sum(Fund.fund_size_usd).label('total_aum'),
        func.avg(Fund.fund_size_usd).label('avg_fund_size')
    ).filter(
        Fund.data_confidence_score >= min_confidence
    ).group_by(
        Fund.strategy
    ).all()

    return {
        "strategies": [
            {
                "strategy": result[0],
                "fund_count": result[1],
                "total_aum_usd": float(result[2]) if result[2] else 0,
                "avg_fund_size_usd": float(result[3]) if result[3] else 0
            }
            for result in results
        ]
    }


@router.get("/stats/by-geography")
def get_funds_by_geography(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get fund count and total AUM by geography.
    """
    results = db.query(
        Fund.geography,
        func.count(Fund.id).label('count'),
        func.sum(Fund.fund_size_usd).label('total_aum')
    ).filter(
        Fund.data_confidence_score >= min_confidence
    ).group_by(
        Fund.geography
    ).all()

    return {
        "geographies": [
            {
                "geography": result[0],
                "fund_count": result[1],
                "total_aum_usd": float(result[2]) if result[2] else 0
            }
            for result in results
        ]
    }


@router.get("/stats/vintage-years")
def get_funds_by_vintage_year(
    min_confidence: float = Query(0.95, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """
    Get fund count and total AUM by vintage year.
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
        Fund.vintage_year.desc()
    ).all()

    return {
        "vintage_years": [
            {
                "year": result[0],
                "fund_count": result[1],
                "total_aum_usd": float(result[2]) if result[2] else 0
            }
            for result in results
        ]
    }
