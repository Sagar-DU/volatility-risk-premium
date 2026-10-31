"""Data download and the shared daily dataset.

Everyone on the team reads data/daily.csv, built by notebooks/01_data.ipynb.

Conventions (keep these fixed across notebooks):
- Underlying: S&P 500 index (^GSPC), the index VIX is computed on.
- Returns: daily close-to-close log returns.
- Annualization: 252 trading days for realized variance.
- VIX is quoted in percent; implied variance = (VIX / 100) ** 2.
- rv_fwd21 on day t uses returns t+1 ... t+21 (future data: a target, never a signal).
"""
import numpy as np
import pandas as pd

TRADING_DAYS = 252
HORIZON = 21  # trading days in the 30-calendar-day VIX window

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"

# Named stress episodes used across all notebooks.
EPISODES = {
    "GFC 2008":              ("2008-09-01", "2009-03-31"),
    "China deval Aug 2015":  ("2015-08-17", "2015-09-30"),
    "Volmageddon Feb 2018":  ("2018-01-29", "2018-02-28"),
    "COVID Mar 2020":        ("2020-02-19", "2020-04-30"),
    "2022 bear (contrast)":  ("2022-01-03", "2022-10-31"),
    "Yen carry Aug 2024":    ("2024-07-31", "2024-08-30"),
    "Tariff shock Apr 2025": ("2025-04-01", "2025-05-15"),
}


def _download_yahoo(ticker, start, end):
    import yfinance as yf
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if df.empty:
        raise RuntimeError(f"No data returned for {ticker}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    df.index = df.index.normalize()
    return df


def download_fred(series, start, end):
    """Download one FRED series as a float Series (percent units, as FRED publishes them)."""
    raw = pd.read_csv(FRED_URL.format(series=series), na_values=".")
    raw.columns = ["date", series]
    raw["date"] = pd.to_datetime(raw["date"])
    s = raw.set_index("date")[series].astype(float)
    return s.loc[start:end]


def download_raw(start="2004-01-01", end=None):
    """Download S&P 500 OHLC, VIX, VIX3M and the 3-month T-bill rate."""
    end = end or pd.Timestamp.today().strftime("%Y-%m-%d")
    spx = _download_yahoo("^GSPC", start, end)
    vix = _download_yahoo("^VIX", start, end)["Close"]
    vix3m = _download_yahoo("^VIX3M", start, end)["Close"]  # history starts Dec 2007
    dtb3 = download_fred("DTB3", start, end)

    df = pd.DataFrame({
        "spx_open": spx["Open"],
        "spx_high": spx["High"],
        "spx_low": spx["Low"],
        "spx_close": spx["Close"],
    })
    df["vix"] = vix.reindex(df.index)
    df["vix3m"] = vix3m.reindex(df.index)
    df["rf"] = (dtb3 / 100).reindex(df.index).ffill()
    df.index.name = "date"
    return df


def forward_sum(x, horizon=HORIZON):
    """Sum of x over the NEXT `horizon` rows: t+1 ... t+horizon (NaN where incomplete)."""
    return x[::-1].rolling(horizon, min_periods=horizon).sum()[::-1].shift(-1)


def build_daily(raw, horizon=HORIZON):
    """Add returns, realized-variance measures and the variance risk premium."""
    df = raw.copy()
    df = df.dropna(subset=["spx_close", "vix"])
    df["logret"] = np.log(df["spx_close"]).diff()
    r2 = df["logret"] ** 2

    # Implied variance from VIX (annualized, decimal units)
    df["iv_var"] = (df["vix"] / 100) ** 2

    # HAR inputs: known at the close of day t (annualized variance)
    df["rv_d"] = TRADING_DAYS * r2
    df["rv_w"] = df["rv_d"].rolling(5).mean()
    df["rv_m"] = df["rv_d"].rolling(horizon).mean()

    # Parkinson range variance (HAR input only; misses overnight gaps, so never use it for the premium)
    hl = np.log(df["spx_high"] / df["spx_low"])
    df["rv_parkinson_d"] = TRADING_DAYS * hl ** 2 / (4 * np.log(2))

    # Target: realized variance over the next 21 trading days (FUTURE data)
    df["rv_fwd21"] = (TRADING_DAYS / horizon) * forward_sum(r2, horizon)

    # Variance risk premium: short variance-swap payoff per unit of variance notional
    df["vrp"] = df["iv_var"] - df["rv_fwd21"]
    # Same thing in volatility points, easier to explain
    df["vrp_volpts"] = df["vix"] - 100 * np.sqrt(df["rv_fwd21"])

    # Term structure: VIX / VIX3M > 1 means inverted (stress)
    df["vix_ratio"] = df["vix"] / df["vix3m"]
    return df


def load_daily(path="../data/daily.csv"):
    return pd.read_csv(path, index_col="date", parse_dates=True)


def episode_mask(index, name):
    start, end = EPISODES[name]
    return (index >= start) & (index <= end)
