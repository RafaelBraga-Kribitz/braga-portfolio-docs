# Viability retrospective: was each project worth building?

Date: 2026-10-28. One page per project sits in this folder. The method is in `docs/BUSINESS_ACUMEN_PLAN_2026-10-28.md`. The shared assumptions are in [`_assumptions.md`](_assumptions.md).

**Read this first.** Rafael has sent 0 applications. No conversion data exists. Every score below is a hiring-evidence score (0 to 10), not a conversion rate. Every page uses the one rubric and finish-cost rule in `_assumptions.md` ("Scoring rubric for the five hiring-evidence items"). S1 evidence comes from the published commit (gate run B, prose measures of 2026-10-28). Every hours figure is an estimate from git with a range of ±50 %, until Rafael supplies his own log. Agent-assisted repositories inflate commit counts. Market shares come from the snapshot of 2026-10-18 ("ads mention").

## Summary

Opportunity cost shows what the same hours would buy. Applications use 1 to 1.25 h each. German uses about 640 h from A1.2 to the B1 exam. Next project uses the 60 h median of the five flagships.

| Project | Hours (estimate, range) | Opportunity cost: applications · German · next project | S1 today | S2 after plan | Verdict | Lesson |
|---|---|---|---|---|---|---|
| [austria-data-job-market-intelligence](austria-data-job-market-intelligence.md) | 24 h (12 to 36) | 19 to 24 · 3.8 % · 40 % | 7 | 9 | worth it, keep | The project found SQL is the scarcest skill but shows SQL in one query. Build the next project on SQL. |
| [warehouse_humanoid_tco](warehouse_humanoid_tco.md) | 80 h (40 to 120) | 64 to 80 · 12.5 % · 133 % | 7 | 9 | worth it, finish then freeze | Cap the governance layer before the build. It grew to 140 files against 33 source files. |
| [austrian-mmm-budget-optimizer](austrian-mmm-budget-optimizer.md) | 32 h (16 to 48) | 26 to 32 · 5.0 % · 53 % | 8 | 9 | worth it, finish then freeze | Put the top-demand skill in the minimum scope. The SQL warehouse was the first layer cut. |
| [energy-procurement-risk-analyzer](energy-procurement-risk-analyzer.md) | 60 h (30 to 90) | 48 to 60 · 9.4 % · 100 % | 9 | 10 | worth it, finish then freeze | A decision model on real public data with one euro answer earns most evidence in about 60 h. Check what is already built before you plan an extension. |
| [decision-analytics-reconstruction](decision-analytics-reconstruction.md) | 144 h (72 to 216) | 115 to 144 · 22.5 % · 240 % | 6 | 8 | sunk, freeze with summary only | Name the decision owner and the first business number before the first commit. Cap governance at a fixed share of hours. |
| [metric_lineage_simulator](metric_lineage_simulator.md) | 24 h (12 to 36) | 19 to 24 · 3.8 % · 40 % | 7 | 9 | worth it, finish then freeze | Name a real decider and a real data source before the build. Cap the process load. |
| [NextMove](NextMove.md) | 48 h (24 to 72) | 38 to 48 · 7.5 % · 80 % | 8 | 10 | worth it, finish then freeze | Write the market-fit check and the first number before the first commit. |
| [Chart_Audit_Framework](Chart_Audit_Framework.md) | 40 h (20 to 60) | 32 to 40 · 6.3 % · 67 % | 3 | 4 | sunk, archive and unpin | Score a project by the ad vocabulary it shows and a named business user. A kit with one frozen target gives no story. |
| [funnel_correlation_py](funnel_correlation_py.md) | 24 h (12 to 36) | 19 to 24 · 3.8 % · 40 % | 5 | 6 | sunk, freeze with summary only | A port of a free tool with no named user gives no story. Cap such a project at one day. |
| [governance-bootstrap](governance-bootstrap.md) | 24 h (12 to 36) | 19 to 24 · 3.8 % · 40 % | 3 | 3 | sunk, freeze with summary only | Name the ad vocabulary and the one number a tool will produce. Five of six commit days went to presentation. |
| [brazil_presidential_election_prediction_2026](brazil_presidential_election_prediction_2026.md) | 16 h (8 to 24) | 13 to 16 · 2.5 % · 27 % | 5 | 5 | sunk, freeze with summary only | Write the persona line before the first commit. Cap a project with no Austrian persona at 8 h. |

Five sunk projects carry a proposed ten-line summary README on their page: `decision-analytics-reconstruction`, `Chart_Audit_Framework`, `funnel_correlation_py`, `governance-bootstrap` and `brazil_presidential_election_prediction_2026`. Rafael decides whether any of them replaces a README (open question 1 in the brief). Four READMEs stay unchanged until he decides: `Chart_Audit_Framework`, `funnel_correlation_py`, `governance-bootstrap` and `brazil_presidential_election_prediction_2026`. The fifth, `decision-analytics-reconstruction`, is frozen by D-034, and brief step 4 required summary-level edits, so its README was rewritten at summary level (business-acumen box, plain names, no new analysis).

## The three strongest lessons across the portfolio

1. **Write the buyer and the first number before the first commit.** Five projects with a sunk verdict (`decision-analytics-reconstruction`, `Chart_Audit_Framework`, `funnel_correlation_py`, `governance-bootstrap`, `brazil_presidential_election_prediction_2026`) started without a named decision owner, or without a business user in the Austrian target market. The worth-it flagships `energy-procurement-risk-analyzer`, `warehouse_humanoid_tco` and `austrian-mmm-budget-optimizer` each answer one money decision with one number, and each scores 9 or 10 after the plan. Rule: if the persona line names nobody in the target market, cap the project at 8 h.
2. **Cap governance and process before the build.** `warehouse_humanoid_tco` holds 140 governance files against 33 source files. About 60 % of the non-merge commits in `decision-analytics-reconstruction` are governance, audit or CI work, and that repository took 144 h, 2.4 times the median of 60 h. Five of six commit days in `governance-bootstrap` and in `funnel_correlation_py` went to presentation. Ads do not mention this work. Rule: fix a share of hours for governance when you set the scope.
3. **Put the skill that ads mention most into the smallest scope that ships.** SQL (40 % of ads, about 10 % of observed candidates) appears in one query in `austria-data-job-market-intelligence`, and the SQL warehouse was the first layer cut from `austrian-mmm-budget-optimizer`. The warehouse dashboard uses Tableau (3 % of ads) instead of Power BI (17 %). Rule: the next project (B2B SaaS revenue retention) starts with SQL over a modelled schema, not with SQL as a later layer.

## Notes on method and facts

* The git table in `BUSINESS_ACUMEN_PLAN_2026-10-28.md` came from local clones that were 8 to 185 commits behind GitHub. These pages use `origin/<default>` and say where they differ from the plan. Examples: `NextMove`, `metric_lineage_simulator` and `Chart_Audit_Framework` have READMEs on GitHub, and `energy-procurement-risk-analyzer` has real-data results from 2026-10-28.
* The gate baseline for both runs is in [`_gate_baseline_2026-10-28.txt`](_gate_baseline_2026-10-28.txt).
* A verdict follows cost and fit, not only the total. `decision-analytics-reconstruction` scores 8 after the plan but stays "sunk": it took 144 h against the 60 h median, and D-034 freezes it.
* The ex-ante counterpart of every page is in `docs/business-case/`.
