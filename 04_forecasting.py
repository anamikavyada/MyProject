"""
04_forecasting.py
Forecasts next-quarter denial volume using a simple, explainable time
series model (Holt-Winters exponential smoothing via statsmodels).
Deliberately avoids black-box models - for a metric like denial volume,
stakeholders need to trust and understand the forecast.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os
from db_utils import load_claims_clean

sns.set_theme(style="whitegrid")
os.makedirs("outputs", exist_ok=True)

df = load_claims_clean()
print(f"Loaded {len(df):,} claims.\n")

# ------------------------------------------------------------------
# 1. Build a monthly denial volume time series
# ------------------------------------------------------------------
denied = df[df["status"] == "Denied"].copy()
denied["month"] = denied["date_submitted"].dt.to_period("M")

monthly_denials = denied.groupby("month").size()
monthly_denials.index = monthly_denials.index.to_timestamp()
monthly_denials = monthly_denials.sort_index()

# drop the most recent partial month if data collection cuts off mid-month
# (uncomment if your last month looks artificially low)
# monthly_denials = monthly_denials.iloc[:-1]

print(f"Monthly denial series: {len(monthly_denials)} months")
print(monthly_denials.tail(6))

# ------------------------------------------------------------------
# 2. Fit Holt-Winters model and forecast next 3 months (next quarter)
# ------------------------------------------------------------------
model = ExponentialSmoothing(
    monthly_denials,
    trend="add",
    seasonal="add",
    seasonal_periods=12
).fit()

forecast_horizon = 3
forecast = model.forecast(forecast_horizon)

print("\n=== Next-Quarter Denial Volume Forecast ===")
print(forecast)

# ------------------------------------------------------------------
# 3. Plot history + forecast
# ------------------------------------------------------------------
plt.figure(figsize=(11, 6))
plt.plot(monthly_denials.index, monthly_denials.values, label="Historical Denials", color="#4C72B0")
plt.plot(forecast.index, forecast.values, label="Forecast (Next Quarter)", color="#C44E52", linestyle="--", marker="o")
plt.title("Monthly Denial Volume: Historical + Forecast")
plt.xlabel("Month")
plt.ylabel("Number of Denied Claims")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/08_denial_forecast.png", dpi=150)
plt.close()
print("\nSaved: 08_denial_forecast.png")

# ------------------------------------------------------------------
# 4. Simple business framing for the presentation
# ------------------------------------------------------------------
avg_recent = monthly_denials.tail(6).mean()
avg_forecast = forecast.mean()
pct_change = (avg_forecast - avg_recent) / avg_recent * 100

print(f"\nAvg monthly denials (last 6 months): {avg_recent:.0f}")
print(f"Avg monthly denials (forecast, next quarter): {avg_forecast:.0f}")
print(f"Projected change: {pct_change:+.1f}%")
