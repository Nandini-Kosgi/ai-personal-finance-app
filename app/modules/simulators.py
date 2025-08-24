import numpy as np
import pandas as pd

def butterfly_effect(start_balance: float,
                     monthly_contrib: float,
                     contrib_delta_pct: float,
                     years: int,
                     annual_return: float = 0.06,
                     annual_volatility: float = 0.10,
                     seed: int = 42) -> pd.DataFrame:
    """Simulate baseline vs. adjusted monthly contributions over time.

    Uses geometric Brownian motion for market returns to illustrate
    compounding effects of small changes (\"butterfly effect\").
    """
    rng = np.random.default_rng(seed)
    months = years * 12
    mu_m = (1 + annual_return) ** (1/12) - 1
    sigma_m = annual_volatility / np.sqrt(12)

    def simulate(contrib):
        bal = start_balance
        series = []
        for m in range(months):
            shock = rng.normal(mu_m, sigma_m)
            bal = max(0.0, bal * (1 + shock) + contrib)
            series.append(bal)
        return np.array(series)

    base = simulate(monthly_contrib)
    adjusted = simulate(monthly_contrib * (1 + contrib_delta_pct/100.0))

    df = pd.DataFrame({
        "month": np.arange(1, months+1),
        "baseline": base,
        "adjusted": adjusted,
        "delta": adjusted - base
    })
    df["year"] = (df["month"] - 1) // 12 + 1
    return df

def scenario_tester(monthly_income: float,
                    monthly_expense: float,
                    emergency_fund_target: float,
                    horizon_months: int = 36,
                    job_loss_prob_month: float = 0.01,
                    med_bill_prob_month: float = 0.02,
                    med_bill_amount: float = 1500.0,
                    market_return_month_mu: float = 0.004,
                    market_return_month_sigma: float = 0.03,
                    sims: int = 2000,
                    seed: int = 7) -> dict:
    """Monte Carlo stress test. Returns probability of reaching emergency
    fund target and distribution statistics for end balances.
    """
    rng = np.random.default_rng(seed)
    end_balances = []
    successes = 0

    for _ in range(sims):
        bal = 0.0
        inc = monthly_income
        exp = monthly_expense
        for m in range(horizon_months):
            # Random market drift to emulate investment return on spare cash
            drift = rng.normal(market_return_month_mu, market_return_month_sigma)
            # Random shocks
            if rng.random() < job_loss_prob_month:
                # lose job for 3 months
                for _ in range(3):
                    bal = max(0.0, bal - exp)
                    bal *= (1 + drift)
                continue
            if rng.random() < med_bill_prob_month:
                bal = max(0.0, bal - med_bill_amount)
            # Standard month
            bal = max(0.0, (bal + inc - exp) * (1 + drift))

        end_balances.append(bal)
        if bal >= emergency_fund_target:
            successes += 1

    end_balances = np.array(end_balances)
    return {
        "success_rate": successes / sims,
        "mean_end_balance": float(end_balances.mean()),
        "p10": float(np.percentile(end_balances, 10)),
        "p50": float(np.percentile(end_balances, 50)),
        "p90": float(np.percentile(end_balances, 90)),
        "samples": end_balances[:100].tolist(),  # preview
    }
