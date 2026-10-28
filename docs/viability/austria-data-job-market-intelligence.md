# austria-data-job-market-intelligence: was it worth building?
2026-10-28 · status in registry: Complete · hours: 24 h (range 12–36 h), estimate from git ±50 % (owner log not supplied)

Outcome measure: 0 applications have been sent (owner statement 2026-10-06, still true on 2026-10-28). No conversion data exists. Every score below is a hiring-evidence score, not a conversion. Values and units: [`_assumptions.md`](_assumptions.md).

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Hours | 6 distinct commit days × 4 h = 24 h (12–36 h) | Public default branch `main` at 1648808: 31 commits, 6 commit days, 80 code files (.py/.js). Estimate from git ±50 %. |
| Period | 2026-09-17 to 2026-10-27 (commits); work started by 2026-09-16 | The public decision log dates its first 15 decisions 2026-09-16. |
| Caveat 1 | The estimate is a lower bound | The first public commit is one squashed export: 220 files, 31,784 lines. The public decision log also dates work on 2026-09-16 and 2026-09-18, which have no commits. With those 2 days: 32 h. |
| Caveat 2 | Agent-assisted work inflates commit counts | 11 commits on 2026-10-26 alone. Commit count is not used. |
| Caveat 3 | The plan file's git table does not match the public branch | Plan: 28 commits, 2026-09-16 to 2026-10-19, 136 Python files. Public `main`: 31 commits, 2026-09-17 to 2026-10-27. This page uses the public branch only. |

## Opportunity cost

All three alternatives are shown until Rafael answers open question 5.

| Alternative | What 24 h (12–36 h) buys instead | Source |
|---|---|---|
| Applications | 19 to 24 applications (10 to 36 over the hours range), about 2.5 weeks at 8 to 10 per week. The career knowledge advised a low-volume track of about 3 per week from late September 2026. That track did not start: 0 sent. | `_assumptions.md` (1 to 1.25 h per application); `career-knowledge-full.md` §5 item 9 |
| German study | 24 h ≈ 3.75 % of the ~640 h from A1.2 to the B1 exam; about 1.2 weeks of the 20 h/week course load | `_assumptions.md` |
| Next scored project (B2B SaaS revenue retention, D-034) | 24 h ≈ 40 % of one flagship. Proxy: median of the five flagships = 15 commit days × 4 h = 60 h (days: 6, 8, 15, 20, 36) | git on the five public default branches, 2026-10-28; proxy, labelled |

Best alternative at the time (September 2026): applications. Only the application log turns ad patterns into hiring evidence (README, "What I would do with production data").

## Scenarios

Scores 0 to 2 per item, total /10, on the shared rubric (`_assumptions.md`, "Scoring rubric for the five hiring-evidence items"). Market shares: snapshot 2026-10-18, n = 699 core ads, "ads mention".

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no project; hours go to an alternative above | 0: no evidence shown | 0: none | 0: targeting by gut; no evidence behind "Graz + Vienna hybrid" or the skip list | 2: by convention, no hours at stake | 2 |
| S1 as published today (`main` 1648808) | 2: Python (39 %), ETL pipeline (20 %), data-quality audits (31 %), statistics (16 %: Wilson intervals, robust OLS), Power BI project (17 %). SQL (40 %) only in one SQLite query (`src/analysis/supplement_radar.py`); no cloud (32 %) | 2: README has question, result and limits (gate PASS_WITH_EXCELLENCE, `_gate_baseline_2026-10-28.txt` run B), plus data quality (hand-labelled precision 83 %/95 %, export guard) and a Power BI semantic model (72 measures). No SQL warehouse, no Azure | 1: Austrian and Styrian setting, but labour market, not marketing/customer/e-commerce | 0: number (Vienna 45 % of 699 ads; 147 English-no-German ads) and caveat (one-day stock, small Styrian n) exist, but the README names no decision owner; 72.3 % STE, 6 internal codes (`_prose_measures_2026-10-28.md`) | 2: plan budgets 2 h to reach S2 | 7 |
| S2 after this plan (README rewritten, gate green) | 2: unchanged; the rewrite adds no SQL | 2: unchanged; the rewrite makes the README form (question → result → limits → decision) easier to read | 1: unchanged | 2: top box with decider, decision, answer, caveat; rewritten README names the owner, 99.6 % STE, 0 codes (`_prose_measures_2026-10-28.md`) | 2: 0 h left | 9 |
| S3 extended (second candidate-supply snapshot, the README's next milestone) | 2: unchanged | 2: unchanged | 1: unchanged | 2: a time axis for supply adds little to a 2-minute story | 1: 6 to 10 h on top of S2: GitHub re-collection about 5–7 h at API limits (README, Reproduce), plus re-analysis and re-export (assumption 1 to 3 h) | 8 |

## Verdict

**worth it, keep.** S2 (9/10) is the best scenario, and it costs about 2 h. The project is the source of the decisions in force: Graz + Vienna hybrid, English-written ads, the skip list, and the D-034 choice of SaaS (32 reachable ads). The weekly refresh (D-031) keeps it current. Do S2 now. Do not do S3 before 2027-01-04, because S3 scores lower than S2.

## Lesson for the next project choice

The project found that SQL is the most-mentioned and the scarcest skill (40 % of ads, 10 % of observed candidates), but it shows SQL in one query only. Build the SaaS retention project on SQL over a modelled schema. An information project pays only when its advice is used: start the application log.

## Open questions

1. Real hours (open question 4). The public history starts with a squashed export, and the private repository is out of scope.
2. Which alternative counts as the opportunity cost (open question 5).
3. Why the low-volume application track (about 3 per week from late September) did not start, and when the log will start.
4. Do recruiters read a project about the author's own job market as business-relevant? No data. The `portfolio_version` field of the application log can test it after about 40 rows.
5. Which clone produced the plan file's git table (28 commits, 136 Python files)?
6. Skill recall is not measured (README, Validation). The size of the "wrong advice" risk is therefore unknown.
