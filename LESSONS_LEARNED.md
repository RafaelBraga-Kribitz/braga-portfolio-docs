# Lessons learned: BRAGA portfolio (canonical)

The shared lessons for every BRAGA project. **Before a build**, read this file and cite the ids that apply in the
project's `docs/economic-evaluation.md` ([method](docs/PROJECT_VALUE_EVALUATION.md)). **After delivery**, record
project lessons in the project's `docs/lessons-learned.md` and add a lesson here only when it applies beyond one
project. Never edit a lesson's evidence after the fact; supersede it with a new id.

Each lesson has a scope, evidence with its originating projects, and a date.

| Id | Lesson | Scope | Evidence (originating projects) | Date |
|---|---|---|---|---|
| L-001 | **Evaluate before the first commit.** Commit `docs/economic-evaluation.md` and the README's "Why this project exists" before implementation starts, and select the project against the 4× financial hurdle. A project built for other reasons keeps its financial verdict. | every new project | `honesty.value_evaluation` (manifest 1.6.0); the five website projects, [results](docs/value-evaluation/README.md) | 2026-10-30 |
| L-002 | **Test perfect information against four times the cost before estimating anything else.** If the expected value of perfect information (EVPI) is below 4× cost, no study quality can pass the hurdle. Look for more decisions sharing the answer (cells, sites, years), or build smaller. | decision studies, one-off decisions | Warehouse: EVPI €28.6k against 4× cost €28.9k (L-WHT-3). Decision Analytics: 4× needs €140k against a whole assumed gap of €80k | 2026-10-30 |
| L-003 | **Secure the person who will act, and their data, before the build.** The binding risk in three of five evaluations was adoption: no owner, no data or no action, not model quality. | client-data analytics, career research, reconstructions | MMM: client data never arrived (L-AMBO-1). Decision Analytics: a closed decision has nobody to act (L-DAR-1). Job market: advice not yet acted on (L-ADJMI-1) | 2026-10-30 |
| L-004 | **Do the spreadsheet pass first.** Compute the break-even from the first-commit configuration and check the sign of the expected gain on a quick backtest before building a simulator or a pipeline. | procurement and technology evaluations | Warehouse: break-even of 1.19 worker-equivalents from the prices alone (L-WHT-1). Energy: on real data the assumed premium saving reversed sign (L-EPRA-1) | 2026-10-30 |
| L-005 | **Value the decision, not the forecast error.** A model with lower error can carry less decision value. | models that support budget or allocation moves | MMM: ridge had lower holdout error, yet only the MMM answers the channel split (L-AMBO-2) | 2026-10-30 |
| L-006 | **Freeze the scale inputs with the evaluation, and re-run it when they change.** Budget, volume and revenue base drive the multiple almost linearly. | every evaluation whose value scales with a budget | Decision Analytics: scope $2M, build $6M (L-DAR-2). MMM: 4× needs about €0.93M of media | 2026-10-30 |
| L-007 | **Keep a time log from the first private commit.** Commit days × 4 h is a convention, not a record; squashed exports and agent runs make it unreliable by a factor of three. | every project, above all those that start private | Job market: 28 h by commit days against 9 h by commit sessions (L-ADJMI-2); [cost basis](docs/value-evaluation/COST_BASIS.md) | 2026-10-30 |
| L-008 | **Name the repository's own gates in the brief.** Line caps, number whitelists, generated READMEs and document-count budgets each need a small, named exception for a portfolio-wide change. | agent briefs for cross-repository changes | Warehouse: 200-line README cap and claims ledger. Energy: money-figure whitelist. MMM: generated README with a digit test. Decision Analytics: 20-document budget and registry | 2026-10-30 |

## Project lessons

| Project | File | Ids |
|---|---|---|
| Warehouse Humanoid TCO | [`docs/lessons-learned.md`](https://github.com/RafaelBraga-Kribitz/warehouse_humanoid_tco/blob/main/docs/lessons-learned.md) | L-WHT-1 to 3 |
| Energy Procurement Risk Analyzer | [`docs/lessons-learned.md`](https://github.com/RafaelBraga-Kribitz/energy-procurement-risk-analyzer/blob/main/docs/lessons-learned.md) | L-EPRA-1 to 3 |
| Austrian MMM and Budget Optimizer | [`docs/lessons-learned.md`](https://github.com/RafaelBraga-Kribitz/austrian-mmm-budget-optimizer/blob/main/docs/lessons-learned.md) | L-AMBO-1, 2 |
| Decision Analytics Reconstruction | [`docs/lessons-learned.md`](https://github.com/RafaelBraga-Kribitz/decision-analytics-reconstruction/blob/main/docs/lessons-learned.md) | L-DAR-1, 2 |
| Austria Data-Job Market Intelligence | [`docs/lessons-learned.md`](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/docs/lessons-learned.md) | L-ADJMI-1 to 3 |

Where to retrieve this file: `braga-portfolio-docs/LESSONS_LEARNED.md` on `main`. An assistant without access to this
repository cannot read it; say so in the evaluation instead of claiming it was checked.
