# Metric Driver-Tree Studio: was it worth building?
2026-10-28 · registry status: In development (`incomplete: true`) · hours: 24 h, estimate from git ±50 % (range 12 to 36 h)

Hiring evidence only. **0 applications have been sent**, so no conversion data exists. The score below is a hiring-evidence score (0 to 2 on five items), not a conversion rate. Assumptions: [`_assumptions.md`](_assumptions.md).

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days on `origin/main` | 6 (first 2026-06-07, last 2026-10-27) | `git log origin/main`, base 663d046 |
| Hours | 6 days × 4 h = **24 h**, range 12 to 36 h | Estimate from git ±50 % (`_assumptions.md`) |
| Cross-check, all branches | 12 commit days = 48 h; 111 commits against 24 on `main` | Squash merges hide branch work. One day (2026-10-14) holds 11 pull requests from an agent-assisted run. Treat 24 to 48 h as the plausible band. |
| Size | 24 commits on `main`; 149 script files (`.py`, `.ts`, `.tsx`, `.js`), 68 of them app and engine source; 92 unit tests, 7 end-to-end tests (README) | Agent-assisted, so commit counts overstate effort |
| Not in git | Build specs v2 to v4 and the Phase 0 prototype, written before the first commit | Unknown hours (open question 1) |

## Opportunity cost

| Alternative | 24 h buys | 48 h buys | Source |
|---|---|---|---|
| Applications | 19 to 24 applications at 1 to 1.25 h each (2.4 weeks of the 2 h weekday block) | 38 to 48 | `_assumptions.md`, D-035. Applications start 2027-01-04, so this cost is real only if the hours had come out of the application-system build. |
| German | 24 h of study = 15 % of one sublevel (160 h); 3.8 % of the 640 h from A1.2 to B1 | 30 % of a sublevel; 7.5 % of 640 h | `_assumptions.md` |
| Next project (B2B SaaS retention, D-034) | 40 % of one flagship-sized project (proxy 60 h = median of the five flagships: 6, 8, 15, 20, 36 commit days × 4 h) | 80 % | Proxy, labelled |

All three stay on the page until Rafael answers open question 5 of the brief.

## Scenarios

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no artefact | 0: no artefact | 0: none | 0: none | 2: by convention, no hours at stake | **2** |
| S1 as published today (`origin/main`, gate PASS, `_gate_baseline_2026-10-28.txt` run B) | 1: SQL view, DAX and statistics shown (ads mention SQL 40 %, Power BI 17 %, statistics 16 %; snapshot 2026-10-18); DAX never run in Power BI; no Python (39 %) | 2: README follows question, result, limits (scarce on GitHub); the SQL and Power BI part is a kit, no `.pbix` | 2: online-shop funnel, contribution profit, test priority; baselines ILLUSTRATIVE and not Austrian | 0: number (€5,832, 5.5×) and caveat exist, but the README names no decision owner (`_prose_measures_2026-10-28.md`: owner no); the shop is invented | 2: about 1 to 1.5 h to S2 (estimate on this page) | **7** |
| S2 after this plan (README in plain language, decider named) | 1: no new skill shown | 2: same | 2: same | 2: role, number, caveat and next test fit in 2 minutes; 0 codes, 96.1 % STE | 2: 0 h left | **9** |
| S3 extended: build the `.pbix` from the kit, add one page image | 1: Power BI and SQL shown running (kit check values: profit 549,121 over 12 periods), but only as an export beside the TypeScript app | 2: Power BI plus SQL on a KPI tree with stated limits | 2: same | 2: same | 1: 2 to 4 h on top of S2 (assumption, central 3 h; the kit says about 30 min to build, plus checks) | **8** |

Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention). A hosted demo stays outside S3: the project's own launch rule is not met (two of three modeled edges are ILLUSTRATIVE).

## Verdict

**Worth it, finish then freeze.** The product already runs end to end and passes the gate. S1 to S2 costs about 1 to 1.5 h for +2 points. S3 scores 1 point below S2. Do not extend to S3 before the application-log gate (about 40 rows). Keep it as a supporting repository, not a fourth flagship.

README edits needed most (`BUSINESS_ACUMEN_PLAN_2026-10-28.md`, section "Standard rewrite recipe"):

| Priority | Edit | Evidence |
|---|---|---|
| 1 | Name the decider in the first paragraph: a growth or experimentation lead at an online shop, who picks the next test | No role is named today |
| 2 | Replace internal codes: ADR-0004, ADR-0010 (twice), F-001 to F-021, "21 closed findings" | Writing rule 2 |
| 3 | Define or move down: elasticity, P10/P50/P90, tornado, Fisher-z, OLS, Anscombe | Writing rule 1 |
| 4 | Move the governance badge and the `make verify` row below Limitations | Recipe step 4 |
| 5 | Sentences: 10.4 % of 67 prose sentences have more than 25 words; 80.6 % STE (`_prose_measures_2026-10-28.md`, published README) | Already near target |

## Lesson for the next project choice

Name a real decider and a real data source before the build. This tool ranks tests on an invented shop, so its public launch is blocked by its own rule. Cap the process load too: 22 findings, 10 decision records and a copied governance kit surround a 2,468-line engine.

## Open questions

1. How many hours did you spend, including the specs and the Phase 0 prototype before 2026-06-07 (open question 4 of the brief)?
2. Did any online-shop analyst or a real incident shape the scope? The repository has none. The planner's prior ("where a wrong KPI comes from") does not match the product: the studio ranks which guess to test.
3. The registry `demo_reason` says the Phase 2 UI is not built. The README shows the built UI and a GIF. Should the registry text change? (Not edited here.)
4. The plan's git table lists 70 commits and no README. `origin/main` has 24 commits and a README. Which clone and which count do you use?
5. Does the launch rule (ADR-0004, a defended authoring pass) still stand? It decides whether a hosted demo is possible.
