# governance-bootstrap: business case, written as of 2026-06-09

Persona: engineering lead of a small data team (3 to 8 people) at a mid-sized company (assumption). Decision owned: adopt a governance kit for the team's repositories, or not. Cycle: one adoption decision, reviewed yearly; effects counted per quarter. Sign-off: head of data or IT (assumption).

Shared values (rate, hours rule): `docs/viability/_assumptions.md`. Every probability below is an assumption. Rework hours are an assumption: no repository number exists.

## Money at stake per decision cycle

| Item | Central | Range | Unit | Source |
|---|---|---|---|---|
| People who write code in data projects | 5 | 3 to 8 | people | assumption (judgement: "small team") |
| Working weeks | 46 | - | weeks per year | assumption |
| Re-found and re-fixed problems (hardcoded values, broken config, regressions) | 1.0 | 0.5 to 2.0 | h per person-week | assumption (judgement; no public benchmark found) |
| Team rework | 230 (57.5 per quarter) | 69 to 736 | h per year | 5 × 46 × 1.0 |
| Cost of rework | 10,350 | 2,415 to 44,160 | EUR per year | hours × loaded rate EUR 45 per h (EUR 35 to 60), `_assumptions.md` |
| Share a used kit avoids | 30 % | 15 to 50 % | of rework | assumption (judgement) |
| Avoidable rework | 69 h per year (17 per quarter) | 10 to 368 h per year (3 to 92 per quarter) | h | product of rows above |
| Avoidable cost | 3,105 | 362 to 22,080 | EUR per year | product of rows above |

## Status quo

Code review, ad-hoc audits, and a discipline copied by hand between projects (the bootstrap prompt names `warehouse_humanoid_tco` as the source). Agent coding sessions invent audits, call work closed and keep no state (the project's premise; frequency is an assumption: 1.0 h per person-week above). Cost of the status quo: EUR 10,350 per year (EUR 2,415 to 44,160), assumption.

## Options

3-year horizon (judgement: tool shelf life). Net EV = 3 × yearly EV − 3-year cost, central case. Time to answer is calendar time at part-time (assumption).

| Option | Cost (one-time + run) | Time to answer | Net EV, 3 years | Note |
|---|---|---|---|---|
| Do nothing | EUR 0 | 0 | EUR 0 | Keeps the rework above |
| Buy: ready-made linters (pre-commit, ruff, radon, coverage, import-linter) | EUR 945 + EUR 180 per year | 1 to 2 weeks | +EUR 1,129 | 12 h setup + 3 projects × 3 h. Avoids 20 % of rework. Keeps no open-finding state |
| Build small: one Makefile, the ratchet helper, 3 gates, one agent protocol file, copy once | EUR 765 + EUR 180 per year | 2 weeks | +EUR 1,464 | 8 h + 3 projects × 3 h. Avoids 25 %. Wraps the bought linters |
| Build full: hub repo, 11 gates, two-way sync, fan-out, bootstrap prompt | EUR 1,890 + EUR 360 per year | 4 to 6 weeks | -EUR 682 | 24 h (12 to 36, estimate from git ±50 %) + 3 projects × 6 h. Avoids 30 % |

## Outcome tree for "build full"

Values are per year, central. Branch ranges are not additive; the range in the sum row uses a pessimistic and an optimistic corner case (probabilities 15/25/50/10 and 45/25/20/10).

| Branch | Probability (range, basis) | Value if it happens (EUR per year, basis) | Probability × value |
|---|---|---|---|
| Changes behaviour and pays off | 30 % (15 to 45 %), judgement | +3,105 (362 to 22,080): avoidable cost above | +932 |
| Confirms the status quo | 25 % (15 to 35 %), judgement | +360 (280 to 480): 2 h per quarter of review time saved, assumption | +90 |
| Built but not adopted by the team | 35 % (20 to 50 %), judgement: gates and sync need a token and discipline | 0 | 0 |
| Wrong: false alarms slow the team | 10 % (5 to 20 %), judgement | -2,588 (-1,208 to -5,520): 0.25 h per person-week × 5 × 46 × EUR 45, assumption | -259 |
| Sum | 100 % | | EV before cost +763 per year (4 to 9,504) |

## Cost

| Item | Value | Basis |
|---|---|---|
| Build | 24 h × EUR 45 = EUR 1,080 (EUR 420 to 2,160) | git hours estimate for the scope, ±50 %; rate EUR 35 to 60 (anchor: advertised analytics floor EUR 50.0k per year × 1.3 ÷ 1,700 h ≈ EUR 38 per h, snapshot 2026-10-18) |
| Onboarding | 6 h × 3 projects × EUR 45 = EUR 810 | assumption (3 projects) |
| Run | 8 h per year × EUR 45 = EUR 360 per year | assumption (token rotation, tag, sync pull requests) |
| Delay cost | EUR 0 | no decision waits for the build |
| First year / three years | EUR 2,250 / EUR 2,970 | sum |

## Result

| Measure | Build full | Build small | Buy |
|---|---|---|---|
| Net EV, 3 years (corner-case range) | -EUR 682 (-4,189 to +26,532) | +EUR 1,464 | +EUR 1,129 |
| Net EV, year 1 | -EUR 1,487 | -EUR 22 | -EUR 254 |
| Payback | about 4.7 years (beyond the horizon) | about 1.0 year | about 1.4 years |
| Break-even chance of "pays off" | 37 % (central 30 %, range 15 to 45 %) | not computed | not computed |

Value of better information: not applicable. The product is a tool, not an information product.

## Sensitivity

Net EV over 3 years at 5 people, by rework per person-week. The verdict flips on this one assumption.

| Rework (h per person-week) | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|
| Build full | -2,079 | -1,380 | -682 | +17 | +716 | +2,113 |
| Build small | +106 | +785 | +1,464 | +2,143 | +2,823 | +4,181 |
| Buy | -113 | +508 | +1,129 | +1,750 | +2,371 | +3,613 |

Flip points: build full beats nothing at 1.25 h or more (team: 6.2 h per week); build small at 0.46 h; buy at 0.55 h. Second assumption: the "pays off" chance must reach 37 % for build full.

## Verdict

**Build small first.** At the central rework level only the small build and ready-made linters have positive 3-year EV (+EUR 1.5k and +EUR 1.1k); the difference between them is inside the noise, and the small build keeps the one thing linters lack, a record of open findings across agent sessions (judgement). Evidence that would change it: a team log showing at least 1.25 h of rework per person-week, or three or more teams ready to take shared updates.

## Calibration against the retrospective

Retrospective verdict (`docs/viability/governance-bootstrap.md`): sunk, freeze with summary only. Agree? Yes on the core: do not build the full kit. The labels differ because the questions differ (company EV versus hiring evidence).

| What the ex-ante view missed | Evidence |
|---|---|
| The kit was an extraction from live work, so cost exceeds 24 h | First commit holds 61 files and 4,414 lines on one day; the sister repository's first governance finding opened 2026-06-08 |
| Adoption stayed at one consumer | `consumers.yaml` lists one project; the repository has no release tag; this matches the "not adopted" branch (35 %), n = 1 |
| Five of six commit days were presentation work | Commit subjects: README, banner, README gate. Not in the cost model |
| A recorded use signal exists, but no hours | The sister repository holds 62 findings, 5 with a recorded recurrence (7 in total, 2026-06-08 to 2026-08-10). At an assumed 2 h per recurrence this is about 1.6 h per week for one developer, above the 1.25 flip point. One developer, assumed 2 h, cost side unmeasured |
| No before/after number in this repository | Open: rework hours were never logged |
