# Cost basis for project value evaluations

Version 1.2 | 30 October 2026. Every `docs/economic-evaluation.md` uses these conventions. The method is
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
| Maintenance | 10 % of build hours per year **of use**, at the project's all-in rate, beyond any maintenance already inside the scope estimate | Convention, applied to every project and every alternative. A study that informs one decision is used for one year; a tool reused every year is maintained every year. |

## Hours per project

No time log exists. **Central hours are the owner's scope estimates (2026-10-30)**, task by task, because commit days hide
squashed private work. Where the owner gave none, the charter's committed effort budget is used. Each estimate covers
discovery, data preparation, development, validation, documentation and, where stated, first-year maintenance. The
hours stand for active, agent-assisted effort; elapsed calendar time is separate and is not cost. Sensitivity: 0.5× and
1.5× hours. The commit-day count (days with a commit × 4 h, the convention of 2026-10-28) is kept as a cross-check.

| Project | Source of central hours | Central h | 0.5× / 1.5× h | All-in rate | Build cost (central) | Commit-day check |
|---|---|---|---|---|---|---|
| warehouse_humanoid_tco | charter: 8 to 10 part-time weeks × 20 h | 180 | 90 / 270 | €54 | €9,720 | 84 h |
| decision-analytics-reconstruction | owner scope: data and segments 80, allocation 100, poll tracking 70, integration and campaign support 70 | 320 | 160 / 480 | €54 | €17,280 | 144 h |
| austrian-mmm-budget-optimizer | owner scope: data 40, model 60, validation 50, optimiser 30, reporting and first-year maintenance 40 | 220 | 110 / 330 | €54 | €11,880 | 36 h |
| energy-procurement-risk-analyzer | charter effort budget: 11.5 days × 8 h | 92 | 46 / 138 | €47 | €4,324 | 60 h |
| austria-data-job-market-intelligence | owner scope: acquisition 90, analysis 40, presentation 60, validation 30, first-year maintenance 20 | 240 | 120 / 360 | €45 | €10,800 | 28 h |

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
