# Healthcare Claims Denial & Revenue Leakage Analytics

**SQL | Python | Power BI | Data Quality | Revenue Cycle Analytics | Business Intelligence**

> End-to-end portfolio analytics project demonstrating how claim-level healthcare data can be transformed into executive KPIs, payer/provider analysis, denial-driver investigation, and actionable business recommendations.

**Portfolio note:** This project uses synthetic, business-realistic data. It is not a real client implementation and contains no real patient or confidential healthcare information.

## Business Problem

Healthcare claims denials can delay reimbursement, increase accounts receivable, and create preventable revenue leakage. Revenue Cycle and operations teams need to answer:

- Which payers have the highest denial rates?
- Which denial reasons contribute most to financial leakage?
- Which providers or departments show elevated denial performance risk?
- Where should coding, documentation, authorization, or process improvements be prioritized?
- Can an executive KPI be traced back to individual claims for investigation?

The project approaches the problem from a **Data Analyst / BI Analyst perspective**, combining data preparation, validation, SQL analysis, Power BI modeling, and business storytelling.

## Executive Dashboard

The Power BI dashboard analyzes **465,435 claims** across a simulated **2021–2025** period.

| KPI | Result |
|---|---:|
| Denial Rate | **12.2%** |
| Clean Claim Rate | **80.8%** |
| Net Leakage | **$376.5M** |
| Average Days in AR | **32 days** |
| Claims Analyzed | **465,435** |

> These are simulated portfolio results, not real business outcomes.

## Dashboard Views

### 1. Executive Summary

Leadership-level monitoring of:

- Denial Rate
- Net Leakage
- Clean Claim Rate
- Average Days in AR
- Denial-rate trend by time
- Net leakage by denial reason
- Payer and department filters

### 2. Payer Drilldown

Moves from payer-level performance into provider-level detail using:

- Denial Rate by payer
- Total Claims
- Net Leakage
- Provider-level breakdown
- Department filtering

### 3. Claim-Level Detail

Supports investigation using:

- Claim ID
- Procedure Code
- Claim Amount
- Claim Status
- Denial Reason Code

This creates an analytical path from **KPI → payer/provider → individual claim**.

### 4. Provider Risk

Segments providers into:

- Low Risk
- Moderate Risk
- High Risk
- Very High Risk

The view compares provider experience, denial rate, department, and claim volume. Example results include high-risk providers with denial rates above 17%.

## Analytical Approach

### Step 1 — Data Preparation

- Standardize claim status values
- Validate required fields
- Handle null and blank values
- Check duplicate claim identifiers
- Validate payer/provider/department relationships
- Apply business rules consistently

### Step 2 — SQL Analytics

The analytical design demonstrates:

- CTEs
- Multi-table joins
- Conditional aggregation
- Window functions
- Ranking
- Period-over-period analysis
- Pareto analysis
- Data-quality checks
- KPI-ready views

### Step 3 — Python

Python is used as an analytical workflow layer for:

- Data preparation
- Pandas-based transformations
- Exploratory data analysis
- Validation checks
- Analytical feature preparation

### Step 4 — Power BI

Validated data is transformed into decision-oriented dashboards using:

- KPI cards
- Time-series analysis
- Payer drilldowns
- Provider risk segmentation
- Claim-level tables
- Interactive filters
- DAX measures

## Business Metrics

**Denial Rate** — proportion of claims that are denied.

**Clean Claim Rate** — proportion of claims processed without denial-related issues.

**Net Leakage** — simulated financial exposure associated with claims requiring further action.

**Average Days in AR** — operational view of reimbursement cycle time.

**Provider Risk** — risk segmentation based on provider denial performance and claim volume.

## Key Analytical Insights

- Denial performance varies across payers, making payer-level monitoring important.
- Denial reasons can be prioritized by financial contribution rather than count alone.
- Provider risk segmentation helps identify high-risk outliers for deeper investigation.
- Claim-level drilldown provides traceability from aggregate KPIs to individual records.
- Combining denial rate with claim volume and financial exposure gives a stronger prioritization framework than using a single KPI.

Denial categories represented in the dashboard include **Duplicate Claim, Eligibility Expired, Non-Covered Service, Coding Mismatch, Prior Authorization, Medical Necessity, Timely Filing, and Documentation-related issues**.

## Business Recommendations Framework

| Finding | Potential Business Action |
|---|---|
| High prior-authorization denials | Strengthen authorization validation before submission |
| Coding-related denials | Target coding-quality review and training |
| Documentation-related denials | Improve documentation completeness checks |
| High-risk providers | Perform provider-level root-cause analysis |
| Payer-specific denial spikes | Review payer rules and submission requirements |
| High-value denied claims | Prioritize recoverability and appeal analysis |

Because the dataset is synthetic, these are recommendations demonstrated by the analytical framework and **not claimed real-world savings**.

## Data Quality & Validation

Data quality is treated as part of the analytical solution.

Checks include:

- Duplicate detection
- Missing-value analysis
- Status consistency
- Payer/provider relationship validation
- Numeric validation of claim amounts
- Denial-reason consistency
- Aggregate reconciliation between claim-level and dashboard totals

## SQL Portfolio Example

```sql
-- Example: payer-level denial rate
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

Other interview-relevant patterns covered by the analytical design include CTEs, `RANK()`, `DENSE_RANK()`, `LAG()`, conditional aggregation, running totals, Pareto analysis, and data-quality validation.

## Power BI Design

The report follows a management-reporting pattern:

**Executive KPI → Trend → Driver Analysis → Segment Drilldown → Claim-Level Investigation**

This allows a stakeholder to move from:

**What is happening? → Where is it happening? → Which records should we investigate?**

## Portfolio Architecture

```text
Synthetic Claims Data
        │
        ▼
Data Cleaning & Validation
        │
        ├──────────────► Python / Pandas
        │
        ▼
SQL Analytical Layer
        │
        ├── KPI calculations
        ├── Payer analysis
        ├── Provider analysis
        ├── Denial-driver analysis
        └── Data-quality checks
        │
        ▼
Power BI Reporting Layer
        │
        ├── Executive Summary
        ├── Payer Drilldown
        ├── Claim Detail
        └── Provider Risk
        │
        ▼
Business Insights & Recommendations
```

## Technology Stack

| Category | Tools |
|---|---|
| BI | Power BI Desktop |
| Querying | SQL |
| Programming | Python, Pandas |
| Analytics | KPI analysis, EDA, trend analysis, Pareto analysis, risk segmentation |
| Data Quality | Validation, reconciliation, duplicate/null checks |
| Business Analysis | Root-cause analysis, prioritization, decision support |

## Interview Talking Points

### Data Analyst

> I started with claim-level data, established data-quality and business-rule checks, calculated core KPIs in the analytical layer, and designed Power BI views that allow stakeholders to move from executive metrics into payer, provider, and claim-level analysis.

### SQL

> I used joins, CTEs, conditional aggregation, window functions, ranking, trend analysis and reconciliation checks to create reliable analytical outputs.

### Power BI

> Different stakeholders need different levels of detail. Executives need KPIs and trends, managers need payer/provider comparisons, and analysts need claim-level records for investigation.

### Business Analysis

> For a high-denial provider, I would segment denials by reason, payer, department and financial impact, identify the dominant drivers, and then recommend a targeted operational intervention.

## Repository Scope

This repository focuses on the **analytical methodology, dashboard design, business requirements, metrics, SQL approach, and portfolio documentation**. Underlying datasets or executable notebooks/scripts should only be published when they are synthetic and safe to share.

This keeps the portfolio useful for recruiters while avoiding exposure of real employer/client data.

## Data Disclaimer

**All healthcare data and financial figures represented in this project are synthetic and intended only for learning, portfolio demonstration, and interview discussion.**

No real patient information, confidential employer information, or production healthcare-system data is included.

## Portfolio Positioning

This project demonstrates the ability to combine:

**SQL + Python + Power BI + Data Quality + Business Analysis + Data Storytelling**

into an end-to-end analytics solution rather than presenting a dashboard as an isolated visualization exercise.
