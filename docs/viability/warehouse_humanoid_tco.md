# warehouse_humanoid_tco: was it worth building?
2026-10-28 · status in registry: Complete · hours: 80 h, estimate from git ±50 % (40 to 120 h)

## Cost
| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days | 20 (2026-05-21 to 2026-10-27) | `git log origin/main` at 9027334 |
| Hours | 80 h (40 to 120 h), estimate from git ±50 % | 20 days × 4 h, `_assumptions.md` |
| Build phase | 14 days ≈ 56 h (2026-05-21 to 2026-07-17) | same log |
| Presentation phase | 6 days ≈ 24 h (2026-09-16 to 2026-10-27: README, banner, charts, design system) | same log |
| Commits, code files | 109 commits · 189 `.py/.ts/.js` files (governance 140 files, src 33, tests 91) | `git rev-list`, `git ls-files`. The README says AI coding agents built it, so the commit count is inflated. |
| Money value | €3,600 (€1,400 to €7,200) | hours × €45/h (€35 to €60), `_assumptions.md` |
| Plan at start | "8 to 10 weeks part-time" | first-commit `PROJECT_CHARTER.md`. The build phase took 8 weeks: on plan. |

Caveat: the first commit already holds a 635-line charter and a 705-line data check notebook. Work before 2026-05-21 is not in the estimate.

## Opportunity cost
The alternatives below are seen with hindsight (D-034 and the application plan did not exist in May 2026). All three are shown until Rafael answers open question 5.

| Alternative | 80 h buys (range for 40 to 120 h) | Source |
|---|---|---|
| Applications at 1 to 1.25 h each | 64 to 80 applications (32 to 120) ≈ 8 weeks at 8 to 10 per week | `_assumptions.md`; 0 sent as of 2026-10-28 |
| German study toward B1 | 80 h = 12.5 % of about 640 h from A1.2 to the B1 exam (6 % to 19 %) | `_assumptions.md`; only 6 ads name B1 as enough (vintage 2026-10-18) |
| Next scored project (B2B SaaS revenue retention) | 1.3 projects (0.4 to 4.0); proxy = median git estimate of the five flagships, 15 days × 4 h = 60 h (30 to 90 h) | D-034; median of 6, 8, 15, 20, 36 commit days, git 2026-10-28 |

## Scenarios
Outcome = hiring-evidence score, 0 to 2 per item. **0 applications have been sent, so this is not a conversion rate.** Market shares: "ads mention", snapshot vintage 2026-10-18, core n = 699. Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention).

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no artefact; the hours go to an alternative above | 0: nothing to show | 0: no intralogistics proof elsewhere in the portfolio (the energy project covers procurement, not logistics) | 0: no story | 2: by convention, no hours at stake | 2 |
| S1 as published today | 1: Python (39 %), statistics (16 %), SQL (40 %) only as DuckDB checks; dashboard is Tableau (3 %), no Power BI (17 %), no cloud (32 %) | 2: question in the lead, decision box, result, limits, data-quality tags and 91 test files; the pool lacks these | 2: KNAPP-type intralogistics; KNAPP and Magna each have 5 ads in Styria (vintage 2026-10-18, small n) | 0: number (€0.453M lean mix) and caveat exist, but the README names no decision owner; codes (F-222, ρ), 8 internal codes, 75.0 % STE (`_prose_measures_2026-10-28.md`) | 2: the published README already passes the gate, PASS_WITH_EXCELLENCE (`_gate_baseline_2026-10-28.txt`, run B); about 1.5 h README rewrite left (plan budget) | 7 |
| S2 after this plan | 1: the rewrite adds no tool from the top of the ad list | 2: same, easier to read | 2: same | 2: the plan's renames ("Lean mix: 1 worker + 3 robot carts", "5-year total cost in today's money") give a 2-minute story; rewritten README names the owner, 0 codes | 2: 0 h left | 9 |
| S3 extended (one Power BI page on the existing DuckDB SQL, in place of Tableau) | 2: adds Power BI (17 %) and moves SQL (40 %) to the front | 2: Power BI is on the scarcity list | 2: same | 2: same | 1: no `.pbix` exists (`docs/POWER_BI_SETUP.md`, ADR-0008); assumption 4 to 8 h on top of S2 | 9 |

## Verdict
**worth it, finish then freeze.** Finish S2 (README rewrite for plain language and business names; the gate is already green). Then freeze. S3 adds 1 point and costs 1 point, so it does not pay.

The planner's prior was "worth it, keep". The value agrees. The difference is the next step: the S3 score and the knowledge rule "do not extend the Tableau dashboard" both say: add no more work.

## Lesson for the next project choice
The decision answer came from crew sizing and simple cost arithmetic. Governance (140 files) grew larger than the model (33 source files). Next time, cap the governance layer before the build starts, and lead with the tool that ads mention most (Power BI over Tableau).

## Open questions
1. Rafael's own hours log (open question 4). The estimate ignores work done before the first commit.
2. The charter's success test "at least 1 response from an Austrian industrial company within 4 weeks of public release": the repository holds no record of the result.
3. The S3 hours (4 to 8 h) are an assumption. No Power BI work exists to measure.
4. Which alternative counts as the 2026 opportunity cost (open question 5).
