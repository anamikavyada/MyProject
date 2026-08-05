"""
03_segmentation.py
Segments providers into risk groups using KMeans, based on denial rate,
claim volume, and experience - so RCM leadership can target training
at specific provider clusters instead of treating everyone the same.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
from db_utils import load_claims_clean

sns.set_theme(style="whitegrid")
os.makedirs("outputs", exist_ok=True)

df = load_claims_clean()
print(f"Loaded {len(df):,} claims.\n")

# ------------------------------------------------------------------
# 1. Build provider-level feature table
# ------------------------------------------------------------------
provider_features = df.groupby("provider_id").agg(
    denial_rate=("status", lambda x: (x == "Denied").mean()),
    avg_claim_amount=("claim_amount", "mean"),
    claim_volume=("claim_id", "count"),
    years_experience=("years_experience", "first"),
    department=("department", "first"),
).reset_index()

# only include providers with enough volume for a meaningful denial rate
provider_features = provider_features[provider_features["claim_volume"] >= 30].copy()
print(f"Providers included in segmentation: {len(provider_features)}")

# ------------------------------------------------------------------
# 2. Scale features and run KMeans
# ------------------------------------------------------------------
features = ["denial_rate", "claim_volume", "years_experience"]
X = provider_features[features]
X_scaled = StandardScaler().fit_transform(X)

# Elbow method to justify choice of k (saved as a chart, not just picked blindly)
inertias = []
k_range = range(2, 8)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(7, 5))
plt.plot(list(k_range), inertias, marker="o")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method for Choosing k")
plt.tight_layout()
plt.savefig("outputs/06_elbow_method.png", dpi=150)
plt.close()
print("Saved: 06_elbow_method.png (use this to justify your k choice)")

# k=4 chosen: low/medium/high/very-high risk is a natural, explainable split
K = 4
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
provider_features["cluster"] = kmeans.fit_predict(X_scaled)

# ------------------------------------------------------------------
# 3. Label clusters by risk level (based on mean denial rate per cluster)
# ------------------------------------------------------------------
cluster_summary = provider_features.groupby("cluster").agg(
    avg_denial_rate=("denial_rate", "mean"),
    avg_volume=("claim_volume", "mean"),
    avg_experience=("years_experience", "mean"),
    provider_count=("provider_id", "count"),
).sort_values("avg_denial_rate")

risk_labels = ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"]
cluster_summary["risk_label"] = risk_labels[:len(cluster_summary)]
label_map = dict(zip(cluster_summary.index, cluster_summary["risk_label"]))
provider_features["risk_label"] = provider_features["cluster"].map(label_map)

print("\n=== Cluster Summary ===")
print(cluster_summary)

# ------------------------------------------------------------------
# 4. Visualize clusters
# ------------------------------------------------------------------
plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=provider_features, x="years_experience", y="denial_rate",
    hue="risk_label", size="claim_volume", sizes=(20, 200), palette="Set2"
)
plt.title("Provider Risk Segments: Experience vs. Denial Rate")
plt.xlabel("Years of Experience")
plt.ylabel("Denial Rate")
plt.tight_layout()
plt.savefig("outputs/07_provider_segments.png", dpi=150)
plt.close()
print("Saved: 07_provider_segments.png")

# ------------------------------------------------------------------
# 5. Save the segmented table for use in Power BI / reporting
# ------------------------------------------------------------------
provider_features.to_csv("outputs/provider_risk_segments.csv", index=False)
print("Saved: outputs/provider_risk_segments.csv (import this into Power BI if useful)")

high_risk_count = (provider_features["risk_label"] == "Very High Risk").sum()
print(f"\n{high_risk_count} providers flagged as Very High Risk - candidates for targeted training.")
