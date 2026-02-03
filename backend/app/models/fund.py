from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, Boolean, Text, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base


class Fund(Base):
    """Fund model - Main fund entity"""

    __tablename__ = "funds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    identifier = Column(String(100), unique=True)
    vintage_year = Column(Integer, index=True)
    strategy = Column(String(100), index=True)  # PE, VC, Infrastructure, Real Estate, Private Credit
    geography = Column(String(100))
    sector_focus = Column(String(100))

    # Fund size and fees
    fund_size_usd = Column(Numeric(15, 2))
    target_size_usd = Column(Numeric(15, 2))
    committed_capital_usd = Column(Numeric(15, 2))
    management_fee_pct = Column(Numeric(5, 2))
    carry_pct = Column(Numeric(5, 2))

    # Dates
    inception_date = Column(Date)
    final_close_date = Column(Date)
    end_date = Column(Date)

    # Data quality and audit
    data_confidence_score = Column(
        Numeric(3, 2),
        nullable=False,
        default=0.0,
        index=True
    )
    data_source = Column(String(100))  # 'sec', 'scraper', 'manual', etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    investments = relationship("Investment", back_populates="fund", cascade="all, delete-orphan")
    performance_records = relationship("FundPerformance", back_populates="fund", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint('data_confidence_score >= 0 AND data_confidence_score <= 1', name='confidence_range'),
    )

    def __repr__(self):
        return f"<Fund(name='{self.name}', vintage={self.vintage_year}, confidence={self.data_confidence_score})>"


class Investment(Base):
    """Investment model - Portfolio companies"""

    __tablename__ = "investments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id', ondelete='CASCADE'), nullable=False, index=True)
    company_name = Column(String(255), nullable=False)
    company_identifier = Column(String(100))

    # Investment details
    investment_date = Column(Date)
    exit_date = Column(Date)
    investment_amount_usd = Column(Numeric(15, 2))
    current_valuation_usd = Column(Numeric(15, 2))
    ownership_pct = Column(Numeric(5, 2))

    # Classification
    industry = Column(String(100))
    geography = Column(String(100))
    stage = Column(String(50))  # Seed, Series A, Growth, etc.
    status = Column(String(50), default='active')  # active, exited, written_off

    # Data quality
    data_confidence_score = Column(Numeric(3, 2), default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    fund = relationship("Fund", back_populates="investments")

    def __repr__(self):
        return f"<Investment(company='{self.company_name}', fund_id={self.fund_id})>"


class FundPerformance(Base):
    """Fund performance metrics - Time series data"""

    __tablename__ = "fund_performance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), ForeignKey('funds.id', ondelete='CASCADE'), nullable=False, index=True)
    as_of_date = Column(Date, nullable=False)

    # Financial metrics
    nav_usd = Column(Numeric(15, 2))
    total_contributions_usd = Column(Numeric(15, 2))
    total_distributions_usd = Column(Numeric(15, 2))

    # Performance metrics
    irr_pct = Column(Numeric(7, 4))  # IRR as percentage
    moic = Column(Numeric(7, 4))  # Multiple on Invested Capital
    dpi = Column(Numeric(7, 4))  # Distributions to Paid-In
    rvpi = Column(Numeric(7, 4))  # Residual Value to Paid-In
    tvpi = Column(Numeric(7, 4))  # Total Value to Paid-In

    # Data quality
    data_confidence_score = Column(Numeric(3, 2), default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    fund = relationship("Fund", back_populates="performance_records")

    def __repr__(self):
        return f"<FundPerformance(fund_id={self.fund_id}, date={self.as_of_date}, irr={self.irr_pct})>"


class DataSource(Base):
    """Data sources tracking"""

    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String(100), nullable=False)
    source_type = Column(String(50))  # 'web_scraper', 'sec_filing', 'manual', 'csv_import'
    url = Column(Text)
    last_scraped_at = Column(DateTime(timezone=True))
    scrape_frequency_days = Column(Integer, default=7)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DataSource(name='{self.source_name}', type='{self.source_type}')>"


class IngestionLog(Base):
    """Data ingestion log for audit trail"""

    __tablename__ = "ingestion_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True))
    ingestion_started_at = Column(DateTime(timezone=True), server_default=func.now())
    ingestion_completed_at = Column(DateTime(timezone=True))
    status = Column(String(50))  # 'success', 'partial', 'failed'
    records_processed = Column(Integer)
    records_accepted = Column(Integer)
    records_rejected = Column(Integer)
    error_message = Column(Text)

    def __repr__(self):
        return f"<IngestionLog(source_id={self.source_id}, status='{self.status}')>"


class DataQualityIssue(Base):
    """Data quality issues tracking"""

    __tablename__ = "data_quality_issues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50))  # 'fund', 'investment', 'performance'
    entity_id = Column(UUID(as_uuid=True))
    issue_type = Column(String(100))  # 'missing_field', 'duplicate', 'outlier', 'invalid_format'
    issue_description = Column(Text)
    severity = Column(String(20))  # 'critical', 'high', 'medium', 'low'
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<DataQualityIssue(type='{self.issue_type}', severity='{self.severity}', resolved={self.is_resolved})>"
