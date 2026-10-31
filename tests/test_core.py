"""Sanity checks. Run from the repo root with: python -m pytest -q"""
import numpy as np
import pandas as pd

from src import bs
from src.data import forward_sum, build_daily


def test_forward_sum_alignment():
    x = pd.Series(np.arange(10, dtype=float))
    f = forward_sum(x, horizon=3)
    assert f.iloc[0] == 1 + 2 + 3  # uses t+1..t+3, not t..t+2
    assert np.isnan(f.iloc[7])     # incomplete window at the end


def test_put_call_parity():
    S, K, T, r, s = 100.0, 95.0, 0.25, 0.04, 0.2
    lhs = bs.call_price(S, K, T, r, s) - bs.put_price(S, K, T, r, s)
    assert abs(lhs - (S - K * np.exp(-r * T))) < 1e-10


def test_straddle_greeks_match_finite_differences():
    S, K, T, r, s, h = 100.0, 100.0, 30 / 365, 0.04, 0.2, 1e-3
    p = lambda x: bs.straddle_price(x, K, T, r, s)
    assert abs(bs.straddle_delta(S, K, T, r, s) - (p(S + h) - p(S - h)) / (2 * h)) < 1e-6
    assert abs(bs.straddle_gamma(S, K, T, r, s) - (p(S + h) - 2 * p(S) + p(S - h)) / h ** 2) < 1e-4
    v = lambda sig: bs.straddle_price(S, K, T, r, sig)
    assert abs(bs.straddle_vega(S, K, T, r, s) - (v(s + h) - v(s - h)) / (2 * h)) < 1e-5


def test_build_daily_on_simulated_prices():
    rng = np.random.default_rng(0)
    n = 300
    idx = pd.bdate_range("2020-01-01", periods=n)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    raw = pd.DataFrame({"spx_open": close, "spx_high": close * 1.005, "spx_low": close * 0.995,
                        "spx_close": close, "vix": 16.0, "vix3m": 18.0, "rf": 0.04}, index=idx)
    df = build_daily(raw)
    r2 = df["logret"] ** 2
    t = 50
    assert np.isclose(df["rv_fwd21"].iloc[t], 252 / 21 * r2.iloc[t + 1:t + 22].sum())
    assert np.isclose(df["vrp"].iloc[t], 0.16 ** 2 - df["rv_fwd21"].iloc[t])
    # daily vol 1% -> annualized variance about 252 * 0.0001 = 0.0252
    assert 0.015 < df["rv_fwd21"].mean() < 0.035
