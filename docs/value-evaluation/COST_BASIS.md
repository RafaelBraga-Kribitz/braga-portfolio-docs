# Common cost basis for project value evaluations

Version 1.0 | 30 October 2026. Every `docs/economic-evaluation.md` in the portfolio uses these values, so that
projects can be compared. The method is [`../PROJECT_VALUE_EVALUATION.md`](../PROJECT_VALUE_EVALUATION.md).

## Loaded hourly rate: €40 per hour

| Input | Value | Source |
|---|---|---|
| Annual gross salary | €50,000 | Median **advertised minimum** for the `data_analytics` role family, n = 82 ads, Austria Data-Job Market Intelligence snapshot of 2026-10-18 ([`outputs/salaries.json`](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/outputs/salaries.json)). An advertised floor (collective-agreement minimum, ×14 payments), not actual pay; 375 of 699 core ads say they pay above it. |
| Employer contributions and payroll costs | 29.6 % of gross → €14,800 | Austrian employer on-costs 2026: social insurance ≈ 18.5 %, Dienstgeberbeitrag 3.7 %, Zuschlag ≈ 0.3–0.4 %, Kommunalsteuer 3 %, Mitarbeitervorsorge 1.53 % ([freefinance.at](https://freefinance.at/selbststaendig-machen/lohnnebenkosten.html), [everbill.com](https://www.everbill.com/lohnnebenkosten/)). |
| Productive annual hours | 1,640 h | Assumption: 38.5 h × 52 weeks = 2,002 h, less 25 vacation days, 13 public holidays and 9 sick days (47 days × 7.7 h). Paid nonproductive time sits in this denominator and is not charged again. |
| **Loaded rate** | (€50,000 + €14,800) / 1,640 h = €39.5 → **€40 per hour** | One rate for every project: one employee, one role. |

Why `data_analytics`: the portfolio targets analytics roles, and the analytics floor is the lowest of the families Rafael
applies to; `data_science` (€55,356, n = 124) would raise every cost by 11 % and change no verdict that is not already
marginal (each page names its own reversal threshold).

## Other cost lines (same for every project)

| Line | Value | Type |
|---|---|---|
| AI assistance | €2 per active hour | Allowance. Agent-assisted builds; the plan and token volumes are not recorded in the repositories. A €180-per-month subscription spread over about 125 active project hours per month (≈ 760 h over six months) gives €1.4 per hour; €2 covers retries and API overage. Marginal expenditure. |
| Equipment, electricity, internet | €1 per active hour | Allowance, allocated overhead (not marginal). |
| Hosting, compute, data | €0 unless the page states otherwise | GitHub, GitHub Pages and Tableau Public free tiers; public data. Machine runtime is never charged as employee hours. |
| **All-in cost per active hour** | **€43** | €40 labour + €2 AI + €1 overhead |
| Maintenance over the horizon | 10 % of build hours per year, at €43 per hour | Convention, applied to every project and every alternative. |

## Hours per project

No time log exists. **Central hours = distinct commit days on the default branch × 4 h**, the convention behind the
relative effort already on record in [`../viability/README.md`](../viability/README.md) (2026-10-28), updated with the
commits up to 2026-10-30. The hours stand for Rafael's active, agent-assisted effort, not a human-equivalent delivery
estimate; elapsed calendar time is separate and is not cost. Sensitivity: 0.5× and 1.5× hours. The session-span check
(commit timestamps grouped at gaps of 90 minutes or less, plus 30 minutes per session) is lower for most repositories
because squashed commits hide work, and higher for `DSX`, whose agent runs commit continuously.

| Project | First commit | Commit days | Central h | 0.5× / 1.5× h | Build cost at €43/h (central · 0.5× · 1.5×) | Session-span check |
|---|---|---|---|---|---|---|
| austria-data-job-market-intelligence | 2026-09-17 | 7 | 28 | 14 / 42 | €1,204 · €602 · €1,806 | 9 h |
| warehouse_humanoid_tco | 2026-05-21 | 21 | 84 | 42 / 126 | €3,612 · €1,806 · €5,418 | 38 h |
| austrian-mmm-budget-optimizer | 2026-08-04 | 9 | 36 | 18 / 54 | €1,548 · €774 · €2,322 | 17 h |
| energy-procurement-risk-analyzer | 2026-07-19 | 15 | 60 | 30 / 90 | €2,580 · €1,290 · €3,870 | 32 h |
| decision-analytics-reconstruction | 2026-05-07 | 36 | 144 | 72 / 216 | €6,192 · €3,096 · €9,288 | 105 h |
| metric_lineage_simulator | 2026-06-07 | 7 | 28 | 14 / 42 | €1,204 · €602 · €1,806 | 6 h |
| NextMove | 2026-07-24 | 12 | 48 | 24 / 72 | €2,064 · €1,032 · €3,096 | 31 h |
| Chart_Audit_Framework | 2026-06-23 | 10 | 40 | 20 / 60 | €1,720 · €860 · €2,580 | 9 h |
| funnel_correlation_py | 2026-02-25 | 6 | 24 | 12 / 36 | €1,032 · €516 · €1,548 | 5 h |
| governance-bootstrap | 2026-06-16 | 6 | 24 | 12 / 36 | €1,032 · €516 · €1,548 | 8 h |
| brazil-2026-election-forecast | 2026-09-29 | 4 | 16 | 8 / 24 | €688 · €344 · €1,032 | 8 h |
| DSX | 2026-07-27 | 34 | 136 | 68 / 204 | €5,848 · €2,924 · €8,772 | 202 h |
| bk-viz | 2026-08-08 | 4 | 16 | 8 / 24 | €688 · €344 · €1,032 | 3 h |
| braga-portfolio-docs | 2026-09-17 | 9 | 36 | 18 / 54 | €1,548 · €774 · €2,322 | 8 h |
| braga-portfolio-v2 (website) | 2026-10-20 | 10 | 40 | 20 / 60 | €1,720 · €860 · €2,580 | 27 h |

## Perspective and earnings conventions

* **Company decision tools and reusable tooling** are costed as work by one employee for the employer that would use
  them, at €43 per active hour. The decision owner is the setting the repository names; scale facts come from the
  repository.
* **Career research and the portfolio website** take Rafael's own perspective at the same cost convention. Earlier
  earnings are valued at **€962 per week** (€50,000 ÷ 52, gross, the same advertised floor). Hiring evidence is shared by
  every project in the portfolio, so a project's career value is reported as a break-even requirement, never added
  across projects.
* Benefit horizons are chosen per decision and stated on each page; benefits over more than one year are discounted at
  5 % per year where material.
