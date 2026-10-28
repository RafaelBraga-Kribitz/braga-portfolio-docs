# governance-bootstrap: was it worth building?

2026-10-28 · registry: framework, Maintained · hours: 24 h (range 12 to 36), estimate from git ±50 %

Outcome measure: 0 applications have been sent (as of 2026-10-28). The scores below are hiring-evidence scores, not conversions. Assumptions: `docs/viability/_assumptions.md`.

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days | 6 (2026-06-16, 09-16, 09-17, 09-21, 10-26, 10-27) | `git log origin/main`, 19 commits, 22 tracked `.py` files, base `cb7c2c7` |
| Hours | 24 h = 6 days × 4 h; range 12 to 36 h | Estimate from git ±50 %. Replace with Rafael's log (open question 4) |
| Split by commit subject | 1 day builds the kit (61 files, 4,414 lines in the first commit); 5 days polish the README, banner and README gate | Commit subjects only. The agent-assisted share is high: 4 of 19 commits are by Claude, Cursor Agent or a sync bot |
| Not counted | Work inside `decision-analytics-reconstruction` before the extraction (its first governance finding opened 2026-06-08) | Hours there cannot be separated from that project's 399 commits |

## Opportunity cost

24 h (12 to 36 h) could have bought one of these. This is a unit equivalence, not a claim that the hours were free to move: the application track starts 2027-01-04.

| Alternative | Equivalent of 24 h | Basis (`_assumptions.md`) |
|---|---|---|
| Applications | 19 to 24 applications (range 10 to 36); 2 to 3 weeks at 8 to 10 per week | 1 to 1.25 h per application. 0 sent so far |
| German study | 24 h = 1.2 weeks of the 20 h/week course = 4 % of the 640 h from A1.2 to the B1 exam | Owner-stated 2026-10-12 and 2026-10-19. B1 alone unlocks nothing measurable (6 ads name B1 as enough, snapshot 2026-10-18) |
| Next project | 40 % of one flagship. Proxy: median of 15 commit days × 4 h = 60 h across the five flagships | D-034: B2B SaaS revenue retention is next. Its true size is unknown |

## Scenarios

Scale 0 to 2 per item on the shared rubric (`_assumptions.md`, "Scoring rubric for the five hiring-evidence items"). Market shares are "ads mention", core n = 699, snapshot 2026-10-18. S0 earns its 2 points only from the finish-cost convention.

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: nothing shown | 0: nothing shown | 0 | 0 | 2: by convention, no hours at stake | 2 |
| S1 as published today (origin/main) | 1: Python 39 %, CI/CD 15 % visible; no SQL, Power BI or Azure. The kit gates code, not data (data quality 31 % is a different skill) | 0: Limitations section and a falsifiable closing sentence, but no result, so not the scarce question → result → limits form; no SQL, data-quality or warehouse content | 0: no marketing, customer or Styrian setting | 0: no number, no decision owner in the README (`_prose_measures_2026-10-28.md`: owner no) | 2: about 0.75 h to S2 (plan estimate); gate already PASS on origin/main (`_gate_baseline_2026-10-28.txt`, run B) | 3 |
| S2 after this plan (10-line summary README, gate green) | 1: same as S1 | 0: the summary states that no measured result exists | 0 | 0: problem, mechanism and one stated limit; no decision owner and no before/after number in the repository | 2: 0 h left | 3 |
| S3 extended: tag a first release, then log re-found issues in one consumer for 8 weeks and publish the counts | 1: same | 2: a measured result with limits completes the question → result → limits form | 0: still no domain | 0: a measured before/after number with a caveat, but still no decision owner (the kit serves the author's own projects) | 1: about 6 to 10 h over 8 weeks on top of S2 (estimate on this page) | 4 |

Totals: S0 2 · S1 3 · S2 3 · S3 4. S2 adds no point: the summary removes stale text but adds no evidence. S3 adds 1 point for 6 to 10 h, and it still names no decision owner.

## Verdict

**sunk, freeze with summary only.** The kit has no domain angle and no result; 24 h is 40 % of a flagship. Evidence against archiving: the only consumer (`decision-analytics-reconstruction`) hard-codes this repository as its upstream in two workflows, so an archived hub would block its upstream pull requests (inference, not tested). Rafael's standing decision (move to a tooling organisation, career knowledge §7) stays compatible.

## Proposed summary README

Ten lines. Every fact exists in this repository today. The sentence "Repository last updated 2026-09-16" in the current README is stale (last commit 2026-10-27) and must go.

```markdown
# governance-bootstrap
Status: Maintained, frozen. A tool for the author's own projects. It is not a data product.
Coding sessions with an LLM agent repeat fixed mistakes and leave no record of what is still open.
This kit turns each repeated mistake into a YAML file with a check script.
While the file is open, the script only reports. When it is closed, the same script fails the build if the mistake returns.
The kit has 11 checks: hardcoded values in code, notebooks and SQL, config keys, test coverage, complexity, file size, import layers, and a score for risky untested code.
One project uses it today: decision-analytics-reconstruction. Updates move by git subtree and GitHub Actions.
Result: this repository holds no measured before/after number. It shows the mechanism only.
Limits: needs GitHub Actions and an access token. A user can still delete the re-check job. No release tag exists yet.
Start: CONSUMER_SETUP.md. Licence: MIT. Author: Rafael Braga-Kribitz.
```

## Lesson for the next project choice

Name the ad vocabulary and the one number a tool will produce before the first commit. Five of six commit days went to presentation, not to the kit.

## Open questions

1. Rafael's own hours, including the extraction work inside `decision-analytics-reconstruction` (open question 4).
2. Is there a rework-hours before/after number for any consumer? Not in this repository. The sister repository records 62 findings (60 closed, 2 closed historical) and 5 findings with a recorded recurrence (7 recurrences in total) in `governance/AUDIT_STATE.json` and the finding files, but no hours.
3. Is the repository pinned today? The registry does not say. Is the "tooling organisation" move done?
4. Does a frozen `decision-analytics-reconstruction` still need upstream pull requests? If not, archiving costs nothing.
