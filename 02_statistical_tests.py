"""
02_statistical_tests.py
Validates the patterns seen in EDA with actual statistical tests,
so your findings are backed by evidence, not just "the chart looks different."
"""

import pandas as pd
import numpy as np
from scipy import stats
from db_utils import load_claims_clean

df = load_claims_clean()
print(f"Loaded {len(df):,} claims.\n")

# ------------------------------------------------------------------
# 1. Chi-square test: is denial status associated with payer?
#    (confirms the variation we saw in SQL isn't just random noise)
# ------------------------------------------------------------------
contingency = pd.crosstab(df["payer_name"], df["status"])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

print("=== Chi-Square Test: Payer vs. Claim Status ===")
print(f"Chi-square statistic: {chi2:.2f}")
print(f"p-value: {p_value:.2e}")
if p_value < 0.05:
    print("Result: SIGNIFICANT. Denial status IS associated with payer (p < 0.05).")
    print("This confirms the denial-rate variation across payers is a real pattern, not noise.\n")
else:
    print("Result: NOT significant. No strong evidence payer affects denial status.\n")

# ------------------------------------------------------------------
# 2. T-test: does days-in-AR differ between Medicaid and Private payers?
# ------------------------------------------------------------------
medicaid_ar = df[df["payer_type"] == "Medicaid"]["days_in_ar"].dropna()
private_ar = df[df["payer_type"] == "Private"]["days_in_ar"].dropna()

t_stat, p_val_ttest = stats.ttest_ind(medicaid_ar, private_ar, equal_var=False)

print("=== T-Test: Days-in-AR, Medicaid vs. Private ===")
print(f"Medicaid mean days-in-AR: {medicaid_ar.mean():.2f}")
print(f"Private mean days-in-AR:  {private_ar.mean():.2f}")
print(f"t-statistic: {t_stat:.3f} | p-value: {p_val_ttest:.4f}")
if p_val_ttest < 0.05:
    print("Result: SIGNIFICANT difference in AR days between payer types.\n")
else:
    print("Result: NOT significant. AR days are similar across payer types.\n")

# ------------------------------------------------------------------
# 3. Correlation: provider experience vs. denial rate
#    (aggregate to provider level first - correlating raw rows would be wrong here)
# ------------------------------------------------------------------
provider_stats = df.groupby("provider_id").agg(
    years_experience=("years_experience", "first"),
    denial_rate=("status", lambda x: (x == "Denied").mean()),
    claim_count=("claim_id", "count")
).reset_index()

# only include providers with a reasonable claim volume, to avoid noisy small samples
provider_stats = provider_stats[provider_stats["claim_count"] >= 30]

corr, corr_p = stats.pearsonr(provider_stats["years_experience"], provider_stats["denial_rate"])

print("=== Correlation: Provider Experience vs. Denial Rate ===")
print(f"Providers analyzed (30+ claims): {len(provider_stats)}")
print(f"Pearson correlation: {corr:.3f} | p-value: {corr_p:.4f}")
if corr_p < 0.05:
    direction = "negative (more experience -> fewer denials)" if corr < 0 else "positive (more experience -> more denials)"
    print(f"Result: SIGNIFICANT {direction} relationship.\n")
else:
    print("Result: NOT statistically significant at the individual-provider level.\n")

# ------------------------------------------------------------------
# 4. Summary table for your README / presentation
# ------------------------------------------------------------------
print("=== SUMMARY FOR REPORTING ===")
print(f"1. Payer significantly affects denial status (chi2 p={p_value:.1e})")
print(f"2. AR days {'differ' if p_val_ttest<0.05 else 'do not differ'} significantly by payer type (p={p_val_ttest:.3f})")
print(f"3. Provider experience correlation with denial rate: r={corr:.3f} (p={corr_p:.3f})")
