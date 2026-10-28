# energy-procurement-risk-analyzer: was it worth building?

2026-10-28 · registry: `Functional`, `incomplete: true` · 60 h (30 to 90 h), estimate from git ±50 %

Outcome measure: 0 applications have been sent. This page scores hiring evidence, not conversions (source: `_assumptions.md`).

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days, `origin/main` | 15 | `git log origin/main` at `dc62a20`, 2026-10-28 |
| Period | 2026-07-19 to 2026-10-28 | Core build 2026-07-19 to 07-24 (146 of 198 commits). First real-data run on 2026-10-28. |
| Hours | 60 h (30 to 90 h) | 15 days × 4 h, ±50 % (`_assumptions.md`). Not a measured number. |
| Commits | 198 (171 Rafael, 24 Claude, 3 Cursor Agent, by author name) | Agent-assisted. The commit count is not an effort measure. |
| Code and tests | 101 code files; 54 test files, at least 402 top-level test functions | `git ls-files`; `grep '^def test_'` |
| Work outside `main` | 9 more commit days on unmerged branches (2026-07-25 to 07-31, 09-02 to 09-03) | Local branch `gsd/v1.0-milestone` has 395 commits. With all branches, the estimate is 24 days, which is 96 h. This is an upper-side caveat. |

## Opportunity cost

The 60 h (30 to 90 h) could have bought one of these. All three are shown until Rafael answers open question 5.

| Alternative | What 60 h buys | Note |
|---|---|---|
| Applications | 48 to 60 applications (24 to 90 in the full range), at 1 to 1.25 h each. That is about 6 weeks at 8 to 10 per week. | 0 sent so far. Applications start 2027-01-04. |
| German | 60 h is about 9 % of the ≈ 640 h path from A1.2 to the B1 exam, or 3 weeks of the 20 h/week course load. | B1 alone unlocks little: 6 ads name B1 as enough (2026-10-18). |
| Next project | About one full B2B SaaS retention flagship. Proxy: the median of the five flagships is 15 commit days = 60 h, and this project is that median. | D-034 rank 1, score 82. Proxy only; its real size is unknown. |

## Scenarios

Market shares: "ads mention", `career-knowledge-core.md`, snapshot 2026-10-18, n = 699. Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items".

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no artefact | 0: no artefact | 0: no artefact | 0: no story | 2: by convention, no hours at stake; the 60 h go to an alternative above | 2 |
| S1 as published today (`dc62a20`) | 2: SQL (dbt, `sql/`), Python, a data-quality report, ETL gates, a Power BI project, Azure Bicep. Ads mention SQL 40 %, Python 39 %, data quality 31 %, ETL 20 %, Azure 19 %, Power BI 17 %. | 2: SQL, data quality, a dbt warehouse, Power BI, and a README with question → result → limits are all on the scarce list | 2: a 50 GWh Styrian manufacturer on the Austrian market, with a German summary. Industrial, not marketing. | 1: has a number (€27.04 M wrong-strategy cost, CALIBRATED) and a caveat (constructed load), but the decider is only "a manufacturer", with no role. No one-line recommendation. No "what I would do differently". 2,284 words, 62.7 % STE (`_prose_measures_2026-10-28.md`). | 2: gate already `PASS_WITH_EXCELLENCE`, 2 warnings (`_gate_baseline_2026-10-28.txt`, run B). About 1 h to S2 (plan budget). | 9 |
| S2 after this plan | 2: same | 2: same | 2: same | 2: the top box names the CFO and the choice. Fixed annual is cheapest in expectation. Hybrid 70 % fixed costs €0.18 M more for a €0.17 M lower P95 (both SIMULATED). | 2: 0 h after the rewrite; freeze | 10 |
| S3 extended (deploy the existing Azure path, refresh the Power BI project in Desktop, add screenshots) | 2: shows a live Azure deployment (19 %) and a visible Power BI report (17 %). No new skill family. | 2: Azure and Power BI proof are on the scarce list | 2: same | 2: same story | 1: the code exists since 2026-10-14 (ADR-020). Deploy, secrets and the Desktop refresh remain. The hours are not in the repository (judgement: 4 to 8 h on top of S2). D-034 gates it behind about 40 logged applications. | 9 |

## Verdict

**Worth it, finish then freeze.** Finish means the S2 README rewrite (about 1 h). Then freeze. S3 adds tools, not story. Keep S3 behind the application-log gate.

## Lesson for the next project choice

A decision model on real public data with one euro answer earns most of the hiring evidence in about 60 h. Before you schedule an extension, check the repository: most of the planned Azure refit was already built.

## Open questions

1. Rafael's own hours (open question 4). The default branch gives 15 days. All branches give 24 days.
2. Branch `gsd/v1.0-milestone` (395 commits, window 2021 to 2024) is not merged. The plan file quotes its numbers (€25.62 M, €6.99 M, €0.12 M). The real-data run replaces them. Keep or delete the branch?
3. Plan item 5 asks for a README line on "why 70 % forward over the others". The real-data run does not support 70 % as the default. It supports Fixed annual for a cost-minimizing CFO, and 70 % only for a risk-averse CFO. Which framing does Rafael want?
4. The registry descriptor still says "real-data results pending". The run was done on 2026-10-28. Update the registry?
5. ADR-008 (the ÖSPI series pick) still has status "proposed". The CALIBRATED strategy costs depend on it. Owner confirmation is open.
6. The S3 hours are not in the repository.
7. Which alternative counts as the opportunity cost for 2026 (open question 5)?
