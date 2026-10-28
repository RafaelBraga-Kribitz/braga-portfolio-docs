# austrian-mmm-budget-optimizer: was it worth building?
2026-10-28 · status in registry: Complete · hours: 32 h, estimate from git ±50 % (16 to 48 h)

## Cost
| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days | 8 (2026-08-04 to 2026-10-27) | `git log origin/main` at 948dbcb |
| Hours | 32 h (16 to 48 h), estimate from git ±50 % | 8 days × 4 h, `_assumptions.md` |
| Phases on `main` | planning 1 day (2026-08-04) · model build 1 day (2026-09-15, "overnight build") · README, memo, audit 4 days · design system and dashboard 2 days (2026-10-26/27) | same log; STATUS.md |
| Commits, code files | 62 commits · 36 code files (35 `.py`, 1 `.js`) | `git rev-list`, `git ls-files`. Agents built most of it (GSD plans, a 44-pull-request agent stack, a parallel build), so the commit count is inflated. |
| Work not on `main` | all local refs: 399 commits on 15 days → 60 h. That is above the ±50 % range. | `git log --all`. Seven branch-only days (2026-08-05/06, 09-01 to 09-03, 09-18/19); the stack was salvaged by copying functions (STATUS D-04, D-30). |
| Money value | €1,440 (€560 to €2,880) | hours × €45/h (€35 to €60), `_assumptions.md` |
| Plan at start | 14 days (charter §5, M0 to M7) | `docs/archive/PROJECT_CHARTER.md`, 2026-07-18. Scope was cut later (ADR-008, ADR-009), so plan and actual do not compare one to one. |

The plan file's git table (57 commits, last commit 2026-09-19, 42 Python files) is out of date. The October commits came after it.

## Opportunity cost
The alternatives below use hindsight (D-034 and the application plan did not exist in August 2026). All three are shown until Rafael answers open question 5.

| Alternative | 32 h buys (range for 16 to 48 h) | Source |
|---|---|---|
| Applications at 1 to 1.25 h each | 26 to 32 applications (13 to 48) ≈ 3 to 4 weeks at 8 to 10 per week | `_assumptions.md`; 0 sent as of 2026-10-28 |
| German study toward B1 | 32 h = 5 % of about 640 h from A1.2 to the B1 exam (2.5 % to 7.5 %) | `_assumptions.md`; only 6 ads name B1 as enough (vintage 2026-10-18) |
| Next scored project (B2B SaaS revenue retention) | 0.53 projects (0.18 to 1.6); proxy = median git estimate of the five flagships, 15 days × 4 h = 60 h (30 to 90 h) | D-034; median of 6, 8, 15, 20, 36 commit days, git 2026-10-28 |

## Scenarios
Outcome = hiring-evidence score, 0 to 2 per item. **0 applications have been sent, so this is not a conversion rate.** Market shares: "ads mention", snapshot vintage 2026-10-18, core n = 699. Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention).

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no artefact; the hours go to an alternative above | 0: nothing to show | 0: no marketing project; the 20-year marketing career has no code proof | 0: no story | 2: by convention, no hours at stake | 2 |
| S1 as published today | 1: Python (39 %), statistics (16 %); Power BI (17 %) only as a text project not yet opened in Desktop; no SQL (40 %): the DuckDB and dbt warehouse was cut (ADR-009); no cloud (32 %) | 2: README has questions in the lead, a recommendation, results and limits, plus a Power BI text project; 2,942 words | 2: marketing budget split, the domain angle in force; marketing analytics as a title: 18 ads nationally, 0 in Styria | 1: number (15.1 %, 10th percentile 8.8 %), caveat (units are not euros) and "what I would do differently" exist; the README says only "one advertiser", the role ("the marketing lead") is only in `reports/memo_EN.md`; 17 internal codes, 56.4 % STE (`_prose_measures_2026-10-28.md`) | 2: gate PASS_WITH_EXCELLENCE (`_gate_baseline_2026-10-28.txt`, run B); about 1.5 h README rewrite left (plan budget) | 8 |
| S2 after this plan | 1: the rewrite adds no tool | 2: same README form; easier to read | 2: same | 2: the top box names the owner and the decision: "move budget from out-of-home to TV and Facebook; gain about 15 % of media contribution"; 0 codes | 2: 0 h left | 9 |
| S3 extended (finish the D-034 Power BI page: open `MMM.pbip` in Desktop, refresh, check the cards, commit Power BI screenshots) | 1: Power BI is now visible; SQL (40 %) is still absent | 2: a rendered Power BI report adds proof; the item is already at 2 | 2: same | 2: same | 1: 8-step checklist in `dashboards/README.md`; never opened in Desktop; assumption 2 to 4 h on top of S2 (central 3 h) | 8 |

## Verdict
**worth it, finish then freeze.** Finish S2 (README rewrite, gate green). Then freeze.

S3 scores 1 point below S2: scarcity is already at 2, and the Desktop step costs 1 finish-cost point. D-034 lists it as the last Track A step, and the report is already written as text. Do the Desktop step only if Track A hours allow. Two other repositories also hold Power BI text projects (austria-data-job-market-intelligence, energy-procurement-risk-analyzer), so this one is not the only Power BI proof.

The planner's prior was "worth it, finish (Power BI page)". The verdict agrees. Two facts differ:
1. The Power BI page exists since 2026-10-27 (ADR-010: four pages as PBIP, plus an HTML twin). Only the human Desktop step is open.
2. The knowledge file's refit plan says "data in DuckDB/PostgreSQL queried with SQL". The repository rejects this (STATUS D-29: do not resurrect the warehouse; ADR-009). The project shows no SQL. That is the largest demand gap.

## Lesson for the next project choice
The charter planned nine specs, including a SQL warehouse. The slim build that shipped dropped the warehouse first, and SQL is the skill ads mention most. Next time, put the top-demand skill in the minimum scope, not in a layer that can be cut.

## Open questions
1. Rafael's own hours log (open question 4). Branch-only work (7 days) is not in the 32 h.
2. Is SQL still part of the MMM refit (knowledge file) against STATUS D-29 and ADR-009? Rafael decides. A SQL step would raise demand match to 2. Its hours are unknown.
3. The Desktop-step hours (2 to 4 h) are an assumption. Nobody has opened the report in Desktop.
4. Real Austrian client data: the charter's Layer R plan needs a private agency drop with written permission. The repository records no date or contact for it.
5. Which alternative counts as the 2026 opportunity cost (open question 5).
