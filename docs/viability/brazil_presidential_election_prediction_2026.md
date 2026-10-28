# Brazil 2026 Election Forecast: was it worth building?

2026-10-28 · registry: `brazil-2026-election-forecast`, analytical, In development · about 16 h (estimate from git ±50 %: 8 to 24 h)

Scope: 0 applications have been sent (owner statement 2026-10-06). The scores below measure hiring evidence, not conversion. Values come from `docs/viability/_assumptions.md`.

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Commits on `origin/main` | 41 (eb88554) | `git rev-list --count`. The plan file lists 34 to 2026-10-07; it was taken from an older clone. |
| Commit days | 4: 2026-09-29 (25 commits), 09-30 (8), 10-26 (6), 10-27 (2) | `git log`. 33 of 41 commits fall on 2 days. |
| Hours | 4 days × 4 h = **16 h** (8 to 24 h) | Estimate from git ±50 %. The formula probably understates: 25 commits on one day, and an agent-assisted repository. The 2.5 h clean-clone run is compute time, not work time. |
| Size | 59 code files, 154 tracked files, 25,788 words in README, docs and pre-registration | `git ls-files`. The plan file lists 134 Python files; the git count is 59. |
| Cost at €45 per hour | €720 (€280 to €1,440) | `_assumptions.md`: €35 to €60, central €45. |
| After the freeze decision | about 8 h (2 commit days, 2026-10-26 and 10-27) | Scoring of the forecast and the design-system migration. D-034 (2026-10-19) does not name this project. |

## Opportunity cost

| Alternative use of 16 h | What it buys | Source |
|---|---|---|
| Applications | 13 to 16 applications (1 to 1.25 h each), about 1.5 weeks at 8 to 10 per week. The range 8 to 24 h gives 6 to 24. | `_assumptions.md`; 0 sent so far; start 2027-01-04 |
| German | 16 of about 640 h from A1.2 to the B1 exam (2.5 %); 0.8 week of the 20 h per week course | `_assumptions.md`; course from 2026-10-26 |
| Next scored project | 27 % of one flagship. Proxy 60 h = median of 6, 8, 15, 20, 36 commit days × 4 h for the five flagships (estimate from git ±50 %). | D-034: B2B SaaS revenue retention |

All three stay on this page until Rafael answers open question 5.

## Scenarios

Scores: 0 to 2 per item on the shared rubric (`_assumptions.md`, "Scoring rubric for the five hiring-evidence items"; finish cost 2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention). S0 scores the portfolio without this project; the 16 h go to the alternatives above, which this scale does not score.

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no skill shown | 0: nothing added to the public pool | 0: none | 0: none | 2: by convention, no hours at stake | **2** |
| S1 as published today | 1: Python 39 %, statistics 16 % (ads mention, snapshot 2026-10-18); no SQL, Power BI or Azure; data-quality checks (41 of 41 TSE vote counts match) | 2: question in the lead, results, honest misses and a Limitations section, plus data-quality checks; the README has 5,312 words | 0: political forecast, no marketing, customer or Austrian business setting | 0: number (share error 1.06 pp), caveat (first place called wrong) and lesson (freeze missed) exist, but no decision owner (`_prose_measures_2026-10-28.md`: owner no; 68.2 % STE, 5 codes) | 2: 1 to 1.5 h to S2 (recipe estimate); gate already passes, 2 warnings (`_gate_baseline_2026-10-28.txt`, run B) | **5** |
| S2 after this plan | 1: unchanged | 2: top box shows question, result and limits in the scarce README style | 0: a rewrite cannot add a domain | 0: the summary names no decision owner; none exists in the target market | 2: 0 h left | **5** |
| S3 extended: TSE reading replaces secondary results, plus an addendum on the missed freeze | 1: unchanged | 2: unchanged | 0: unchanged | 0: addendum gives an honest process story, no new number that matters and no decision owner | 1: 2 to 3 h on top of S2 (assumption, no log; central 2.5 h) | **4** |

S2 adds no point: the summary only shortens the README. S3 does not pay: it adds 2 to 3 h and loses 1 point.

## Verdict

**Sunk, freeze with summary only.**

## Proposed summary README

Replace the 5,312-word README with this text if Rafael accepts the verdict. Every fact comes from the current README.

```
# Brazil 2026 Election Forecast
Status: experiment finished and frozen. The 2026 scoring is UNREGISTERED.
Question: how accurate and how well calibrated is a pre-registered Bayesian poll aggregation, compared with a 14-day poll average, when each forecast uses only information available at the time?
Method: PyMC random-walk model on public poll tables, tested leave-one-election-out on 2014, 2018 and 2022 (6 rounds). The design is fixed in PREREG.md with 6 dated addenda.
Backtest: share error 1.38 pp against 2.07 pp for the poll average (eve horizon). First-place probabilities were worse (Brier 0.075 against 0.034), so criterion H3 is not met.
2026 (preliminary forecast, cutoff 2026-09-29): first-round share error 1.06 pp; all 6 results inside the 80 % intervals; first place called wrong (36 % for the candidate who finished first); Lula elected with 51.79 % of valid votes, inside the runoff 80 % interval.
Limits: 3 historical elections only; the registered freezes of 2026-10-03 and 2026-10-24 did not happen; results are secondary-source counts pending the TSE reading.
Data: public Wikipedia poll tables pinned by revision (CC BY-SA 4.0); results reconciled to TSE files (41 of 41 vote counts match).
Reproduce: uv sync --locked; make test; make reproduce (about 2.5 h from a clean clone, tested 2026-09-29/30).
Decision: no further work. The repository shows method discipline, not a domain project. Licence: MIT (code).
```

## Lesson for the next project choice

Write the persona line before the first commit. If it names nobody in the Austrian target market, cap the project at 8 h or do not start. Book the one dated step an event-bound project depends on (here the 2026-10-03 freeze) before any modelling work.

## Open questions

| # | Question | Why it matters |
|---|---|---|
| 1 | What are your own hours for this project? | The git formula gives 16 h and probably understates (open question 4). |
| 2 | Why did the 2026-10-03 and 2026-10-24 freezes not happen? | The README promises an addendum with the reason; none exists. |
| 3 | Is the repository pinned or public on GitHub, and does any decision cover it? | Knowledge files hold no decision for this project; the verdict needs a pin decision. |
| 4 | How many ads mention forecasting, Bayesian methods or PyMC? | The core file has no share. The CV lists forecasting as "have" with no public evidence (full file §1), so this repository is the only public evidence. The weekly archive can answer. |
| 5 | Which alternative counts as the opportunity cost for 2026? | Plan open question 5. |
| 6 | Do media or polling employers appear in the Austrian job archive? | The market file has no such category; a yes would change the domain score. |
