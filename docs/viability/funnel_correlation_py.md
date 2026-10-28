# funnel_correlation_py: was it worth building?

2026-10-28 · registry status: Functional (type library) · hours: about 24 h, estimate from git ±50 % (12 to 36 h)

Outcome measure: 0 applications have been sent (owner statement 2026-10-06). No conversion data exists. This page scores hiring evidence, 0 to 2 on five items, not conversions. Assumptions: `docs/viability/_assumptions.md`.

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Commits on `origin/main` | 18 (5 by an agent; merges of agent branches add more) | `git rev-list --count`, base c7427ec |
| Distinct commit days | 6: 2026-02-25, 09-16, 09-17, 09-21, 10-26, 10-27 | `git log`, first day 2026-02-25, last day 2026-10-27 |
| Python files | 15 tracked (4 modules, 1 package init, 5 empty package stubs, 4 test files and a test init) | `git ls-files` |
| Hours | 6 days × 4 h = **24 h**, range 12 to 36 h | estimate from git ±50 % (`_assumptions.md`) |
| Money | 24 h × €45 per hour = **€1,080** (€420 to €2,160) | rate €35 to €60, central €45 (assumption) |

Caveat 1: one init commit (2026-02-25) holds all four modules and the tests, about 1,900 lines of Python. Git cannot show the time spent before that commit, so 24 h may be too low for the build.
Caveat 2: 5 of the 6 days are README, quality-gate, design-system and pandas 3 repair work. Agents made several of those commits. Agent work is not Rafael's hours.

## Opportunity cost

The same 24 h (12 to 36 h) could have bought:

| Alternative | What 24 h buys | Source |
|---|---|---|
| Applications | 19 to 24 applications at 1 to 1.25 h each, or about 2.4 weeks of the 10 h per week application block. 0 sent as of 2026-10-28. | `_assumptions.md`; D-035 |
| German | 24 h = 3.8 % of about 640 h from A1.2 to the B1 exam; at 20 h per week, 1.2 weeks (0.15 of one 8-week sublevel step). | `_assumptions.md`; owner statements 2026-10-12, 10-19 |
| Next project | 40 % of one flagship. Proxy for the next project (B2B SaaS retention): median of five flagships = 15 commit days × 4 h = 60 h (days: 6, 20, 36, 8, 15). Labelled proxy. | `_assumptions.md`; D-034 |

Caveat: the init commit (February) predates the application and German tracks, so the first day had no planned alternative. The two days on 2026-10-26 and 2026-10-27 (about 8 h) fall inside the current plan.

## Scenarios

Market shares: ads mention (snapshot 2026-10-18, core n = 699). Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention).

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: nothing shown | 0: nothing shown | 0: nothing shown | 0: no story | 2: by convention, no hours at stake | **2** |
| S1 as published today | 1: Python 39 %, statistics 16 %, pandas 3 %, R 7 %; no SQL or data quality in the repo | 1: part of the scarce README form: a problem line, a demo result in a chart caption (r = 0.33) and a Limitations section, but no stated question; 47 test functions; pool is crowded with notebooks | 1: demo is a bank telemarketing table (customer outcome); no Austrian setting; marketing analytics 0 ads in Styria | 0: no decision owner (the prose measure's "owner yes" matches "bank-marketing" in a chart caption, not a role), no "what I would do differently"; a port of a free R package | 2: plan file says 45 min to reach S2 | **5** |
| S2 after this plan | 1: same skills, now visible in the first screen | 2: question, result and limits in the order the pool lacks | 1: same demo data | 0: opens with a question and a finding (r = 0.33 and 0.28); still no decision owner (an analyst who screens traits is a user, not a decider) | 2: 0 h left | **6** |
| S3 extended (worked churn example on the bundled telco table, pre-decision traits only, with a stability check of the ranking; about 6 h, assumption) | 1: same | 2: same | 1: customer retention; links to D-034 SaaS retention, still public data | 2: owner, number, caveat, next step | 1: about 6 h (3 to 8 h, assumption) on top of S2 | **7** |

S3 adds 1 point over S2 for about 6 more hours: the story gain (+2) outweighs the finish-cost loss (−1).

## Verdict

**sunk, freeze with summary only.** S1 to S2 buys +1 point for 0.75 h. S3 buys 1 more point for about 6 h (assumption), the time of about 5 to 6 applications. Ads mention tools (Python 39 %), not libraries. The repo has no named decision owner and no Austrian domain. Keep it public, do not pin it, add the summary below.

## Lesson for the next project choice

Write the business case first. Name the decision owner, the euro stake and a free alternative (here the R package). A port of a free tool with no named user gives no interview story. Cap such a project at one day (8 h) unless the story is written first.

## Proposed summary README

```
# funnel-correlation-py
A small Python library. It ranks which traits move with a yes/no outcome.
It is a port of the R package correlationfunnel (Business Science) to pandas.
Question: which traits should an analyst check first, before building a model?
How: binarize() makes 0/1 flags. correlate() gives Pearson r per flag. plot_correlation_funnel() draws the ranking.
Demo result: on a 4,521-row bank telemarketing table, top-quartile call duration has r = 0.33 with a term deposit. A successful earlier campaign has r = 0.28.
Caveat: association is not cause. Check that a top driver is known before the decision is made.
Limits: binary targets only, no missing values, no dates. The bundled tables are public examples, not a client funnel.
Status: Functional, v0.1.0, 47 unit tests, MIT. Frozen: no new features planned.
Start: pip install -e . then open notebooks/01_example_usage.ipynb.
```

## Open questions

| # | Question | Why it matters |
|---|---|---|
| 1 | Rafael's own hours (brief question 4). How long did the code take before the init commit? | Git shows 24 h; the true build may be higher. |
| 2 | Is the repo public and pinned? The knowledge file (section 14) says "make private until finished" for this repo; the registry lists it as published. Which rule holds? | Decides unpin versus private (brief question 1). |
| 3 | Did anyone check for an existing Python alternative before the build? The repository does not say. | Decides the "buy" branch in the business case. |
| 4 | Is the top driver DURATION known only after the call? This needs the dataset notes, which are not in the repository. | If yes, the demo result is a leak, and the summary caveat must name it. |
| 5 | Which alternative is the opportunity cost for 2026 (brief question 5)? | All three are shown until he answers. |
| 6 | Tests were not re-run: `bk_theme` (the bk-viz GitHub dependency) is not installed here. "47 tests" is a count of test functions and the commit message of 4dd29d7. | Verify before the summary is published. |
