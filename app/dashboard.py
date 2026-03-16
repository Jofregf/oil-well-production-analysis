import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# Load data
# -----------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

data_path = BASE_DIR / "data" / "processed" / "oil_well_clean.csv"

df = pd.read_csv(
    data_path,
    index_col="date",
    parse_dates=True
)

oil = df["oil_volume"]

t = np.arange(len(oil))
q = oil.values

# -----------------------------
# Models
# -----------------------------

def exp_decline(t, qi, D):
    return qi * np.exp(-D * t)

def hyperbolic_decline(t, qi, D, b):
    return qi / ((1 + b * D * t) ** (1 / b))

# -----------------------------
# Fit models
# -----------------------------

params_exp, _ = curve_fit(exp_decline, t, q, maxfev=10000)
qi_exp, D_exp = params_exp

params_hyp, _ = curve_fit(
    hyperbolic_decline,
    t,
    q,
    bounds=(0, [100, 1, 2]),
    maxfev=10000
)

qi_h, D_h, b_h = params_hyp

# -----------------------------
# Sidebar controls
# -----------------------------

st.sidebar.title("Forecast Settings")

model_choice = st.sidebar.selectbox(
    "Decline model",
    ["Exponential", "Hyperbolic"]
)

forecast_years = st.sidebar.slider(
    "Forecast years",
    1,
    10,
    2
)

future_days = forecast_years * 365

# -----------------------------
# Forecast
# -----------------------------

t_future = np.arange(len(q) + future_days)

if model_choice == "Exponential":
    q_future = exp_decline(t_future, qi_exp, D_exp)

else:
    q_future = hyperbolic_decline(t_future, qi_h, D_h, b_h)

future_dates = pd.date_range(
    start=df.index[-1],
    periods=future_days + 1,
    freq="D"
)[1:]

# -----------------------------
# EUR calculation
# -----------------------------

historical_cum = q.sum()
future_cum = q_future[-future_days:].sum()

EUR = historical_cum + future_cum

# -----------------------------
# Plot
# -----------------------------

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(df.index, q, label="Historical Production")

ax.plot(
    future_dates,
    q_future[-future_days:],
    linestyle="--",
    label="Forecast"
)

ax.set_title("Oil Production Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Oil Volume (m3/day)")

ax.legend()

st.pyplot(fig)

# -----------------------------
# Metrics
# -----------------------------

st.metric("Historical Production (m3)", f"{historical_cum:,.0f}")
st.metric("Estimated Future Production (m3)", f"{future_cum:,.0f}")
st.metric("Estimated Ultimate Recovery EUR (m3)", f"{EUR:,.0f}")