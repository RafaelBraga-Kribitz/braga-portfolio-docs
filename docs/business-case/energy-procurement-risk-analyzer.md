# energy-procurement-risk-analyzer: business case, written as of 2026-07-12

Persona: energy buyer or controller at a Styrian metal-processing manufacturer that uses about 50 GWh of electricity per year. Decision owned: the procurement strategy for the next 12 months (full spot, index-linked, fixed annual, or a fixed share of 30, 50 or 70 %). Cycle: yearly; the fixed price locks in the second half of the prior year. Sign-off: CFO.

Rates and hours: `docs/viability/_assumptions.md`. Prices: ENTSO-E Austrian day-ahead annual means, public before this date (VERIFIED; values as in the repository's `reports/NUMERIC_SSOT.md`). Arithmetic uses a flat load and energy only (no grid fees, taxes or levies).

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Volume | 50,000 | MWh per year | Reference consumer (planning input, CALIBRATED) |
| Energy spend, calm year | 4.95 | EUR M per year | 50,000 MWh × €98.94/MWh (2025 mean) |
| Energy spend, crisis year | 13.07 | EUR M per year | 50,000 MWh × €261.40/MWh (2022 mean) |
| Exposure swing, unhedged, one year | 7.73 | EUR M | 2021 → 2022 rise in the annual mean (€106.85 → €261.40/MWh) × 50,000 MWh |
| Fixed-price premium (supplier margin) | 0.25 (0 to 0.50) | EUR M per year | Assumption: €5/MWh (0 to 10) × 50,000 MWh; judgement |
| Premium-to-exposure ratio | ≈ 3 % (0 to 6.5 %) | share | Row 5 ÷ row 4. The tail is large next to the premium, so the decision is material. This ratio alone does not value the information. |
| Yearly gap, fixed vs spot (crude) | 0.87 to 7.96; mean 4.26 | EUR M per year, 2021 to 2025 | Fixed price proxied by the prior-year mean vs the spot mean, × 50,000 MWh |

## Status quo

| Item | Value | Source |
|---|---|---|
| How it is decided | Gut feeling or the supplier's offer | Planning claim; judgement, no survey |
| Analysis cost | about €0 per year | Assumption |
| How often it goes wrong | The crude fixed price beat spot in 3 of 5 years (2021, 2022, 2025). It lost in 2023 and 2024. No strategy wins every year. | Row 7 above |
| What is unknown | The tail cost (P95) of each strategy, and the price of a lower tail | Nothing today measures it |

## Options

Two buyer objectives, stated before the build. **(a) Cost-minimising:** minimise the expected 12-month cost; P95 does not count. **(b) Tail-limited:** the P95 annual cost must not exceed a cap X, and the buyer pays up to *w* euros of expected premium per euro of P95 reduction (assumption: *w* = 1.0, range 0.5 to 2.0). The objective is unknown today; the CFO states it.

| Option | Cost (year 1) | Time to answer | Expected value per cycle | Note |
|---|---|---|---|---|
| Do nothing | €0 | none | €0 (baseline) | The status-quo error stays |
| Buy or rent (energy consultant or supplier portfolio service) | €10k to €30k per year (assumption, judgement; no public benchmark found) | 2 to 6 weeks | +€0.04 M (a) to +€0.06 M (b); range −€0.09 M to +€0.30 M | Same tree as build full, minus the fee. A supplier is not neutral. |
| Build small: 2-week spreadsheet. Monthly index and spot prices × 50 GWh flat load, four strategies, past years as the risk view. | 20 h (10 to 30) × €45 = €900, plus €270 per year upkeep | 2 weeks | +€0.057 M for (a) and (b) (−€0.07 M to +€0.21 M) | Answers the expected-cost choice. Gives no P95 per fixed share, so it cannot serve buyer (b). |
| Build full: pipeline, warehouse, hourly load profile, bootstrap P95 per strategy | 60 h (30 to 90) × €45 = €2,700, plus €540 per year upkeep | 4 to 6 weeks (assumption) | (a) +€0.055 M (−€0.07 M to +€0.21 M) · (b) +€0.080 M (−€0.07 M to +€0.31 M) | For (a), the same choice as small at a higher cost. For (b), it adds the P95 per fixed share. |

## Outcome tree for "build full"

Values per 12-month cycle. "Pays off" = expected-cost gain A, €0.30 M (€0.08 M to €0.50 M; cash, expected), plus, for buyer (b) only, a sizing gain B = max(0, *w* × ΔP95 − premium). With ΔP95 €0.2 M (€0.1 M to €0.5 M) and a premium of €0.1 M (€0.05 M to €0.25 M) for a higher fixed share (assumptions, judgement), B = €0.10 M at *w* = 1 (€0 at 0.5, €0.30 M at 2.0). B is risk-adjusted value, not a cash saving. The tree shows buyer (b) at *w* = 1; for buyer (a), the first branch is worth €0.30 M.

| Branch | Probability (range, source) | Value if it happens (EUR, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 25 % (10 to 40 %; judgement, from the status-quo claim) | +€0.40 M (€0.10 M to €0.75 M): A + B; A = an expected-cost gap of €2 to €15/MWh × 50,000 MWh; assumption | +€0.100 M |
| Confirms the status quo | 40 % (25 to 55 %; judgement) | +€0.02 M (€0.01 M to €0.03 M): one external review avoided; assumption | +€0.008 M |
| Built but not adopted | 25 % (15 to 40 %; judgement) | €0 | €0 |
| Wrong, decision gets worse | 10 % (5 to 15 %; judgement: constructed load, index as a proxy for offers) | −€0.25 M (−€0.10 M to −€0.50 M): a wrong hedge share pays the premium for nothing; premium range | −€0.025 M |
| Sum | 100 % | | **+€0.083 M EV before cost (b); +€0.058 M (a)** |

## Cost

| Item | Value | Source |
|---|---|---|
| Build | 60 h (30 to 90 h) × €45/h (€35 to €60) = €2,700 (€1,050 to €5,400), one-off | Hours: estimate from git ±50 %. Rate: `_assumptions.md`, anchored on the advertised analytics floor `floor_analytics_eur` €50.0k per year (vintage 2026-10-18). |
| Run | about €0 per year | Assumption: local DuckDB and free CI minutes |
| Upkeep | 1 h per month × €45 = €540 per year (€420 to €720) | Assumption |
| Delay | €0 if the answer comes before the lock window (second half of the year) | Assumption: 4 to 6 weeks to answer |
| Total, year 1 | €3,240 (€1,470 to €6,120) | Sum |

## Result

| Measure | Buyer (a), cost-minimising | Buyer (b), tail-limited, *w* = 1.0 |
|---|---|---|
| Value of better information (gross, per cycle) | A only: 25 % × €0.30 M = €0.075 M (cash, expected) | A + B: 25 % × €0.40 M = €0.100 M, of which €0.025 M is risk-adjusted |
| EV(build full) | +€0.055 M (−€0.07 M to +€0.21 M) | +€0.080 M (−€0.07 M to +€0.31 M) |
| EV(build small) | +€0.057 M (−€0.07 M to +€0.21 M) | +€0.057 M; it cannot size the hedge |
| Better build | Small, by the €2,070 extra cost of full | Full, by €0.023 M |
| Break-even probability of "pays off" (full) | 7 % | 5 % |
| Payback (full) | Inside the first cycle | Inside the first cycle (year-1 cost is 3.9 % of the gross EV) |
| Small first, then ask the CFO for the objective, X and *w* | About the better build for each buyer, for the cost of one question. Both builds fit before the lock window. | Same |

## Sensitivity

| Assumption | Assumed | Flips at | Effect |
|---|---|---|---|
| Buyer objective | Unknown; tail-limited with 50 % (30 to 70 %; judgement) | (a) or (b) | Cost-minimising: the full build never beats small. Tail-limited: see the next row. |
| Willingness to pay *w*, € of premium per € of P95 reduction (buyer b) | 1.0 (0.5 to 2.0; assumption), with ΔP95 €0.2 M and premium €0.1 M | *w* ≈ 0.54 | Below 0.54, 25 % × B is less than the €2,070 extra cost: build small. Above it, build full. Threshold = (premium + €8.3k) ÷ ΔP95. |
| Probability that the tool changes the decision and pays off | 25 % (10 to 40 %) | 7 % (a, full), 5 % (b, full), 6 % (small) | Below these values, do nothing |
| Build hours | 60 h | about 520 extra hours for buyer (b) (€0.023 M ÷ €45/h) | Not a practical flip |

## Verdict

**Build small first.** The spreadsheet fully serves a cost-minimising buyer. The full build pays its extra cost only for a buyer with a P95 limit who pays more than about €0.54 of premium per euro of P95 reduction. Ask the CFO for the objective, the cap X and *w* before the full build; a stated cap or a *w* above about 0.54 justifies the full build at once. The verdict is unchanged; its reason is now the buyer's stated objective, not a premium ratio.

## Calibration against the retrospective

| Item | Ex-ante view | What the repository later showed (`reports/NUMERIC_SSOT.md`, run 2026-10-28) |
|---|---|---|
| Retrospective verdict | (none) | Worth it, finish then freeze (`docs/viability/energy-procurement-risk-analyzer.md`) |
| Agree? | Partly | The pages answer different questions. Buyer (a): a spreadsheet gives the same choice. Buyer (b): only the full build gives the P95 table that decides. For hiring evidence, the full build was worth it. Both say: do not extend now. |
| Hedge trade-off | Premium €0.1 M for ΔP95 €0.2 M; flip at *w* ≈ 0.54 | Hybrid 70 % vs Fixed annual: premium €0.176 M for €0.171 M less P95 (both SIMULATED). Break-even *w* = 1.03. |
| Meaning for buyer (a) | P95 does not count | Fixed annual has the lowest mean, €4.77 M (SIMULATED). The P95 result does not change the choice. |
| Meaning for buyer (b) | Depends on *w* and X | Buy Hybrid 70 % only if *w* ≥ 1.03, or if the cap X is at least €6.44 M but below €6.61 M (P95, SIMULATED; only Hybrid 70 % meets such a cap). At *w* below 1.03, stay at Fixed annual. That answer is a decision, not zero information. |
| Premium-to-exposure ratio | ≈ 3 % | €0.176 M ÷ P95 €6.44 M (Hybrid 70 %, SIMULATED) = 2.7 % |
| Expected-cost gain A (leave full spot) | €0.30 M per year (€0.08 M to €0.50 M) | Mean next 12 months: spot €5.36 M vs Fixed annual €4.77 M, a gap of €0.59 M (SIMULATED). Past 5 years: €34.61 M vs €30.17 M, or €0.89 M per year (CALIBRATED). Above the assumed range. |
| Crude spreadsheet vs full engine | 5 × €4.26 M = €21.3 M | Wrong-strategy cost €27.04 M, 2021 to 2025 (CALIBRATED). The spreadsheet came within 21 %. A flat load gives €24.96 M, so the hourly shape adds 8 %. |
| Time to answer | 4 to 6 weeks | First commit 2026-07-19; first real-data result 2026-10-28, after about 14 weeks (101 days). A price-series fix (keep only the SDAC day-ahead series) came on the last day. |
| What the ex-ante view missed | | (1) Gain A was about twice the assumption, and a spreadsheet answers it. (2) The first draft did not state the buyer's risk objective. The hedge choice turns on *w* (break-even 1.03) or the cap X; the CFO sets them, not the model. (3) The real return was portfolio evidence (SQL, dbt, data quality, Power BI, Azure-ready); the persona view cannot see it. (4) The plan file's figures (€6.99 M, €0.12 M, €25.62 M) come from the unmerged branch `gsd/v1.0-milestone` (window 2021 to 2024). Do not quote them. |
