# austrian-mmm-budget-optimizer: business case, written as of 2026-07-28
Persona: in-house marketing analyst at an Austrian mid-market advertiser (the charter names retail, e-commerce, telco, banking). Decision owned: the yearly media budget split across channels, at the same total. Cycle: yearly, with an in-year review. Sign-off: head of marketing; the CFO signs the total budget.

All values are per year, at the central media budget of €1.0M, unless stated. Inputs that are not in the charter (`docs/archive/PROJECT_CHARTER.md`, v1.0 2026-07-18) are assumptions with a range. Rate and hours come from `docs/viability/_assumptions.md`.

## Money at stake per decision cycle
| Item | Value | Unit | Source |
|---|---|---|---|
| Media budget B | 1.0M (0.2M to 5M) | EUR per year | Assumption, open question 0. The low end is the charter's "advertiser above about €200k per year media spend" (charter §1, a claim, not a market statistic). |
| Average incremental ROAS (return on ad spend) | 3 (2 to 4) | EUR revenue per EUR media | Judgement; no client data exists yet |
| Media contribution (revenue that media causes) | 3.0M (0.4M to 20M) | EUR revenue per year | B × ROAS |
| Gain from a better split, same budget | 10 % (5 % to 15 %) of media contribution | % | Judgement; no public benchmark cited |
| Contribution margin | 40 % (30 % to 50 %) | % of revenue | Judgement. Breakeven ROAS = 1 ÷ margin = 2.5 (2.0 to 3.3) |
| Profit at stake V | 120k (6k to 1.5M, all-low to all-high corners) | EUR contribution profit per year | B × ROAS × gain × margin; V ÷ B = 0.12 (0.03 to 0.30) |
| Loss if the model is wrong | −60k | EUR per year | Judgement: −0.5 × V |

## Status quo
The split comes from platform dashboards (Google Ads, Meta Ads Manager, GA4 last-click). The charter (§1) says they over-credit their own channels and cannot see offline media. Last year's split rolls forward with agency advice (assumption). Extra cost: €0. How often the split is wrong: no source; the tree below assumes it.

## Options
| Option | Cost | Time to answer | Expected value | Note |
|---|---|---|---|---|
| Do nothing | €0 | 0 | €0 (reference) | Keeps the platform-credit split |
| Buy or rent: external MMM (marketing mix model) study by a consultant, agency or SaaS vendor | €35k per year (€20k to €60k); assumption, no public price list checked | 8 to 12 weeks | €1.8k = €45.6k − €8.8k delay − €35k | Same tree as build full, but "pays off" 0.40 and "not adopted" 0.20 (judgement: vendor experience). Below €0.95M budget it loses money. |
| Build small: one open-source MMM fit (Robyn or pymc-marketing, both named in charter §2) on own weekly data, one reallocation table; no synthetic proof, no dashboard; 2 weeks | 36 h × €45 = €1.6k (16 h fit + 12 h data intake + 8 h refit) | 2 weeks | €22.0k | Tree 0.25 / 0.30 / 0.30 / 0.15 (judgement: without a known-truth test the owner trusts it less, and errors stay hidden) |
| Build full: charter scope (test on synthetic data with a known answer, fit on own data, optimiser with a breakeven rule, Power BI) | €2.3k (see Cost) | 4 weeks (3 to 8); assumption from the charter's 14-day plan | €34.2k (€0.5k to €132k) | Tree below |

## Outcome tree for "build full"
| Branch | Probability (range, source) | Value if it happens (EUR per year, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 0.35 (0.20 to 0.50); judgement. The charter rates "client data falls through" Medium (R-1) and "weak identification on 52 to 104 weeks" High (R-2). | +120k (V) | +€42.0k |
| Confirms the status quo | 0.30 (0.20 to 0.40), judgement | +12k (0.1 × V: avoided doubt, shorter budget debate; judgement) | +€3.6k |
| Built but not adopted | 0.25 (0.15 to 0.40); judgement: the owner keeps the platform numbers | 0 | €0 |
| Wrong, decision gets worse | 0.10 (0.05 to 0.15); judgement. The breakeven rule and the per-channel caps (charter: extrapolation guards) limit the loss. | −60k (−0.5 × V) | −€6.0k |
| Sum | 1.00 | | **€39.6k, EV before cost** (€5.4k to €144k) |

The tree measures value against the status quo. So €39.6k less delay and cost is the value of better information: EV with the tool minus EV without it.

## Cost
| Item | Value | Source |
|---|---|---|
| Build | 32 h (16 to 48 h) × €45/h (€35 to €60) = €1.4k (€0.6k to €2.9k) | Hours: estimate from git ±50 % (`_assumptions.md`). Rate: assumption anchored on the advertised analytics floor `floor_analytics_eur` = €50.0k per year (vintage 2026-10-18) × 1.3 ÷ 1,700 h |
| Data intake | 12 h × €45 = €0.5k | Charter M4 "agency data intake", 1.5 days, "human-heavy"; 8 h per day (assumption) |
| Run | 1 refit per year, 8 h × €45 = €0.4k per year | Judgement; open-source stack, €0 licence (a Power BI licence is not counted) |
| Delay | 4 weeks of the first year's gain: 4 ÷ 52 × €39.6k = €3.0k | Assumption |
| Total, year 1 | **€5.4k** (€2.3k cash plus €3.0k delay) | |
| High case | 132 h (charter plan 14 days × 8 h + 20 h) × €60 = €7.9k, plus 8 weeks of delay | Charter §5 effort budget |

## Result
| Measure | Value |
|---|---|
| EV(build full) | €39.6k − €5.4k = **€34.2k per year** at €1M budget (€0.5k to €132k, worst and best corners paired) · €5.0k at €0.2M · €180k at €5M |
| Payback | €2.3k ÷ (€39.6k ÷ 12) ≈ 0.7 months after the new split goes live |
| Break-even probability of "pays off" | 4.1 % at €1M (12.6 % at €0.2M, 2.4 % at €5M; other branches fixed) |
| EV(build small) | **€22.0k** |
| EV(buy or rent) | **€1.8k** |
| Budget threshold: build full beats do nothing | above **€64k** per year (central) · €1.7M (all-pessimistic: V ÷ B 0.03, "pays off" 0.20, 132 h at €60, 8 weeks) · €9k (all-optimistic) |
| Budget threshold: build full beats buy or rent | at every budget up to about €118M, so at every budget in the range. Build full also beats build small above €56k. |

## Sensitivity
| Assumption | Flip point |
|---|---|
| "Pays off" probability | Do nothing wins below 4.1 % at €1M (12.6 % at €0.2M). It falls toward 0 when the advertiser has no clean weekly spend history by channel (charter R-1, R-2). |
| Media budget × (V ÷ B) | Below €64k per year (central) do nothing. If the pessimistic inputs hold, the threshold rises to €1.7M; below it, build small first. |
| Buy against build | At €1M, buying wins only if the vendor's "pays off" probability is 0.73 or more (assumed 0.40), or if the in-house build needs more than about 770 h. |

## Verdict
**Build full.** The build costs €2k to €8k, which is 2 % to 7 % of the €120k profit at stake at €1M budget. The known-truth test adds trust over build small for about €0.7k more. Change the verdict if the advertiser cannot supply at least 52 weeks of weekly spend by channel, or if the budget is below about €64k per year (central case). In both cases, choose do nothing or build small.

## Calibration against the retrospective
Retrospective verdict (`docs/viability/austrian-mmm-budget-optimizer.md`): **worth it, finish then freeze.**

| Check | Finding (repository, after the build) |
|---|---|
| Agree? | Yes on "build". The reasons differ. The company case pays through a media decision. In the real project no advertiser data arrived, so for the money decision the "not adopted" branch took all the mass. The value came as hiring evidence (S1 8/10, S2 9/10), not as euros. |
| Size of the gain | Same-budget gain: median 15.1 % of media contribution, 10th percentile 8.8 %, 0 of 500 posterior draws lose (`reports/layer_d/decision.json`; SIMULATED, public demo data, units are not euros). This is at the top of the ex-ante range of 5 % to 15 %. |
| V ÷ B | Demo data: the gain is 0.91 revenue units per unit of weekly media spend (10th percentile 0.55). At 40 % margin, V ÷ B = 0.36 (0.22), above the ex-ante high corner of 0.30. The demo's average ROAS is about 6; do not transfer it to a real advertiser. With this value, the build-full threshold falls to about €21k (€35k at the 10th percentile). |
| Cost | The cost row uses the shared git estimate, 32 h, as the brief asks. On 2026-07-28 only the charter's 14 days was known; the high case covers it. All local refs show 15 commit days (≈ 60 h). The core model was built in one agent-assisted day (2026-09-15). Cost never decided the case. |
| What the ex-ante view missed | (1) Charter risk R-1 happened: no client data (ADR-009: the intake was never built). The persona has in-house data access; a portfolio author does not. (2) The scope cut (ADR-008, ADR-009) removed the DuckDB and dbt warehouse, so the project shows no SQL. (3) The Power BI `.pbix` became a text project plus an HTML twin (ADR-010), not yet opened in Desktop. (4) On the demo data, ridge regression beat the MMM on holdout point error (MAPE 5.1 % against 7.9 %). The tree did not price "a simpler model forecasts as well". The MMM still answers the channel-split question; the ridge model does not. |
