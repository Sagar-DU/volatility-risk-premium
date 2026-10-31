"""Black-Scholes prices and Greeks (Lectures 5-6), vectorized.

S: spot, K: strike, T: years to expiry, r: risk-free rate, sigma: volatility,
q: dividend yield (S&P 500 is roughly 1.3-2%; 0 by default, note it as a limitation).
"""
import numpy as np
from scipy.stats import norm


def _d1_d2(S, K, T, r, sigma, q=0.0):
    S, K, T, sigma = map(np.asarray, (S, K, T, sigma))
    vol_sqrt_t = sigma * np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / vol_sqrt_t
    return d1, d1 - vol_sqrt_t


def call_price(S, K, T, r, sigma, q=0.0):
    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def put_price(S, K, T, r, sigma, q=0.0):
    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)


def straddle_price(S, K, T, r, sigma, q=0.0):
    return call_price(S, K, T, r, sigma, q) + put_price(S, K, T, r, sigma, q)


def straddle_delta(S, K, T, r, sigma, q=0.0):
    """Delta of a long straddle = call delta + put delta = e^{-qT} (2 N(d1) - 1)."""
    d1, _ = _d1_d2(S, K, T, r, sigma, q)
    return np.exp(-q * T) * (2 * norm.cdf(d1) - 1)


def straddle_gamma(S, K, T, r, sigma, q=0.0):
    """Gamma of a long straddle = 2 x call gamma."""
    d1, _ = _d1_d2(S, K, T, r, sigma, q)
    return 2 * np.exp(-q * T) * norm.pdf(d1) / (np.asarray(S) * sigma * np.sqrt(T))


def straddle_vega(S, K, T, r, sigma, q=0.0):
    """Vega of a long straddle per 1.00 change in sigma (divide by 100 for per vol point)."""
    d1, _ = _d1_d2(S, K, T, r, sigma, q)
    return 2 * np.asarray(S) * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
