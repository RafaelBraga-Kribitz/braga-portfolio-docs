# Project value evaluations: the five website projects

Date: 2026-10-30. Method: [`../PROJECT_VALUE_EVALUATION.md`](../PROJECT_VALUE_EVALUATION.md) v2.0. Costs:
[`COST_BASIS.md`](COST_BASIS.md) v1.2: the market rate of the role profile each project's work needs, and the owner's scope-estimate hours (the charter's budget where none was given). Each evaluation
sits in its repository at `docs/economic-evaluation.md`; actuals and lessons sit next to it in `docs/lessons-learned.md`.
Shared lessons: [`../../LESSONS_LEARNED.md`](../../LESSONS_LEARNED.md).

All probabilities and the fraction of perfect information a study recovers are labelled assumptions, so every verdict
is conditional on them. Multiples carry no currency and compare across projects; the rates differ by role.

## Financial result

| Project | Decision and value mechanism | Role profile (all-in rate) | Expected gross value | Central total cost | Multiple: central · 0.5× h · 1.5× h · rate +30 % | 4× verdict | Recommendation | Maximum affordable cost |
|---|---|---|---|---|---|---|---|---|
| [Energy Procurement Risk Analyzer](https://github.com/RafaelBraga-Kribitz/energy-procurement-risk-analyzer/blob/main/docs/economic-evaluation.md) | Fixed-price share for a 50 GWh Styrian consumer; information value, 3 yearly locks | data analytics · senior (€47) | €77k | €6,373 | 12.2× · 22× · 8.4× · 9.5× | passes financial hurdle | build | €19k |
| [Warehouse Humanoid TCO](https://github.com/RafaelBraga-Kribitz/warehouse_humanoid_tco/blob/main/docs/economic-evaluation.md) | Crew size and a two-humanoid pilot for one cell; cost of not knowing, 5 years | data science · senior (€54) | €53k | €11,124 | 4.8× · 9.2× · 3.2× · 3.7× | passes financial hurdle | build, capped at 180 h | €13.3k |
| [Austria Data-Job Market Intelligence](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/docs/economic-evaluation.md) | Which roles, regions and skills to prepare for; earlier employment, one search | data engineering (€45) | €11.2k | €10,800 | 1.0× · 2.1× · 0.69× · 0.81× | fails financial hurdle | smaller version (a 40 h focused study: 4.2×) | €2.8k |
| [Austrian MMM and Budget Optimizer](https://github.com/RafaelBraga-Kribitz/austrian-mmm-budget-optimizer/blob/main/docs/economic-evaluation.md) | Yearly channel split against today's allocation; budget moved × change in revenue per euro × margin, 3 years | data science · senior (€54) | €12.3k | €14,256 | 0.86× · 1.7× · 0.57× · 0.67× | fails financial hurdle | defer | €3.1k |
| [Decision Analytics Reconstruction](https://github.com/RafaelBraga-Kribitz/decision-analytics-reconstruction/blob/main/docs/economic-evaluation.md) | A campaign's budget split and re-plans; 1.3 % of the actionable budget, one campaign | data science · senior (€54) | €26k at $2M, €78k at $6M (unsourced) | €17,280 | at $2M / $6M: 1.5 / 4.5× · 3.0 / 9.0× · 1.0 / 3.0× · 1.2 / 3.5× | insufficient evidence | defer until the budget is sourced | €6.5k / €19.5k |

Two of five pass; one has insufficient evidence; two fail. Every verdict keeps its financial result, whatever the project was built for.

What reverses each result:
- **Energy:** real fixed-price offers carry a premium of about €1.7/MWh or less.
- **Warehouse:** the real cell is already right-sized, or the build runs past about 215 h.
- **Job market:** the full system is reused for further decisions worth about 7.7 months of earlier employment in total.
- **MMM:** an advertiser of about €2.3M of media a year.
- **Decision Analytics:** an actionable budget of about €5.3M or more passes; below about €1.3M it fails even 1×.

## Selection-preference inputs (kept separate from money)

These inputs feed a future selection score. They never multiply a financial value, and no aggregate score is computed here.

| Project | Value class | Geography of the setting |
|---|---|---|
| Energy Procurement Risk Analyzer | cost/risk reduction | other Styria |
| Austrian MMM and Budget Optimizer | revenue | Graz (the design advertiser) |
| Warehouse Humanoid TCO | cost/risk reduction | Graz area (KNAPP-type operator) |
| Decision Analytics Reconstruction | efficiency/strategic | elsewhere (Paraguay) |
| Austria Data-Job Market Intelligence | efficiency/strategic | Graz |

Classes: revenue · cost/risk reduction · efficiency/strategic · meta. Geography: Graz · other Styria · Vienna · elsewhere.
