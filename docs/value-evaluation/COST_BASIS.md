# Cost basis for project value evaluations

Version 1.1 | 30 October 2026. Every `docs/economic-evaluation.md` uses these conventions. The method is
[`../PROJECT_VALUE_EVALUATION.md`](../PROJECT_VALUE_EVALUATION.md).

**Owner decision (2026-10-30), replacing the method's "one common rate":** each project is costed at the market rate
of the role profile its work needs, not at one rate for every project. Different work needs different skills, and the
market prices those skills differently. Each rate is the **cost of a role in the market**, drawn from advertised legal
minimums. It is not the author's pay, expectation or price. Projects are compared on their value/cost multiples, which
carry no currency.

## Role rate: closest profile in Austria Data-Job Market Intelligence

Source: median **advertised minimum** gross annual salary (collective-agreement floor, ×14 payments) by role family and
seniority, snapshot of 2026-10-18 ([`outputs/salaries.json`](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/outputs/salaries.json),
`by_family_seniority`; families as defined in [`docs/role-taxonomy.md`](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/docs/role-taxonomy.md)).
These are floors: 375 of 699 core ads say they pay above them, and third-party medians sit 20 to 40 % higher
([`docs/salary-context.md`](https://github.com/RafaelBraga-Kribitz/austria-data-job-market-intelligence/blob/main/docs/salary-context.md)).

**Selection rule.** Name the role family and seniority an Austrian employer would staff for the project's core work.
Use that cell when it holds at least 10 ads. Otherwise use the family row when it holds at least 20 ads. Otherwise use
the nearest family with at least 20 ads that covers the core skill, and say why.

**Loaded hourly rate** = (advertised minimum × 1.296) / 1,640 h, rounded to €1.

* Employer contributions and payroll costs: 29.6 % of gross (Austria 2026: social insurance ≈ 18.5 %, Dienstgeberbeitrag
  3.7 %, Zuschlag ≈ 0.3–0.4 %, Kommunalsteuer 3 %, Mitarbeitervorsorge 1.53 %;
  [freefinance.at](https://freefinance.at/selbststaendig-machen/lohnnebenkosten.html),
  [everbill.com](https://www.everbill.com/lohnnebenkosten/)).
* Productive hours: 1,640 h a year, an assumption: 38.5 h × 52 weeks = 2,002 h, less 25 vacation days, 13 public
  holidays and 9 sick days (47 days × 7.7 h). Paid nonproductive time sits in this denominator and is not charged again.

| Project | Core work | Closest profile (family · seniority, n ads) | Advertised minimum | Loaded rate | All-in per hour |
|---|---|---|---|---|---|
| warehouse_humanoid_tco | discrete-event simulation and Monte Carlo cost model | data science · senior, n = 32 | €64,554 | €51 | €54 |
| decision-analytics-reconstruction | segmentation, optimisation (MILP) and Bayesian poll tracking | data science · senior, n = 32 | €64,554 | €51 | €54 |
| austrian-mmm-budget-optimizer | Bayesian marketing-mix model and budget rule | data science · senior, n = 32 (marketing analytics has 13 ads in all, 2 senior: too thin) | €64,554 | €51 | €54 |
| energy-procurement-risk-analyzer | procurement risk analysis and backtests on market prices | data analytics (includes risk analysts) · senior, n = 12 | €56,000 | €44 | €47 |
| austria-data-job-market-intelligence | multi-source collection pipeline, de-duplication, taxonomy, dashboards | data engineering · unspecified, n = 74 | €53,240 | €42 | €45 |

**Rate sensitivity.** Because the inputs are floors, every page also states its central multiple at a rate 30 % higher,
as a reversal check.

## Other cost lines (same for every project)

| Line | Value | Type |
|---|---|---|
| AI assistance | €2 per active hour | Allowance. Agent-assisted builds; plan and token volumes are not recorded in the repositories. A subscription of about €180 a month spread over about 125 active project hours a month gives €1.4 per hour; €2 covers retries and API overage. Marginal expenditure. |
| Equipment, electricity, internet | €1 per active hour | Allowance, allocated overhead (not marginal). |
| Hosting, compute, data | €0 unless the page states otherwise | GitHub, GitHub Pages and Tableau Public free tiers; public data. Machine runtime is never charged as employee hours. |
| Maintenance over the horizon | 10 % of build hours per year, at the project's all-in rate | Convention, applied to every project and every alternative. |

## Hours per project

No time log exists. **Central hours = distinct commit days on the default branch × 4 h**, the convention behind the
relative effort already on record in [`../viability/README.md`](../viability/README.md) (2026-10-28), updated with the
commits up to 2026-10-30. The hours stand for active, agent-assisted effort, not a human-equivalent delivery estimate;
elapsed calendar time is separate and is not cost. Sensitivity: 0.5× and 1.5× hours. The session-span check (commit
timestamps grouped at gaps of 90 minutes or less, plus 30 minutes per session) is lower everywhere because squashed
commits hide work.

| Project | First commit | Commit days | Central h | 0.5× / 1.5× h | Build cost (central · 0.5× · 1.5×) | Session-span check |
|---|---|---|---|---|---|---|
| warehouse_humanoid_tco | 2026-05-21 | 21 | 84 | 42 / 126 | €4,536 · €2,268 · €6,804 | 38 h |
| decision-analytics-reconstruction | 2026-05-07 | 36 | 144 | 72 / 216 | €7,776 · €3,888 · €11,664 | 105 h |
| austrian-mmm-budget-optimizer | 2026-08-04 | 9 | 36 | 18 / 54 | €1,944 · €972 · €2,916 | 17 h |
| energy-procurement-risk-analyzer | 2026-07-19 | 15 | 60 | 30 / 90 | €2,820 · €1,410 · €4,230 | 32 h |
| austria-data-job-market-intelligence | 2026-09-17 | 7 | 28 | 14 / 42 | €1,260 · €630 · €1,890 | 9 h |

## Perspective

* **Company decision tools** are evaluated for the employer setting the repository names, with scale facts from the
  repository, as work done by the closest role profile above.
* **Career research** (`austria-data-job-market-intelligence`) takes the job seeker's perspective. Value it first by
  avoided rework, i.e. project hours not spent on the wrong portfolio projects, at the profile rate. If earlier earnings
  are used, express them as a break-even number of weeks at the target role's advertised floor, labelled as a market
  floor, never as the author's salary or expectation. Hiring evidence is shared across the portfolio, so it is never
  added to a company case.
* Benefit horizons are chosen per decision and stated on each page; benefits over more than one year are discounted at
  5 % per year where material.
