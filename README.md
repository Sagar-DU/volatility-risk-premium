# Is Selling S&P 500 Volatility a Free Lunch?

*Erdős Institute Quant Finance Boot Camp, Fall 2026 · Nahid Hasan Sagar, Kevin Specht

Option prices usually imply more volatility than actually follows, so selling volatility tends to earn a premium. This project asks four questions:

1. How large is that **variance risk premium** for the S&P 500, and is it statistically real?
2. What happens to sellers in volatility shocks (2008, Feb 2018, Mar 2020, Aug 2024, Apr 2025)?
3. Can a simple, real-time forecast tell you when the premium is worth collecting?
4. Does the premium survive when you actually sell options and delta hedge them?

## Headline results
*(fill in when done)*

## Repository
| Path | What it does | Owner |
|---|---|---|
| `notebooks/01_data.ipynb` | Downloads data and builds `data/daily.csv` | Nahid |
| `notebooks/02_premium.ipynb` | Measures the premium; Newey–West tests; payoff shape; episode table | Nahid |
| `notebooks/03_har_forecast.ipynb` | HAR-RV forecast, forecast premium, trading rule fixed in advance | Nahid |
| `notebooks/04_straddle_backtest.ipynb` | Delta-hedged short straddle, P&L attribution, rule applied | Kevin |
| `src/data.py` | Data download, conventions, episode dates | |
| `src/bs.py` | Black–Scholes prices and Greeks | |
| `tests/` | Sanity checks (`python -m pytest -q`) | |
| `docs/` | Executive summary and slides | both |

## How to run
```bash
pip install -r requirements.txt
python -m pytest -q          # 4 checks should pass
jupyter lab                  # run the notebooks in order: 01 → 04
```
Data sources, all free: Yahoo Finance (`^GSPC`, `^VIX`, `^VIX3M`) and FRED (`DTB3`).

## Conventions
- **Underlying:** the S&P 500 index (^GSPC), the index VIX is computed on.
- **Returns:** close-to-close log returns.
- **Realized variance:** annualized ×252, measured over the next 21 trading days.
- **Implied variance:** (VIX/100)². VIX covers 30 calendar days.
- **Premium:** `vrp = VIX²/10000 − RV(next 21 days)`. This equals the payoff of a short variance swap per unit of notional.

## Trading rule (fixed before testing on 2016 onwards)
*Nahid: write the exact rule here and commit it **before** running notebook 03, section 4. Example:*
> Hold a short-volatility position on day t only if yesterday's forecast premium (VIX² minus the HAR forecast) is positive and yesterday's VIX/VIX3M is below 1.

## Trading rule (fixed on 4 Nov 2026, before running the 2016+ test)
Sell one month of variance on day t only if, at the previous close,
(1) the forecast premium VIX²/10000 − HAR forecast is positive, and
(2) VIX/VIX3M < 1 (the VIX curve is not inverted).
Otherwise hold cash. Nothing is tuned. Train 2008–2015, test 2016+, run once.

## Limitations
*(fill in)*

Starting points:
- VIX is not the same as at-the-money implied vol: put skew pushes VIX higher, which is why notebook 04 uses haircuts.
- There are only a few independent tail events in the test period.
- Costs are simplified.
- Dividends are ignored in Black–Scholes.
