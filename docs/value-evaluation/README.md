# Project value evaluations: the five website projects

Date: 2026-10-30. Method: [`../PROJECT_VALUE_EVALUATION.md`](../PROJECT_VALUE_EVALUATION.md) v2.0. Costs:
[`COST_BASIS.md`](COST_BASIS.md) v1.1, the market rate of the role profile each project's work needs. Each evaluation
sits in its repository at `docs/economic-evaluation.md`; actuals and lessons sit next to it in `docs/lessons-learned.md`.
Shared lessons: [`../../LESSONS_LEARNED.md`](../../LESSONS_LEARNED.md).

All probabilities and the fraction of perfect information a study recovers are labelled assumptions, so every verdict
is conditional on them. Multiples carry no currency and compare across projects; the rates differ by role.

## Financial result

| Project | Decision and value mechanism | Role profile | Expected gross value | Central total cost | Multiple: central · 0.5× h · 1.5× h · rate +30 % | 4× verdict | Recommendation | Maximum affordable cost |
|---|---|---|---|---|---|---|---|---|
| [Energy Procurement Risk Analyzer](https://github.com/RafaelBraga-Kribitz/energy-procurement-risk-analyzer/blob/main/docs/economic-evaluation.md) | Fixed-price share for a 50 GWh Styrian consumer; information value, 3 yearly locks | data analytics · senior | €77k | €4,418 | 17.5× · 30× · 12× · 13.7× | passes financial hurdle | build | €19k |
| [Austrian MMM and Budget Optimizer](https://github.com/RafaelBraga-Kribitz/austrian-mmm-budget-optimizer/blob/main/docs/economic-evaluation.md) | Yearly channel split; budget moved × change in revenue per euro × margin, 3 years | data science · senior | €6.9k | €3,175 | 2.2× · 3.6× · 1.5× · 1.7× | fails financial hurdle | defer | €1.7k |
| [Warehouse Humanoid TCO](https://github.com/RafaelBraga-Kribitz/warehouse_humanoid_tco/blob/main/docs/economic-evaluation.md) | Two-humanoid pilot in one cell, or wait; cost of not knowing, 5 years | data science · senior | €7.1k | €7,236 | 0.99× · 1.9× · 0.67× · 0.77× | fails financial hurdle | defer | €1.8k |
| [Decision Analytics Reconstruction](https://github.com/RafaelBraga-Kribitz/decision-analytics-reconstruction/blob/main/docs/economic-evaluation.md) | A campaign's budget split and re-plan; information value, one campaign | data science · senior | €5.6k | €9,850 | 0.57× · 1.0× · 0.40× · 0.44× | fails financial hurdle | reject | €1.4k |
| [Austria Data-Job Market Intelligence](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/docs/economic-evaluation.md) | Which roles, regions and skills to target; avoided project rework, one search cycle | data engineering | €738 | €1,323 | 0.56× · 1.1× · 0.37× · 0.56× | fails financial hurdle | smaller version | €180 |

One of five passes. The four that fail were built for other portfolio reasons and keep their financial verdict.

What reverses each result:
- **Energy:** real fixed-price offers carry a premium of about €1.1/MWh or less.
- **MMM:** media spend of about €0.93M or more.
- **Warehouse:** four or more cells decide together, or the site would otherwise follow a vendor demo.
- **Decision Analytics:** a budget of about $14M.
- **Job market:** about two thirds of the planned project hours redirected by the data.

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
