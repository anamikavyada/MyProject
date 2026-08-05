# Healthcare Claims Denial & Revenue Leakage Analytics

**SQL | Python | Power BI | DAX | Data Quality | Business Intelligence**

> End-to-end portfolio analytics project demonstrating how claim-level healthcare data can be transformed into executive KPIs, payer/provider analysis, denial-driver investigation, and actionable business recommendations.

**Portfolio note:** This project uses synthetic, business-realistic data. It is not a real client implementation and contains no real patient or confidential healthcare information.

## Business Problem

Healthcare claims denials can delay reimbursement, increase accounts receivable, and create preventable revenue leakage. The analysis answers:

- Which payers have the highest denial rates?
- Which denial reasons contribute most to financial leakage?
- Which providers/departments show elevated performance risk?
- Where should coding, documentation, authorization, or process improvements be prioritized?
- Can executive KPIs be traced back to payer, provider, and claim-level detail?

## Executive Results

The Power BI report analyzes **465,435 claims** across a simulated **2021–2025** period.

| KPI | Result |
|---|---:|
| Denial Rate | **12.2%** |
| Clean Claim Rate | **80.8%** |
| Net Leakage | **$376.5M** |
| Average Days in AR | **32 days** |
| Claims Analyzed | **465,435** |

> These are simulated portfolio results, not real business outcomes.

## Dashboard Preview

### Executive Summary

![Executive Summary](docs/dashboard-previews/executive-summary.svg.png)

The executive view combines KPI cards, denial-rate trends, denial-reason contribution, and interactive payer/department filters.

### Payer Drilldown

![Payer Drilldown](docs/dashboard-previews/payer-drilldown.png)

The payer view moves from payer-level denial performance into provider-level detail using Total Claims, Denial Rate, and Net Leakage.

### Provider Risk

![Provider Risk](docs/dashboard-previews/provider-risk.png)

The provider-risk view segments providers into Low, Moderate, High, and Very High Risk tiers and compares experience, denial rate, department, and claim volume.

## Report Pages

### 1. Executive Summary
- Denial Rate
- Net Leakage
- Clean Claim Rate
- Average Days in AR
- Denial-rate trend by time
- Leakage by denial reason
- Payer and department filters

### 2. Payer Drilldown
- Denial Rate by payer
- Total Claims
- Net Leakage
- Provider-level breakdown
- Department filtering

### 3. Claim-Level Detail
- Claim ID
- Procedure Code
- Claim Amount
- Claim Status
- Denial Reason Code

This creates a traceable path from **KPI → payer/provider → individual claim**.

### 4. Provider Risk
- Risk segmentation
- Provider denial rate
- Claim volume
- Department analysis
- Experience vs. denial-rate comparison

## Analytical Workflow

```text
Synthetic Claims Data
        ↓
Data Cleaning & Validation
        ↓
SQL Analytical Layer
        ↓
Python / Pandas Analysis
        ↓
Power BI Data Model + DAX
        ↓
Interactive Dashboard
        ↓
Business Insights & Recommendations
```

### Data Preparation & Quality

- Standardized claim status values
- Validated required fields
- Checked null and blank values
- Checked duplicate claim identifiers
- Validated payer/provider/department relationships
- Reconciled claim-level totals with dashboard aggregates

### SQL Analytics

The portfolio demonstrates:

- CTEs
- Multi-table joins
- Conditional aggregation
- Window functions
- Ranking
- Period-over-period analysis
- Pareto analysis
- Data-quality checks
- KPI-ready analytical outputs

Example:

```sql
SELECT
    payer_name,
    COUNT(*) AS total_claims,
    SUM(CASE WHEN status_clean = 'Denied' THEN 1 ELSE 0 END) AS denied_claims,
    CAST(
        100.0 * SUM(CASE WHEN status_clean = 'Denied' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0)
        AS DECIMAL(10,2)
    ) AS denial_rate
FROM claims
GROUP BY payer_name
ORDER BY denial_rate DESC;
```

### Python

Python/Pandas is used for:

- Data preparation
- Exploratory data analysis
- Validation checks
- Analytical transformations
- Feature preparation for reporting

### Power BI

The report uses:

- KPI cards
- Time-series analysis
- Payer drilldowns
- Provider risk segmentation
- Claim-level tables
- Interactive filters
- DAX measures

The reporting pattern is:

**Executive KPI → Trend → Driver Analysis → Segment Drilldown → Claim Investigation**

## Key Business Insights

- Payer denial performance varies materially, supporting payer-level monitoring.
- Denial reasons should be prioritized by financial impact as well as frequency.
- Provider risk segmentation helps identify high-risk outliers for investigation.
- Claim-level drilldown provides traceability from aggregate KPIs to records.
- Combining denial rate, claim volume, and financial exposure creates a stronger prioritization framework than using one metric alone.

Denial categories represented include **Duplicate Claim, Eligibility Expired, Non-Covered Service, Coding Mismatch, Prior Authorization, Medical Necessity, Timely Filing, and Documentation-related issues**.

## Business Recommendations

| Finding | Potential Action |
|---|---|
| High prior-authorization denials | Strengthen authorization validation before submission |
| Coding-related denials | Target coding-quality review and training |
| Documentation-related denials | Improve documentation completeness checks |
| High-risk providers | Perform provider-level root-cause analysis |
| Payer-specific denial spikes | Review payer rules and submission requirements |
| High-value denied claims | Prioritize recoverability and appeal analysis |

Because the dataset is synthetic, these are **portfolio recommendations**, not claimed real-world savings.

## Data Quality & Validation

Data quality is treated as part of the analytical solution through:

- Duplicate detection
- Missing-value analysis
- Status consistency checks
- Payer/provider relationship validation
- Numeric validation of claim amounts
- Denial-reason consistency
- Aggregate reconciliation

## Interview Talking Points

**Data Analyst:** I started with claim-level data, applied data-quality and business-rule checks, calculated core KPIs, and designed Power BI views that allow stakeholders to move from executive metrics into payer, provider, and claim-level analysis.

**SQL:** I used joins, CTEs, conditional aggregation, window functions, ranking, trend analysis, and reconciliation checks to create reliable analytical outputs.

**Power BI:** Executives need KPIs and trends, managers need payer/provider comparisons, and analysts need claim-level records for investigation, so the report provides progressively deeper levels of detail.

**Business Analysis:** For a high-denial provider, I would segment denials by reason, payer, department, and financial impact, identify dominant drivers, and recommend a targeted operational intervention.

## Technology Stack

| Category | Tools |
|---|---|
| BI | Power BI Desktop, DAX |
| Querying | SQL |
| Programming | Python, Pandas |
| Analytics | KPI analysis, EDA, trend analysis, Pareto analysis, risk segmentation |
| Data Quality | Validation, reconciliation, duplicate/null checks |
| Business Analysis | Root-cause analysis, prioritization, decision support |

## Data Disclaimer

**All healthcare data and financial figures represented in this project are synthetic and intended only for learning, portfolio demonstration, and interview discussion.** No real patient information, confidential employer information, or production healthcare-system data is included.

## Portfolio Positioning

This project demonstrates the ability to combine:

**SQL + Python + Power BI + DAX + Data Quality + Business Analysis + Data Storytelling**

into an end-to-end analytics solution rather than presenting a dashboard as an isolated visualization exercise.
