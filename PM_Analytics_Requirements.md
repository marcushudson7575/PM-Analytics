# PM Analytics - Product Requirements Document

## Executive Summary

PM Analytics is a comprehensive data platform designed to solve the private markets industry's data opacity problem. The platform captures, synthesizes (cleans), and stores data across the private markets industry to create actionable insights for General Partners (GP) and Limited Partners (LP).

## Problem Statement

The private markets industry is renowned for messy, opaque, and inconsistent data, which limits GP and LPs from making informed decisions. As institutional investors increase allocations to private equity, private credit, infrastructure, and real assets, more transparency is being demanded. 

## Solution Overview

PM Analytics provides:
- Automated data capture through real-time internet access
- Suplemented by the ability to add in manual data, sourced from PMA's private markets network built over 25+ years
- Data synthesis and cleaning capabilities
- Actionable insights and analytics
- The ability to filter data, and the user can search for certain data accross private markets

---

## Product Goals

### Primary Goals
1. **Data Democratization**: Make private markets data accessible and transparent
2. **Decision Support**: Enable informed investment decisions through actionable insights
3. **Operational Efficiency**: Streamline fund management operations through integrated tools
4. **Data Quality**: Transform messy, inconsistent data into clean, reliable datasets

### Success Metrics
- Data coverage across private markets funds
- Data accuracy and completeness rates
- User adoption and engagement
- Time saved in data collection and analysis
- Decision-making confidence improvement

---

## Product Architecture

### Core Platform

PM Analytics is built as a comprehensive platform that serves all private markets stakeholders - from GPs and fund managers to LPs and institutional investors. The platform is organized into the following core modules:

#### Core Modules

##### 1. Data Ingestion Layer
**Requirements:**
- Automated web scraping capabilities from trusted public data sources
- Manual data entry interfaces for proprietary information
- Bulk data import capabilities (CSV, Excel, PDF parsing)
- Real-time data feeds where available, to update weekly
- Version control and audit trails for all data inputs

**Technical Specifications:**
- Processing capacity: 10,000+ data points per day
- Data validation rules engine
- Duplicate detection and merging logic
- Error handling and retry mechanisms

##### 2. Data Synthesis & Cleaning Engine
**Requirements:**
- Automated data normalization across different formats
- Entity resolution and matching
- Data quality scoring and flagging
- Missing data handling and imputation strategies
- Outlier detection and correction
- Standardization of:
  - Company names and identifiers
  - Date formats
  - Currency conversions
  - Industry classifications
  - Geographic data

**Technical Specifications:**
- Machine learning-based data matching
- Configurable cleaning rules
- Manual override capabilities
- Data lineage tracking
- Confidence scores for cleaned data - MUST be 100% confidence to display

##### 3. Data Storage & Management
**Requirements:**
- Centralized database for all private markets data
- Historical data retention
- Data security and encryption
- Role-based access controls
- Data backup and disaster recovery
- Scalable architecture for growth

**Technical Specifications:**
- Relational database for structured data
- Document store for unstructured data
- Time-series database for performance metrics
- Minimum 95% uptime SLA
- GDPR and compliance-ready infrastructure

##### 4. Fund Management Dashboard
**Requirements:**
- Real-time fund performance monitoring
- Portfolio composition views
- Investment tracking and lifecycle management
- Capital calls and distribution management
- Document management system

**Features:**
- Customizable dashboard layouts
- Drag-and-drop widgets
- Exportable reports
- Mobile-responsive design

##### 5. Analytics & Reporting Engine
**Requirements:**
- Pre-built analytical programs for clients
- Custom report builder

**Deliverables:**
- Standard report templates (quarterly, annual, ad-hoc)
- Interactive visualizations
- Trend analysis and forecasting
- Export to PDF

---

## Functional Requirements

### FR-1: User Management
- User registration and authentication
- Multi-factor authentication support
- Role-based permissions (Admin, Viewer)

### FR-2: Data Capture
- **Automated Capture:**
  - Scheduled web scraping jobs (weekly)
  - Email parsing for data extraction
  - RSS/feed monitoring

- **Manual Capture:**
  - Forms for structured data entry
  - Bulk upload interfaces
  - Document upload and OCR processing
  - Mobile data entry capability

### FR-3: Data Quality Management
- Validation rules at point of entry
- Data quality dashboard
- Error notification system
- Data stewardship workflows
- Quality metrics and KPIs

### FR-4: Fund Operations
- Fund creation and setup
- Investment transaction recording
- Capital account management
- Fee and expense tracking
- Valuation workflows
- Compliance monitoring

### FR-5: Portfolio Management
- Portfolio construction and monitoring
- Asset allocation tracking
- Exposure analysis
- Risk metrics calculation
- Rebalancing recommendations

### FR-6: Investor Relations
- Investor onboarding
- Communication management
- Document distribution
- Performance reporting
- Query management

### FR-7: Analytics
- Performance analytics (IRR, MOIC, DPI, RVPI, TVPI)
- Attribution analysis
- Cohort analysis
- Comparative analytics
- Custom metric creation

### FR-8: Reporting
- Drag-and-drop report builder
- Template management
- Scheduled report generation
- White-label capabilities

### FR-9: Data Export
- Data export capabilities in pdf format
- Export audit trails

### FR-10: Administration
- System configuration
- Data retention policies
- Audit trail access
- Backup management
- System health monitoring

---

## Technical Requirements

### TR-1: Performance
- Page load time: < 120 seconds
- Report generation: < 120 seconds for standard reports
- Data refresh: Every week
- Support for 100 concurrent users
- Database query response: < 5 seconds

### TR-2: Security
- SOC 2 Type II compliance
- Encryption at rest and in transit
- Regular security audits
- Penetration testing
- DDoS protection
- Data anonymization capabilities

### TR-3: Reliability
- 95% uptime guarantee
- Automated failover
- Disaster recovery plan
- Load balancing

### TR-5: Technology Stack

**Phase 1: GitHub Pages (MVP/Beta)**
- **Frontend:** React/Next.js (static export), TypeScript, Tailwind CSS
- **Hosting:** GitHub Pages
- **Backend:** Serverless functions (Vercel/Netlify) or separate API hosting
- **Database:** Cloud-hosted database service
- **Version Control:** GitHub
- **CI/CD:** GitHub Actions
- **Analytics:** Google Analytics or similar
- **Visualization:** D3.js, Chart.js, Plotly

**Phase 2: PMA Website (Production)**
- **Frontend:** React/Next.js, TypeScript, Tailwind CSS
- **Backend:** Node.js/Python, Internal REST APIs
- **Database:** PostgreSQL, MongoDB, Redis
- **Cloud:** AWS/Azure/GCP
- **Analytics:** Python (pandas, NumPy), R
- **Visualization:** D3.js, Chart.js, Plotly
- **Infrastructure:** Docker, Kubernetes
- **Monitoring:** Application performance monitoring tools
- **CDN:** CloudFlare or AWS CloudFront
- **Domain:** Custom PMA domain with SSL

### TR-6: Browser Support
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Data Requirements

### DR-1: Data Entities

#### Funds
- Fund name, identifier, vintage year
- Strategy, geography, sector focus
- Fund size, target size, committed capital
- Management fees, carry structure
- Key dates (inception, final close, end date)

#### Investments
- Company name, identifier
- Investment date, exit date
- Investment amount, valuation
- Ownership percentage
- Industry, geography
- Investment stage

#### Performance
- NAV (Net Asset Value)
- Cash flows (contributions, distributions)
- Valuations over time
- Returns (IRR, MOIC, etc.)
- Benchmarks

#### Investors (LPs)
- Investor name, type
- Commitment amount
- Capital called, distributed
- Contact information
- Reporting preferences

#### Transactions
- Transaction type (capital call, distribution, transfer)
- Amount, date
- Related entities
- Supporting documents

### DR-2: Data Sources
- Fund administrator reports
- Audited financial statements
- News and press releases from reputable sources such as the FT
- SEC filings (Form D, Form ADV)
- Publically available data from private market markets e.g. Large LPs and European investment funds, Pension fund PSERS Private market funds, US public pension funds, (Washington state investment board), florida pension fund, track vc website
- Proprietary network data

### DR-3: Data Governance
- Data ownership and stewardship
- Data classification (public, confidential, restricted)
- Retention policies
- Access controls
- Change management procedures

---

## User Interface Requirements

### UI-1: Design Principles
- Clean, professional aesthetic
- Intuitive navigation
- Minimal clicks to key actions
- Consistent design language
- Accessible (WCAG 2.1 AA compliance)

### UI-2: Key Screens

#### Dashboard
- Customizable widget-based layout
- At-a-glance KPIs
- Recent activity feed
- Quick action buttons
- Alerts and notifications panel

#### Analytics Workspace
- Metric selector
- Date range picker
- Comparison tools
- Visualization options
- Export functionality (PDF)

#### Report Builder
- Template gallery
- Drag-and-drop interface
- Data binding controls
- Preview mode
- Scheduling options

---

## Compliance & Regulatory Requirements

### CR-1: Data Privacy
- GDPR compliance
- CCPA compliance
- Right to deletion
- Data portability
- Privacy policy and terms of service

### CR-2: Financial Regulations
- SEC compliance (for US funds)
- AIFMD compliance (for EU funds)
- AML/KYC requirements
- Audit trail requirements

### CR-3: Industry Standards
- ILPA reporting templates
- GIPS (Global Investment Performance Standards)
- Fair value measurement standards

---

## Deployment & Operations

### DO-1: Deployment Strategy

#### Phase 1: GitHub Pages Hosting (Initial Launch)
**Timeline:** MVP and Early Beta
- Host PM Analytics as a static website on GitHub Pages
- Accessible via GitHub.io domain
- Benefits:
  - Free hosting with version control integration
  - Easy deployment through git commits
  - Built-in CI/CD with GitHub Actions
  - Fast iteration and testing
  - Community feedback and issue tracking via GitHub
- Limitations:
  - Static hosting only (frontend focus)
  - Backend services will need separate hosting (serverless functions or separate API)
  - Custom domain options available but branded as development/beta

#### Phase 2: PMA Website Integration (Production)
**Timeline:** After successful beta testing and user validation
- Migrate to dedicated section on official PMA website
- Professional domain: analytics.pmawebsite.com or pmawebsite.com/analytics
- Benefits:
  - Full control over infrastructure
  - Professional branding and domain
  - Integrated with existing PMA ecosystem
  - Better security and compliance capabilities
  - Full-stack deployment (frontend + backend)
  - Custom authentication and user management
- Requirements:
  - Stable, tested codebase from GitHub phase
  - Infrastructure setup (cloud hosting, databases, CDN)
  - DNS configuration and SSL certificates
  - Migration plan for any beta users

#### General Deployment Practices
- Staged rollout (dev → staging → production)
- Blue-green deployment for zero-downtime updates
- Feature flags for gradual feature release
- Rollback procedures and version tagging
- Automated testing before deployment

### DO-2: Monitoring & Support
- Application performance monitoring
- Error tracking and alerting
- User analytics
- Support ticket system
- Knowledge base and documentation


---

### Assumptions:
1. Users have reliable internet connectivity
2. Most data will be in English initially
3. Standard private equity metrics are sufficient for MVP
4. Cloud deployment is acceptable to target users
5. Users have modern browsers and devices

---

## Appendix

### A. Glossary
- **GP**: General Partner - the fund manager
- **LP**: Limited Partner - the investor in the fund
- **IRR**: Internal Rate of Return
- **MOIC**: Multiple on Invested Capital
- **DPI**: Distributions to Paid-In capital
- **RVPI**: Residual Value to Paid-In capital
- **TVPI**: Total Value to Paid-In capital
- **NAV**: Net Asset Value
- **Vintage Year**: The year the fund was launched

### B. References
- ILPA Reporting Templates
- GIPS Standards
- SEC Form ADV
- AIFMD Regulations

---

## Document Control

**Version:** 1.0
**Date:** 2026-01-30
**Author:** PM Analytics Team
**Status:** Draft for Review
**Next Review:** TBD
