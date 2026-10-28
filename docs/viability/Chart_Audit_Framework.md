# Chart_Audit_Framework: was it worth building?
2026-10-28 · registry status: Foundation (`incomplete: true`) · 40 h (range 20 to 60), estimate from git ±50 %

0 applications have been sent. No conversion data exists. The scores below are a hiring-evidence score (0 to 2 on five items), not a conversion rate. Shared values come from `docs/viability/_assumptions.md`.

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days | 10 (2026-06-23, 06-24, 07-08, 07-09, 09-16, 09-17, 10-05, 10-11, 10-26, 10-27) | `git log origin/main`, base 2e372e97 |
| Hours | 10 days × 4 h = **40 h (20 to 60)** | Estimate from git ±50 %. Not Rafael's log (open question 4) |
| Commits | 30 on `main`: 21 by Rafael, 8 by Claude, 1 by Cursor Agent | Agent commits inflate the count. Days are the safer proxy |
| Period | 2026-06-23 to 2026-10-27 (18 weeks, 10 commit days) | The last two days (10-26, 10-27) are portfolio polish, not build |
| Own code | 10 Python files, about 4,200 lines (rules and tests 460, ratchet 287, hygiene 84, library scripts 3,195) | `git ls-files`, third-party folder excluded |
| Third-party files | 3,410 tracked files under `Deterministic_Data_Visualization_Framework/references/` | Scraped chart-site mirrors. NOTICE says "for study only", no licence granted |

The planner's table (4 commits, 6 Python files, no README) was stale. The current tree has 30 commits, 10 Python files and a README.

## Opportunity cost

| Alternative | What 40 h (20 to 60) buys | Source |
|---|---|---|
| Applications | 32 to 40 applications at 1 to 1.25 h each (range 16 to 60). None sent so far | `_assumptions.md`, D-035 |
| German | 6 % of the about 640 h from A1.2 to the B1 exam (range 3 to 9 %). About 2 weeks of course load at 20 h per week | `_assumptions.md` |
| Next project | About two thirds of one median flagship. Proxy: distinct commit days of the 5 flagships are 6, 8, 15, 20 and 36, so the median is 15 days = 60 h (30 to 90) | Same git method, label "proxy". Next scored project: B2B SaaS revenue retention (D-034) |

## Scenarios

Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention).

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: nothing shown | 0: nothing shown | 0: nothing shown | 0: nothing to tell | 2: by convention, no hours at stake | 2 |
| S1 as published today | 1: Python and YAML only. Ads mention visualisation 36 %, SQL 40 %, Power BI 17 % (2026-10-18). No SQL, no Power BI | 1: touches data quality (31 %, 2026-10-18) with 3 coded checks and 20 tests. README says "No results exist yet" | 0: generic chart method. The only target repo is the frozen election and allocation project | 0: no decision owner (`_prose_measures_2026-10-28.md`: owner no) and no business result; the only numbers are run times (routing 0.18 s, verification about 21 s, 41 charts) | 1: about 3 h to S2 (README recipe 1 h, remove third-party tree 0.5 h, decide on history purge 1.5 h; estimate) | 3 |
| S2 after this plan | 1: same stack | 1: same | 0: same | 0: top box names the BI lead who decides, but still no result number to tell | 2: 0 h left | 4 |
| S3 extended: run the 3 checks and the ratchet on the charts of the warehouse TCO, MMM and market-intel repos, and publish the count of defects found and fixed | 1: still no SQL or Power BI | 2: a result with limits on real repos | 1: Styrian logistics and marketing charts | 2: "I found N defects in my own charts and fixed them" | 0: 12 to 20 h on top of S2 (assumption) | 6 |

S2 adds 1 point, and only through finish cost. It removes a risk (the third-party files). It adds no hiring evidence. S3 adds 4 evidence points and loses 2 finish-cost points, for 12 to 20 h. The same hours buy about 10 to 20 applications at 1 to 1.25 h each.

## Verdict

**sunk, archive and unpin.** 40 h bought a method note and a small code base that no ad vocabulary maps to. The only target is a frozen repo. The repo still holds 3,410 third-party files. The career knowledge already records "Delete: scraped third-party site, legal risk" (full file, section 7).

## Lesson for the next project choice
Score a project by the ad vocabulary it shows and by a named business user before the first commit. A method kit with one frozen target and no result gives no interview story.

## Open questions
1. Is the GitHub repo public, and is it pinned on the profile? The repository does not show this.
2. Does Rafael want the third-party files purged from git history (rewrite and force-push), or only removed from the current tree?
3. Rafael's own hours for this repo (open question 4). The estimate has a ±50 % range.
4. Do the `chart-audit` and `chart-expert` skills help the audits of the other flagships? No usage log exists.
5. The cost of S3 (12 to 20 h) is an assumption. No scope estimate exists.

## Proposed summary README
Use this text if Rafael keeps the repo visible after removing the third-party files. It is a proposal. The README itself is unchanged.

```
# Chart Audit Framework (archived, Foundation)
A BI lead must decide which charts reach management. This kit checks a chart in a fixed order: question, logic, chart type, data, code, look.
Three checks run as code: a flat spread, a wrong interval label and dropped categories. They have 20 unit tests and a CI job.
A ratchet routes each chart to skip, verify-only or full audit. It ran once, on 2026-07-09, on one repo (41 charts): routing took 0.18 s, verification about 21 s.
Result: no audit score exists. A language model judges all other rules.
Limits: one target repo (frozen). The ratchet has no automated test. No release tag.
Status: archived 2026-10. Third-party reference files removed; see NOTICE.
Stack: Python 3, PyYAML, unittest, GitHub Actions, Claude Code skills.
License: Apache-2.0 for the author's files.
Author: Rafael Braga-Kribitz, Austria.
Why archived: no decision owner and no business result.
```
