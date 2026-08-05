"""
MedNova Health Network - Synthetic Claims Dataset Generator
Generates a realistic, deliberately-messy relational dataset for the
Claims Denial & Revenue Leakage Analytics portfolio project.

Output: CSV files in ./output_data/ ready to load into SQLite/Postgres.
"""

import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

OUT_DIR = "output_data"
os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1. DIM_DATE (5 years)
# ----------------------------------------------------------------------
start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 12, 31)
dates = pd.date_range(start_date, end_date, freq="D")

dim_date = pd.DataFrame({
    "date_key": dates.strftime("%Y%m%d").astype(int),
    "date": dates,
    "day": dates.day,
    "week": dates.isocalendar().week,
    "month": dates.month,
    "quarter": dates.quarter,
    "fiscal_year": dates.year,
    "is_holiday": np.random.choice([0, 1], size=len(dates), p=[0.97, 0.03])
})
dim_date.to_csv(f"{OUT_DIR}/dim_date.csv", index=False)
print(f"dim_date: {len(dim_date)} rows")

# ----------------------------------------------------------------------
# 2. DIM_PAYERS (15) - each with an inherent denial-strictness bias
# ----------------------------------------------------------------------
payer_names = [
    "Medicare", "Medicaid", "BlueShield Regional", "UnitedCare Plus",
    "Aetnix Health", "Cigna Bridge", "Humana Direct", "Oxford Freedom",
    "Anthem Prime", "Kaiser Connect", "MetroHealth Plan", "Liberty Mutual Health",
    "Guardian Care Network", "Premier PPO", "National Health Alliance"
]
payer_types = ["Medicare", "Medicaid"] + ["Private"] * 13

dim_payers = pd.DataFrame({
    "payer_id": range(1, 16),
    "payer_name": payer_names,
    "payer_type": payer_types,
    # each payer has a baseline denial strictness (drives realistic variation)
    "denial_strictness": np.round(np.random.uniform(0.05, 0.22, size=15), 3),
    "avg_processing_days": np.random.randint(10, 45, size=15)
})
dim_payers.to_csv(f"{OUT_DIR}/dim_payers.csv", index=False)
print(f"dim_payers: {len(dim_payers)} rows")

# ----------------------------------------------------------------------
# 3. DIM_PROVIDERS (800) - experience affects error-driven denial risk
# ----------------------------------------------------------------------
departments = ["Cardiology", "Orthopedics", "Oncology", "Radiology", "General Surgery",
               "Neurology", "Pediatrics", "Emergency Medicine", "Internal Medicine", "Obstetrics"]
hospitals = [f"MedNova Hospital {i}" for i in range(1, 13)]

n_providers = 800
dim_providers = pd.DataFrame({
    "provider_id": range(1, n_providers + 1),
    "provider_name": [fake.name() for _ in range(n_providers)],
    "department": np.random.choice(departments, n_providers),
    "hospital_id": np.random.randint(1, 13, n_providers),
    "years_experience": np.random.randint(1, 35, n_providers)
})
dim_providers.to_csv(f"{OUT_DIR}/dim_providers.csv", index=False)
print(f"dim_providers: {len(dim_providers)} rows")

# ----------------------------------------------------------------------
# 4. DIM_PROCEDURES (1200) - CPT-style codes with realistic cost tiers
# ----------------------------------------------------------------------
n_procedures = 1200
proc_categories = {
    "Diagnostic Imaging": (150, 2500),
    "Lab Test": (20, 400),
    "Surgery - Minor": (800, 6000),
    "Surgery - Major": (5000, 45000),
    "Consultation": (75, 350),
    "Physical Therapy": (60, 300),
    "Emergency Visit": (200, 3500),
    "Chemotherapy Session": (1200, 9000)
}
cat_names = list(proc_categories.keys())
chosen_cats = np.random.choice(cat_names, n_procedures)
costs = [round(np.random.uniform(*proc_categories[c]), 2) for c in chosen_cats]

dim_procedures = pd.DataFrame({
    "procedure_code": [f"CPT{10000+i}" for i in range(n_procedures)],
    "procedure_name": [f"{c} Procedure {i}" for i, c in enumerate(chosen_cats)],
    "department": np.random.choice(departments, n_procedures),
    "category": chosen_cats,
    "standard_cost": costs
})
dim_procedures.to_csv(f"{OUT_DIR}/dim_procedures.csv", index=False)
print(f"dim_procedures: {len(dim_procedures)} rows")

# ----------------------------------------------------------------------
# 5. DIM_PATIENTS (60,000)
# ----------------------------------------------------------------------
n_patients = 60000
insurance_choices = dim_payers["payer_id"].values
regions = ["North", "South", "East", "West", "Central"]

dim_patients = pd.DataFrame({
    "patient_id": range(1, n_patients + 1),
    "age": np.clip(np.random.normal(48, 20, n_patients).astype(int), 0, 99),
    "gender": np.random.choice(["M", "F", "Other"], n_patients, p=[0.48, 0.48, 0.04]),
    "region": np.random.choice(regions, n_patients),
    "primary_payer_id": np.random.choice(insurance_choices, n_patients),
    "enrollment_date": [fake.date_between(start_date="-5y", end_date="today") for _ in range(n_patients)]
})
dim_patients.to_csv(f"{OUT_DIR}/dim_patients.csv", index=False)
print(f"dim_patients: {len(dim_patients)} rows")

# ----------------------------------------------------------------------
# 6. FACT_CLAIMS (450,000+) - the core table, with business logic + messiness
# ----------------------------------------------------------------------
n_claims = 460000

denial_reasons = [
    "Prior Authorization Missing", "Eligibility Expired", "Coding Mismatch",
    "Duplicate Claim", "Documentation Incomplete", "Non-Covered Service",
    "Timely Filing Limit Exceeded", "Medical Necessity Not Established"
]

claim_ids = np.arange(1, n_claims + 1)
patient_ids = np.random.choice(dim_patients["patient_id"], n_claims)
provider_ids = np.random.choice(dim_providers["provider_id"], n_claims)
procedure_idx = np.random.choice(dim_procedures.index, n_claims)
procedure_codes = dim_procedures.loc[procedure_idx, "procedure_code"].values
base_costs = dim_procedures.loc[procedure_idx, "standard_cost"].values

# map patient -> payer for consistency, with occasional secondary payer (10%)
patient_payer_map = dim_patients.set_index("patient_id")["primary_payer_id"]
payer_ids = patient_payer_map.loc[patient_ids].values.copy()
random_payer_swap = np.random.rand(n_claims) < 0.10
payer_ids[random_payer_swap] = np.random.choice(dim_payers["payer_id"], random_payer_swap.sum())

# provider -> department/experience for denial-risk modeling
prov_exp_map = dim_providers.set_index("provider_id")["years_experience"]
provider_exp = prov_exp_map.loc[provider_ids].values
payer_strictness_map = dim_payers.set_index("payer_id")["denial_strictness"]
payer_strictness = payer_strictness_map.loc[payer_ids].values

# claim amount = base cost +/- variance, occasional wild outliers (data entry errors)
claim_amount = base_costs * np.random.uniform(0.85, 1.25, n_claims)
outlier_mask = np.random.rand(n_claims) < 0.004
claim_amount[outlier_mask] = claim_amount[outlier_mask] * np.random.uniform(50, 100, outlier_mask.sum())
claim_amount = np.round(claim_amount, 2)

# submission dates spread across 3 years, processing lag 5-60 days
submit_dates = [fake.date_between(start_date="-3y", end_date="today") for _ in range(n_claims)]
processing_lag = np.random.randint(5, 60, n_claims)
process_dates = [pd.Timestamp(d) + timedelta(days=int(lag)) for d, lag in zip(submit_dates, processing_lag)]

# denial probability = payer strictness - small experience discount, capped
experience_discount = np.clip(provider_exp / 35 * 0.05, 0, 0.05)
denial_prob = np.clip(payer_strictness - experience_discount + np.random.normal(0, 0.02, n_claims), 0.02, 0.35)
is_denied = np.random.rand(n_claims) < denial_prob

status = np.where(is_denied, "Denied", np.where(np.random.rand(n_claims) < 0.08, "Partial", "Paid"))

paid_amount = np.where(
    status == "Paid", claim_amount,
    np.where(status == "Partial", claim_amount * np.random.uniform(0.3, 0.8, n_claims), 0.0)
)
paid_amount = np.round(paid_amount, 2)

denial_reason_code = np.where(
    status == "Denied",
    np.random.choice(denial_reasons, n_claims),
    None
)

days_in_ar = np.array([(pd - pd0).days if isinstance(pd0, (datetime,)) else lag
                        for pd, pd0, lag in zip(process_dates, submit_dates, processing_lag)])

fact_claims = pd.DataFrame({
    "claim_id": claim_ids,
    "patient_id": patient_ids,
    "provider_id": provider_ids,
    "payer_id": payer_ids,
    "procedure_code": procedure_codes,
    "date_submitted": submit_dates,
    "date_processed": process_dates,
    "claim_amount": claim_amount,
    "paid_amount": paid_amount,
    "status": status,
    "denial_reason_code": denial_reason_code,
    "days_in_ar": processing_lag
})

# ---- INJECT REALISTIC MESSINESS ----

# a) inconsistent status casing/whitespace (~5% of rows)
messy_status_mask = np.random.rand(len(fact_claims)) < 0.05
messy_variants = {"Denied": ["DENIED", "denied ", "Denied "], "Paid": ["PAID", "paid", "Paid "],
                   "Partial": ["PARTIAL", "partial "]}
def messy_status(s):
    variants = messy_variants.get(s, [s])
    return random.choice(variants)
fact_claims.loc[messy_status_mask, "status"] = fact_claims.loc[messy_status_mask, "status"].apply(messy_status)

# b) missing denial_reason_code on ~4% of denied claims
denied_mask = fact_claims["status"].str.strip().str.lower() == "denied"
missing_reason_mask = denied_mask & (np.random.rand(len(fact_claims)) < 0.04)
fact_claims.loc[missing_reason_mask, "denial_reason_code"] = None

# c) duplicate claim submissions (~1.5%)
dup_sample = fact_claims.sample(frac=0.015, random_state=42).copy()
dup_sample["claim_id"] = dup_sample["claim_id"] + n_claims  # new IDs, same claim details
fact_claims = pd.concat([fact_claims, dup_sample], ignore_index=True)

# d) a handful of orphan provider_ids (simulate sync lag, ~0.3%)
orphan_mask = np.random.rand(len(fact_claims)) < 0.003
fact_claims.loc[orphan_mask, "provider_id"] = fact_claims["provider_id"].max() + np.random.randint(1, 500, orphan_mask.sum())

# e) a few date logic errors: date_processed before date_submitted (~0.2%)
bad_date_mask = np.random.rand(len(fact_claims)) < 0.002
fact_claims.loc[bad_date_mask, "date_processed"] = pd.to_datetime(fact_claims.loc[bad_date_mask, "date_submitted"]) - timedelta(days=5)

fact_claims = fact_claims.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle
fact_claims.to_csv(f"{OUT_DIR}/fact_claims.csv", index=False)
print(f"fact_claims: {len(fact_claims)} rows")

# ----------------------------------------------------------------------
# 7. FACT_DENIAL_APPEALS (~40,000, sampled from denied claims)
# ----------------------------------------------------------------------
denied_claims = fact_claims[fact_claims["status"].str.strip().str.lower() == "denied"]
n_appeals = min(40000, int(len(denied_claims) * 0.6))
appeal_sample = denied_claims.sample(n=n_appeals, random_state=42)

appeal_dates = [
    pd.to_datetime(d) + timedelta(days=int(np.random.randint(5, 90)))
    for d in appeal_sample["date_processed"]
]
appeal_outcome = np.random.choice(["Approved", "Denied Again", "Partially Approved"],
                                   n_appeals, p=[0.45, 0.35, 0.20])
recovered_amount = np.where(
    appeal_outcome == "Approved", appeal_sample["claim_amount"],
    np.where(appeal_outcome == "Partially Approved", appeal_sample["claim_amount"] * np.random.uniform(0.3, 0.7, n_appeals), 0.0)
)

fact_denial_appeals = pd.DataFrame({
    "appeal_id": range(1, n_appeals + 1),
    "claim_id": appeal_sample["claim_id"].values,
    "appeal_date": appeal_dates,
    "appeal_outcome": appeal_outcome,
    "recovered_amount": np.round(recovered_amount, 2)
})
fact_denial_appeals.to_csv(f"{OUT_DIR}/fact_denial_appeals.csv", index=False)
print(f"fact_denial_appeals: {len(fact_denial_appeals)} rows")

print("\nAll tables generated in ./output_data/")
print("Total fact_claims rows (incl. duplicates injected):", len(fact_claims))
