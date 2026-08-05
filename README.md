# Healthcare Claims Denial & Revenue Leakage Analytics

**SQL | Python | Power BI | Data Quality | Revenue Cycle Analytics | Business Intelligence**

> A portfolio analytics project simulating a healthcare payer/provider claims environment to identify denial drivers, quantify revenue leakage, assess provider/payer risk, and translate claim-level data into actionable business recommendations.

---

## Executive Summary

Healthcare claims denials can delay reimbursement, increase accounts receivable, and create preventable revenue leakage. This project approaches the problem from a **Data Analyst / BI Analyst perspective**: build a structured claims analytics pipeline, validate business rules, identify the major drivers of denials, and present the findings through an executive Power BI dashboard.

The dashboard covers **465,435 claims** across a simulated 2021–2025 period and provides analysis by payer, provider, department, denial reason, claim status, and risk tier.

### Executive KPIs

| KPI | Result |
|---|---:|
| Denial Rate | **12.2%** |
| Clean Claim Rate | **80.8%** |
| Net Leakage | **$376.5M** |
| Average Days in AR | **32 days** |
| Claims analyzed | **465,435** |

These figures are from the portfolio dashboard and are based on **synthetic data**; they do not represent a real healthcare organization.

---

## Business Problem

Revenue Cycle Management teams need to answer questions such as:

- Which payers have the highest denial rates?
- Which denial reasons contribute most to financial leakage?
- Which providers or departments show unusually high denial rates?
- Where are operational or documentation issues creating preventable denials?
- Which areas should receive remediation, training, or payer-level attention first?
- How can claim-level data be converted into an executive view of financial and operational risk?

The project is designed to move beyond descriptive reporting toward **root-cause analysis and decision support**.

---

## Key Business Questions

1. Which denial reasons drive the largest share of net leakage?
2. How does denial performance vary across payers?
3. Which providers and departments have elevated denial rates?
4. Are high-denial providers concentrated in particular risk tiers?
5. What does claim status and denial reason reveal at claim level?
6. How can denial trends and operational metrics support targeted corrective action?

---

## Dashboard

The Power BI solution is organized around four analytical views:

### 1. Executive Summary

Provides an executive-level view of:

- Denial Rate
- Net Leakage
- Clean Claim Rate
- Average Days in AR
- Denial-rate trend over time
- Net leakage by denial reason
- Payer and date filters
- Department-level filtering

### 2. Payer Drilldown

Analyzes payer performance using:

- Denial Rate by payer
- Total Claims
- Net Leakage
- Provider-level drilldown
- Department filtering

### 3. Claim-Level Detail

Provides a detailed view of individual claims including:

- Claim ID
- Procedure Code
- Claim Amount
- Cleaned Claim Status
- Denial Reason Code

This layer supports investigation from aggregate KPI → business segment → individual claim.

### 4. Provider Risk

Highlights providers with elevated denial rates and classifies them into risk tiers such as:

- Low Risk
- Moderate Risk
- High Risk
- Very High Risk

The view compares provider experience with denial performance and claim volume to support targeted investigation.

---

## Analytical Findings

The dashboard demonstrates several important analytical patterns:

- Denial performance can vary materially across payers, making payer-level analysis important rather than relying only on provider-level averages.
- A relatively small set of denial reasons can account for a significant share of financial leakage, making **Pareto-style prioritization** useful for remediation.
- Providers with elevated denial rates can be surfaced through risk segmentation rather than treating all providers equally.
- Claim-level drilldown enables users to trace an executive KPI back to individual denied claims and their associated denial reasons.

The project blueprint also frames potential actions around prior-authorization processes, coding accuracy, documentation quality, and payer performance.

---

## Data & Modeling Approach

The project uses **synthetic, business-realistic healthcare claims data**. The data is intentionally simulated so that no real patient, provider, payer, or healthcare-system information is exposed.

The analytical design follows a relational / star-schema-oriented approach with claims as the central fact and supporting business dimensions such as:

- Payer
- Provider
- Department
- Date
- Denial Reason
- Procedure / Claim attributes

The project emphasizes data engineering and analytical practices including:

- Data cleaning
- Deduplication
- Status standardization
- Null handling
- Referential-integrity checks
- Business-rule validation
- Aggregation and KPI calculation
- SQL-based analytical transformations
- Power BI semantic modeling and visualization

---

## SQL Analytics

The project is designed to demonstrate interview-relevant SQL patterns including:

- CTEs for staged transformations
- Multi-table joins
- Aggregations and KPI calculations
- Window functions such as `RANK`, `DENSE_RANK`, `LAG`, and `LEAD`
- Running totals and trend analysis
- Pareto analysis
- Data-quality checks
- Views for BI consumption
- Stored-procedure-oriented processing
- Query-performance considerations

Example analytical use cases include payer denial-rate ranking, provider risk identification, denial-reason contribution analysis, and claim-level validation.

---

## Python Analytics

Python is used as part of the portfolio solution for data preparation and analytical workflow development. The project blueprint includes synthetic-data generation, preprocessing, validation, exploratory analysis, and analytical extensions such as provider-risk scoring / forecasting.

The intended workflow is:

**Raw / synthetic data → Cleaning & validation → Analytical transformations → SQL / semantic model → Power BI → Business recommendations**

---

## Power BI

The dashboard focuses on **decision-oriented BI rather than a generic visualization exercise**.

Key design principles include:

- KPI-first executive reporting
- Interactive payer / department / date filtering
- Drilldown from summary to detail
- Risk segmentation
- Trend analysis
- Financial-impact visualization
- Claim-level investigation
- Business recommendations based on analytical findings

The dashboard was designed with executive and manager-level consumption in mind.

---

## Business Impact Framework

Because the dataset is synthetic, the project does **not** claim real-world financial savings or operational improvements.

Instead, it demonstrates how an analyst could translate findings into actions such as:

- Prioritizing high-impact denial reasons
- Improving prior-authorization workflows
- Targeting coding/documentation training
- Investigating high-risk provider groups
- Reviewing payer-specific denial patterns
- Focusing appeal effort on potentially recoverable claims

This distinction is intentional: the project demonstrates **analytical reasoning and decision support without presenting simulated results as real client outcomes**.

---

## Tech Stack

| Area | Tools / Techniques |
|---|---|
| Data Analysis | Python, Pandas, EDA |
| Data Engineering | SQL, data cleaning, validation, transformations |
| Database | Relational / star-schema design |
| BI | Power BI Desktop |
| Analytics | KPI analysis, trend analysis, Pareto analysis, risk segmentation |
| Business Analysis | Root-cause analysis, stakeholder questions, recommendations |

---

## Repository Structure

A recommended structure for the project is:

```text
MyProject/
├── data/
│   └── synthetic claims datasets
├── sql/
│   ├── data_quality/
│   ├── transformations/
│   ├── analytical_queries/
│   └── views/
├── python/
│   ├── data_generation/
│   ├── preprocessing/
│   └── analysis/
├── powerbi/
│   └── dashboard / screenshots
├── docs/
│   └── project documentation
└── README.md
```

Actual files may differ from this logical structure depending on the current repository contents.

---

## Interview Talking Points

This project can be discussed in interviews from four angles:

### Data Analyst

How did you identify the major denial drivers and convert claim-level data into actionable KPIs?

### SQL

How did you structure joins, CTEs, window functions, aggregations, and data-quality checks?

### Power BI

Why did you choose KPI cards, trend analysis, payer drilldowns, and provider-risk segmentation?

### Business / Consulting

If a Revenue Cycle Manager asked where to focus first, how would you prioritize denial reasons, payers, providers, and departments based on financial impact and denial volume?

---

## Important Note on Data

**All healthcare data in this portfolio project is synthetic and created for learning, demonstration, and interview purposes.**

It does not contain real patient information, real claims, or confidential employer/client data.

---

## Portfolio Focus

This project demonstrates the ability to combine:

**SQL + Python + Power BI + Data Quality + Business Analysis + Storytelling**

into an end-to-end analytics solution rather than presenting a dashboard as an isolated visualization exercise.
