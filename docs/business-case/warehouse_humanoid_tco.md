# warehouse_humanoid_tco: business case, written as of 2026-05-14
Persona: automation or operations analyst at a Styrian warehouse operator or integrator (KNAPP-type). Decision owned: crew mix for one picking cell (one 4-port AutoStore station, 1 shift, 120 orders per hour): workers only, workers + robot carts (AMR), or humanoids. Cycle: once per cell per capex round (assumption: yearly). Sign-off: COO or site director; the works council (Betriebsrat) has a say on changes that affect workers.

All values are per cell, 5-year present value at 8 % discount and 2.5 % yearly wage growth, unless stated. The inputs are public figures that the first commit stores in `config/` (WKO collective-agreement wage estimate, Unitree price estimates). The arithmetic is mine, from those inputs.

## Money at stake per decision cycle
| Item | Value | Unit | Source |
|---|---|---|---|
| One worker | 50,350 per year · 0.211M over 5 years | EUR | €18.50/h × 1.35 overhead × 8 h × 252 days; first-commit config |
| Today's crew of 8 workers | 1.68M | EUR, 5 years | 8 × €0.211M; crew size 8 from first-commit config |
| One robot cart (AMR) | 0.081M | EUR, 5 years | €65k + 6 % upkeep per year; config |
| One humanoid | 0.166M, plus 0.2M integration per cell (0.1M to 0.4M) | EUR, 5 years | €120k (€80k to €200k) + €8k install + 8 % upkeep per year; config |
| Humanoid break-even speed | 1.27 × the worker's time per pick, before integration and supervision | ratio | €0.211M ÷ €0.166M |
| Humanoid swap, 8 units | 1.22M | EUR capex | 8 × €128k + €200k |
| Cells in scope | 1 to 4 | cells | assumption, open question 0 |

## Status quo
The site takes vendor quotes and a payback spreadsheet. Humanoid speed comes from vendor demos, not from measured data (first-commit charter, problem statement). Cost: some analyst days per quote round (assumption). How often the choice goes wrong: no source; the tree assumes 10 %.

## Options
| Option | Cost | Time to answer | Expected value per cell | Note |
|---|---|---|---|---|
| Do nothing | €0 | 0 | €0 (reference) | Keeps 8 workers. Open to a humanoid pilot that rests on vendor demos. |
| Buy or rent (integrator or consultant study) | €10k to €30k (assumption, no public benchmark) | 4 to 8 weeks | ≈ €68k (90 % of €100k − €20k − €2.3k delay) | An integrator that sells robots has a stake in the answer. |
| Build small: cost spreadsheet + check of public robot demo data, 2 weeks | 25 h (20 to 30 h) × €45 = €1.1k | 2 weeks | €88k | Assumption: captures 90 % (80 to 95 %) of the full build's value |
| Build full: data extraction, event simulation, 5-year cost model with Monte Carlo, dashboard | €8.4k (see Cost) | 8 to 10 weeks part-time (charter plan) | €92k (−€28k to +€239k) | See the tree |

## Outcome tree for "build full"
| Branch | Probability (range, source) | Value if it happens (EUR per cell, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off (2 to 4 workers move to robot carts) | 0.25 (0.15 to 0.40), judgement: humanoid offers are new and untested | 0.39M (0.26M to 0.52M): 2 to 4 × net €0.130M per swap (€0.211M − €0.081M), if one cart does one worker's job (assumption) | €97.5k |
| Confirms the status quo | 0.45 (0.40 to 0.45), judgement | 0.05M (0.02M to 0.10M): avoided humanoid pilot, about 2 units + part of integration | €22.5k |
| Built but not adopted | 0.20 (0.15 to 0.25), judgement: the model has no site telemetry | 0 | €0 |
| Wrong, decision gets worse | 0.10 (0.05 to 0.15), first-commit charter rates "dataset proves insufficient" as Medium likelihood | −0.20M (−0.10M to −0.40M): integration and capex lost on a bad robot choice | −€20.0k |
| Sum | 1.00 | | **€100k, EV before cost** (−€12k to +€243k) |

The tree measures value against the status quo. So €100k is also the value of better information: EV with the tool minus EV without it.

## Cost
| Item | Value | Source |
|---|---|---|
| Build | 80 h (40 to 120 h) × €45/h (€35 to €60) = €3.6k (€1.4k to €7.2k) | Hours: estimate from git ±50 % (`docs/viability/_assumptions.md`); the plan said 8 to 10 weeks part-time. Rate: assumption anchored on the advertised analytics floor `floor_analytics_eur` = €50.0k per year (vintage 2026-10-18) × 1.3 ÷ 1,700 h |
| Upkeep | 8 h per year × €45 = €360 per year, €1.8k over 5 years | judgement; CI on a free public tier, €0 run cost (assumption) |
| Delay | €3.0k: the decision waits 8 weeks × €78k saving per year × 0.25 | branch 1 value ÷ 5 years |
| Total | **€8.4k** (€4.0k to €16.0k) | |

## Result
| Measure | Value |
|---|---|
| EV(build full) | €100k − €8.4k = **€92k per cell** (−€28k to +€239k; worst and best cases paired) |
| Payback | €8.4k ÷ (€100k ÷ 5 years) ≈ 5 months after the decision |
| Break-even probability of "pays off" | 1.5 % (other branches fixed; the rest moves to "not adopted") |
| EV(build small) | €90k − €1.9k (build + 2-week delay) = **€88k** |
| EV(build small first, then full only on a close call) | **€96k**. Close-call probability 0.30 (0.20 to 0.50, judgement). Assumption: full's extra €10k comes in close calls. Extra cost of the full stage: €6.5k. |

## Sensitivity
| Assumption | Flip point |
|---|---|
| Humanoid time per pick versus the worker's | Break-even 1.27 ×. If public demo data put the humanoid far above it (more than 1.6 ×), the small model settles the case and the full build adds nothing. Within ±25 % of 1.27 ×, the full build pays. |
| Cells in scope (N) | Small-first wins while s × (1 − c) × N × €100k < €4.6k (s = share of full's extra value outside close calls, c = small's capture share 0.9). At 1 cell this holds for s below 45 %. At 4 cells it holds only for s below 11 %: then build full. |
| "Pays off" probability | Do nothing wins only below 1.5 %. |

## Verdict
**Build small first.** The spreadsheet and the demo-data check give the answer 6 weeks sooner, at about a quarter of the cost. Build full only if the small model shows a close call on humanoid speed, or if 4 or more cells are in scope.

## Calibration against the retrospective
Retrospective verdict (`docs/viability/warehouse_humanoid_tco.md`): **worth it, finish then freeze.**

| Check | Finding (repository, after the build) |
|---|---|
| Agree? | Partly. The two pages answer different questions. The company needed only the small build. The portfolio got its value (scarcity, domain angle, interview story) from the full build. |
| Spreadsheet accuracy | Ex-ante 8-worker crew €1.68M; repository €1.726M (SIMULATED, inputs CALIBRATED): +2.5 %. The small model was close. |
| Close call? | No. The lean mix wins 99.8 % of 10,000 Monte Carlo draws. EVPI (expected value of perfect information) ≈ €0 for all six sampled inputs: no sampled uncertainty changes the choice (`reports/sensitivity_analysis_report.json`). The full build added confidence, not a different decision. |
| Size of the payoff | Lean mix (1 worker + 3 robot carts) €0.453M vs 3-worker crew €0.647M: gap €0.19M per cell over 5 years (SIMULATED). This is below the ex-ante range of €0.26M to €0.52M. Against the 8-worker crew the gap is €1.27M, but the README labels that crew overstaffed. |
| What the ex-ante view missed | (1) The main lever was crew sizing (8 to 3 workers), not technology. (2) Humanoid price was not the binding constraint: no all-humanoid price from €10k to €500k reaches parity with the lean mix (README, `breakeven_thresholds`). (3) The README names unfilled vacancies, not wages, as the real driver; the tree valued wages only. (4) About 55 h beyond the 25 h small build went to simulation and governance (140 files). The company view prices that at about €2.5k with no decision value. |
