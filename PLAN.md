# Team Plan: Nahid and Kevin

**Today:** Sat Oct 31
**Finish everything by:** Wed Nov 4
**Official deadline:** Fri Nov 6 (Nov 5–6 are buffer)

## Who owns what
| | Nahid | Kevin |
|---|---|---|
| **Builds** | Data file (`01`), premium measurement and tests (`02`), HAR forecast and trading rule (`03`) | Delta-hedged short straddle backtest and P&L attribution (`04`) |
| **Writes** | Executive summary findings 1–3, README results | Executive summary finding 4, limitations |
| **Presents** | Video slides 1–5 | Video slides 6–8 |
| **Reviews** | Kevin's notebook: look-ahead bias, units | Nahid's notebooks: does the story read clearly? |

Not in scope for Nov 6: the VaR add-on and GARCH. Do them only if both of you finish early.

## Lectures: what to watch, and what each is for
| Lecture | Nahid | Kevin | What you need it for |
|---|---|---|---|
| 1 · Probability | done | if not done: skim | Expectations and variance; the basis for everything |
| 2 · Monte Carlo | skip | **Sat** (only the simulation part) | Kevin's GBM sanity check in `04` section 0 |
| 3 · Bonds and rates | skip | skim the discounting part | Interest on the hedge cash account (`rf`) |
| 4 · Stock paths / GBM | **Sat** | **Sat** | Log returns and annualizing variance (×252, √t). Nahid uses this on day 1; Kevin needs it for simulated paths. |
| 5 · Black–Scholes | **Sun** evening | **Sat** (needed first) | Pricing the straddle. Nahid needs it to understand what VIX measures and to explain Kevin's part. |
| 6 · Greeks | **Mon** evening | **Sun** morning | Delta = the hedge; gamma and theta = the P&L attribution and the reason the premium exists |
| Delta hedging (if posted) | Tue | **Sun–Mon** | Kevin's core method. If it isn't posted yet, Lecture 6 plus `04` section 0 cover it. |
| GARCH / stochastic vol / market making | after Nov 6 | after Nov 6 | Not needed for this submission |

## Day by day

### Sat Oct 31
**Both, a 30-minute call:**
- Agree on this plan.
- Nahid creates the GitHub repo, uploads the starter files and adds Kevin as a collaborator.
- Both run `python -m pytest -q`; 4 checks should pass.

**Nahid:**
- Run `01_data` and commit `data/daily.csv`, so Kevin has the same data.
- Watch Lecture 4.
- Start `02`: the plot and the Newey–West test.

**Kevin:**
- Watch Lectures 5, 4, and the simulation part of 2.
- Start `04` section 0: the GBM sanity check.

### Sun Nov 1
**Nahid:**
- Finish `02`: tests, payoff shape and the episode table.
- Evening: Lecture 5.

**Kevin:**
- Lecture 6 in the morning.
- Finish the sanity check.
- Write the monthly backtest loop (`04` section 1) for one haircut.

**End-of-day checkpoint (message each other):**
- Nahid: is the premium significant, and how big is it?
- Kevin: does the backtest run over 2005 onwards?

### Mon Nov 2
**Nahid:**
- `03`: expanding-window HAR forecasts and the QLIKE/MSE comparison.
- **Write the trading rule in the README and commit it before testing.**
- Evening: Lecture 6.

**Kevin:**
- All haircuts, plus costs.
- P&L attribution (`04` section 2).
- Delta-hedging lecture if it's posted.

### Tue Nov 3
**Nahid:**
- Run the rule once on 2016 onwards and build the episode-by-episode results.
- Add `signal` to `daily.csv` and commit it.

**Kevin:**
- Results tables and charts (`04` section 3).
- Apply Nahid's signal (`04` section 4).

**Both, evening:**
- Draft your executive summary sections (outline in `docs/`).
- Build 8 slides.

### Wed Nov 4
**Both:**
- Restart and run all notebooks, top to bottom.
- Finish the README results and limitations.
- Final executive summary (PDF in `docs/`).
- Record the 5–8 minute video.
- **Submit.**

### Thu Nov 5 – Fri Nov 6
Buffer. Fix anything broken and resubmit if needed; the latest submission counts.

## If you fall behind
Cut in this order:
1. Nahid's trading rule: keep the HAR forecast comparison only.
2. Kevin's haircut grid: use one haircut of 1 vol point.
3. Kevin's cost model.

**Never cut:**
- the premium test with Newey–West
- the episode table
- the basic hedged-straddle P&L

## Rules for working together
- Pull before you start, and commit small and often.
- Each person edits only their own notebooks, which avoids merge conflicts.
- Only `01_data` writes `daily.csv`, with one exception: Nahid's `03` adds the signal columns on Tue.
- Use AI for downloads, plotting and boilerplate. Write the statistics, the hedging logic and the attribution yourselves, and make sure you can explain every line.

## Open item
The project PDF says teams of 3–5. Ask the organizers to confirm in writing that a team of 2 is OK.
