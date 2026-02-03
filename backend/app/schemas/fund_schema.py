"""
Pydantic schemas for Fund API endpoints.
"""
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class FundBase(BaseModel):
    """Base fund schema"""
    name: str
    identifier: Optional[str] = None
    vintage_year: Optional[int] = None
    strategy: Optional[str] = None
    geography: Optional[str] = None
    sector_focus: Optional[str] = None
    fund_size_usd: Optional[Decimal] = None
    target_size_usd: Optional[Decimal] = None
    committed_capital_usd: Optional[Decimal] = None
    management_fee_pct: Optional[Decimal] = None
    carry_pct: Optional[Decimal] = None
    inception_date: Optional[date] = None
    final_close_date: Optional[date] = None
    end_date: Optional[date] = None
    data_confidence_score: Decimal
    data_source: Optional[str] = None


class FundResponse(FundBase):
    """Fund response schema"""
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FundListResponse(BaseModel):
    """List of funds response"""
    funds: list[FundResponse]
    total: int
    page: int
    page_size: int
