"""
01_eda.py
Exploratory Data Analysis: distributions, missingness, outliers.
Saves charts as PNG files to ./outputs/ so you can drop them straight
into your README or presentation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from db_utils import load_claims_clean

sns.set_theme(style="whitegrid")
os.makedirs("outputs", exist_ok=True)

print("Loading data from SQL Server...")
df = load_claims_clean()
print(f"Loaded {len(df):,} claims.\n")

# ------------------------------------------------------------------
# 1. Status distribution
# ------------------------------------------------------------------
plt.figure(figsize=(7, 5))
df["status"].value_counts().plot(kind="bar", color="#4C72B0")
plt.title("Claim Status Distribution")
plt.ylabel("Number of Claims")
plt.tight_layout()
plt.savefig("outputs/01_status_distribution.png", dpi=150)
plt.close()
print("Saved: 01_status_distribution.png")

# ------------------------------------------------------------------
# 2. Claim amount distribution (log scale, since outliers skew it hard)
# ------------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.histplot(df["claim_amount"], bins=60, log_scale=True, color="#55A868")
plt.title("Claim Amount Distribution (log scale)")
plt.xlabel("Claim Amount ($, log scale)")
plt.tight_layout()
plt.savefig("outputs/02_claim_amount_distribution.png", dpi=150)
plt.close()
print("Saved: 02_claim_amount_distribution.png")

# ------------------------------------------------------------------
# 3. Missingness overview
# ------------------------------------------------------------------
missing = df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)
print("\nMissing values by column:")
print(missing)

if len(missing) > 0:
    plt.figure(figsize=(7, 4))
    missing.plot(kind="barh", color="#C44E52")
    plt.title("Missing Values by Column")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig("outputs/03_missingness.png", dpi=150)
    plt.close()
    print("Saved: 03_missingness.png")

# ------------------------------------------------------------------
# 4. Denial rate by payer (bar chart version of your SQL query D2)
# ------------------------------------------------------------------
denial_by_payer = (
    df.groupby("payer_name")["status"]
    .apply(lambda x: (x == "Denied").mean())
    .sort_values(ascending=False)
)
plt.figure(figsize=(9, 6))
denial_by_payer.plot(kind="barh", color="#DD8452")
plt.title("Denial Rate by Payer")
plt.xlabel("Denial Rate")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/04_denial_rate_by_payer.png", dpi=150)
plt.close()
print("Saved: 04_denial_rate_by_payer.png")

# ------------------------------------------------------------------
# 5. Pareto chart: denial reasons by dollar amount (the classic 80/20 view)
# ------------------------------------------------------------------
denied = df[df["status"] == "Denied"].copy()
reason_totals = denied.groupby("denial_reason_code")["claim_amount"].sum().sort_values(ascending=False)
cum_pct = reason_totals.cumsum() / reason_totals.sum() * 100

fig, ax1 = plt.subplots(figsize=(10, 6))
reason_totals.plot(kind="bar", ax=ax1, color="#4C72B0")
ax1.set_ylabel("Total Denied $ Amount")
ax1.set_xticklabels(reason_totals.index, rotation=45, ha="right")

ax2 = ax1.twinx()
ax2.plot(range(len(cum_pct)), cum_pct.values, color="red", marker="o")
ax2.set_ylabel("Cumulative %")
ax2.set_ylim(0, 110)

plt.title("Pareto Chart: Denial Reasons by Dollar Impact")
plt.tight_layout()
plt.savefig("outputs/05_denial_reason_pareto.png", dpi=150)
plt.close()
print("Saved: 05_denial_reason_pareto.png")

# ------------------------------------------------------------------
# 6. Outlier detection (z-score method, matches your SQL check)
# ------------------------------------------------------------------
mean, std = df["claim_amount"].mean(), df["claim_amount"].std()
outliers = df[df["claim_amount"] > mean + 5 * std]
print(f"\nOutlier claims (>5 std dev above mean): {len(outliers)}")
print(f"Mean claim amount: ${mean:,.2f} | Std dev: ${std:,.2f}")
if len(outliers) > 0:
    print(f"Largest outlier: ${outliers['claim_amount'].max():,.2f}")

print("\nEDA complete. Charts saved to ./outputs/")
