# decision-analytics-reconstruction: was it worth building?
2026-10-28 · registry status: Complete (frozen by D-034, summary only) · hours: 144 h, range 72 to 216 h (estimate from git ±50 %)

Outcome measure: 0 applications have been sent (owner statement 2026-10-06). So this page scores hiring evidence, not conversions.
Values for hours, rate and opportunity cost come from [`_assumptions.md`](_assumptions.md).

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Commits on `origin/main` (b530214) | 445 (96 merges) | `git rev-list --count`. 98 commits have the author "Claude", 1 "Cursor Agent", 8 a sync bot. Agent work inflates the count. |
| Distinct commit days | 36 | 29 of the 36 days fall from 2026-05-07 to 2026-07-19. The rest: 4 days in Sep, 3 days in Oct. |
| First and last commit day | 2026-05-07 to 2026-10-27 | 12 commits on 2026-10-26/27 came after D-034 (2026-10-19): design-system re-render and the decision KPI panel. |
| Code files (.py/.ts/.tsx/.js) | 408 | `git ls-files`. 175 tracked files sit in `governance/`. |
| Hours | 144 h (72 to 216 h) | 36 days × 4 h, estimate from git ±50 %. Not a measured number (open question 4). |
| Hours in governance work | about 60 % of commits | 209 of 349 non-merge commit subjects name governance, findings, audit, CI or debt. Keyword count, a heuristic only. |
| Money value of the hours | €6,480 (€2,520 to €12,960) | 144 h × €45 (72 h × €35 to 216 h × €60), `_assumptions.md`. |

The plan file lists 399 commits to 2026-08-20. That table came from an older clone. This page uses `origin/main` on 2026-10-28.

## Opportunity cost

All three alternatives stay until Rafael answers open question 5.

| Alternative | What 144 h (72 to 216 h) buys | Basis |
|---|---|---|
| Applications | 115 to 144 applications (range 58 to 216), about 12 to 18 weeks at 8 to 10 per week | 1 to 1.25 h per application, `_assumptions.md` |
| German | 22.5 % of the A1.2 to B1 path (range 11 to 34 %), about 7 weeks at 20 h per week | 640 h path, `_assumptions.md` |
| Next scored project (B2B SaaS revenue retention, D-034) | 2.4 projects of median size (range 1.2 to 3.6) | Proxy: median git estimate of the five flagships = 15 days × 4 h = 60 h (days: 6, 8, 15, 20, 36; local worktrees, 2026-10-28) |

## Scenarios

Score 0 to 2 per item on the shared rubric (`_assumptions.md`, "Scoring rubric for the five hiring-evidence items"). Market shares: "ads mention", snapshot 2026-10-18, core n = 699.

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no project; the hours go to an alternative above | 0: no project | 0: no project | 0: no project | 2: by convention, no hours at stake | 2 |
| S1 as published today | 1: Python 39 %, statistics 16 %, data quality 31 % (pandera, schema contracts); no SQL (0 `.sql` files, no SQL library), no Power BI 17 %, no Azure 19 % | 2: README has the question in the lead, a result ($766k moved, +1.20 %) and a Limitations section, plus data-quality gates; Bayesian and ML content is crowded; no SQL, Power BI or Azure | 0: Paraguay election campaign; no marketing, customer or Austrian business setting | 1: first screen has a decider ("a campaign", no role), a decision, a number ($766k moved, +1.20 %) and a caveat; 16 internal codes (Module A/B/C, F-021) and jargon (MILP, HDI) hide them; 79.3 % STE (`_prose_measures_2026-10-28.md`) | 2: gate PASS_WITH_EXCELLENCE, 1 warning (`_gate_baseline_2026-10-28.txt`, run B); plan budget 1 h | 6 |
| S2 after this plan | 1: no new skill; same evidence | 2: same README form; plain language makes it easier to read | 1: summary names the transfer to regional budget allocation (case study, "Domain transfer") | 2: owner, decision, number, caveat and "what a campaign would do differently" in 2 minutes; 0 codes | 2: 0 h left | 8 |
| S3 extended (SQL + Power BI view of the allocation table) | 2: adds SQL 40 % and Power BI 17 % | 2: SQL and Power BI are on the scarcity list | 1: unchanged | 2: unchanged | 0: judgement 8 to 20 h on top of S2 (central 14 h); breaks the D-034 freeze; the MMM project already carries the Power BI page | 7 |

S3 scores 1 point below S2. That supports the freeze.

## Verdict

**sunk, freeze with summary only.**

* The cost is the largest of the five flagships: 144 h against a median of 60 h (estimate from git ±50 %).
* About 60 % of commits are governance and audit work. Ads in the snapshot do not name these skills.
* The project shows no SQL, no Power BI and no Azure, the main gaps in the ads.
* The project now has a business result. The budget module moves $766k of a $6.03M plan at week 8 (ILLUSTRATIVE, contacts, not dollars). So the summary costs about 1 h and the interview story reaches 2.

Difference from the planner's prior (same verdict, other reasons):

| Prior says | Repository shows |
|---|---|
| "Today the only result is a model check" | The README leads with the decision KPI panel since 2026-10-26. The week-8 replay is in `reports/CASE_STUDY.md` since 2026-07-15. |
| "399 commits" | 445 commits to 2026-10-27 on `origin/main`. |
| "No business domain" | The domain is political, but the budget module is a region × channel budget allocation under a fixed envelope. It is a framing problem, not a missing result. |

## Proposed summary README

Proposal only. The README is not changed. If it replaces the README, run the gate again.

```markdown
# Campaign budget allocation under uncertainty: Paraguay 2018 (reconstruction)
**Who decides:** a campaign manager with a fixed budget of $6M (a planning assumption in the repository, not audited spend).
**Decision:** how to split the budget across 18 departments and 11 channels, and when to change the plan as the polls move.
**Answer:** at week 8 the tracked lead grew from +8.6 pp to +17.7 pp. A new plan moves $766k from the six swing departments to strongholds and opposition departments.
**Value:** +1.20 % more persuasion-weighted contacts than the old plan. This is an illustrative scenario in contacts, not dollars, and not a causal claim.
**Main caveat:** at the low edge of the 94 % interval the shift reverses. Every voter record is synthetic, and only 8 real polls exist.
**Model check:** the model is checked against the known result (+3.70 pp, turnout 61.25 %). In a hold-out test, 3 of 6 polls fell inside the 95 % band.
**What a campaign would do differently:** feed the poll tracker into the budget plan every week (today a manual replay), and estimate channel response from real spend.
**How it works:** Voter segments and turnout (scikit-learn) → Campaign budget allocation (an optimisation model in PuLP) → Poll tracking and scenarios (Bayesian, PyMC). `make pipeline-full` runs all three.
**Status:** complete and frozen. Detail: `reports/CASE_STUDY.md`, numbers: `reports/NUMERIC_SSOT.md`. MIT licence.
```

## Lesson for the next project choice

Write the decision owner, the money at stake and the first business number before the first commit. Cap governance work at a fixed share of the hours.

## Open questions

1. Rafael's own hours for this project (open question 4). The 144 h is an estimate from git ±50 %.
2. Which alternative counts as the opportunity cost (open question 5).
3. Do the 12 commits of 2026-10-26/27 count as the D-034 "DAR summary" step, or as work past the freeze?
4. Do ads in the snapshot mention optimisation (linear programming) or Bayesian methods? The knowledge files give no share. Statistics (16 %) is the nearest marker.
5. The plan file's git table (399 commits to 2026-08-20) is stale. Update it from `origin/main`?
6. Does the 10-line summary replace the README, or go above it as the top box?
