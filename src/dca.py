import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, r2_score

####################
# Decline models
####################

def hyperbolic_decline(t, qi, D, b):
    return qi / ((1 + b * D * t) ** (1 / b))

def exponential_decline(t, qi, D):
    return qi * np.exp(-D * t)

####################
# Fit models
####################

def fit_decline_model(t, q):
    results = {}
    try:
        params_exp, _ = curve_fit(
            exponential_decline,
            t,
            q,
            maxfev = 10000
        )

        qi_exp, D_exp = params_exp    
        q_exp = exponential_decline(t, qi_exp, D_exp)
        rmse_exp = np.sqrt(mean_squared_error(q, q_exp))
        r2_exp = r2_score(q, q_exp)

    except RuntimeError:
        params_exp = [np.nan, np.nan]
        q_exp = np.full_like(q, np.nan)
        rmse_exp = np.inf
        r2_exp = -np.inf

    try:
        params_hyp, _ = curve_fit(
            hyperbolic_decline,
            t,
            q,
            bounds = (0, [100, 1, 2]),
            maxfev = 20000
        )
        qi_h, D_h, b_h = params_hyp
        q_hyp = hyperbolic_decline(t, qi_h, D_h, b_h)
        rmse_hyp = np.sqrt(mean_squared_error(q, q_hyp))
        r2_hyp = r2_score(q, q_hyp)
    
    except RuntimeError:
        params_hyp = [np.nan, np.nan, np.nan]
        q_hyp = np.full_like(q, np.nan)
        rmse_hyp = np.inf
        r2_hyp = -np.inf

    if rmse_exp < rmse_hyp:
        best_model = "Exponential"
        best_params = params_exp
        q_best = q_exp
    else:
        best_model = "Hyperbolic"
        best_params = params_hyp
        q_best = q_hyp

    return {
        "model": best_model,
        "params": best_params,
        "q_exp": q_exp,
        "q_hyp": q_hyp,
        "q_best": q_best,
        "rmse_exp": rmse_exp,
        "rmse_hyp": rmse_hyp,
        "r2_exp": r2_exp,
        "r2_hyp": r2_hyp
    }    

####################
# Forecast
####################        

def forecast_production(t, q, fit_results, future_days = 365 * 2):
    model = fit_results["model"]
    params = fit_results["params"]

    t_future = np.arange(len(q) + future_days)

    if model == "Exponential":
        qi, D = params
        q_future = exponential_decline(t_future, qi, D)
    else:
        qi, D, b = params
        q_future = hyperbolic_decline(t_future, qi, D, b)

    q_forecast = q_future[-future_days:]

    return {
        "t_future": t_future,
        "q_full": q_future,
        "q_forecast": q_forecast
    }

####################
# Metrics
####################  

def calculate_cumulative(q, dt = 1):
    return np.sum(q * dt)

def calculate_eur(q_hist, q_forecast, dt = 1):
    cumulative = calculate_cumulative(q_hist, dt)
    future = calculate_cumulative(q_forecast, dt)
    return cumulative + future

def economic_limit_analysis(q_forecast, threshold):
    below_idx = np.where(q_forecast < threshold)[0]

    if len(below_idx) > 0:
        return below_idx[0]
    return None

def calculate_revenue(q, oil_price):
    revenue = q * oil_price
    return revenue.sum()




