# NextMove: was it worth building?

2026-10-28 · registry: application, In development · hours: about 48 h (24 to 72), estimate from git ±50 %

0 applications have been sent. The outcome is therefore a hiring-evidence score (0 to 2 on five items), not a conversion. Values and sources: `docs/viability/_assumptions.md`. Base: `origin/master` at 1ec5fd0. The plan file lists NextMove as "no README, 91 commits". That came from a local clone 41 commits behind. On origin/master the README exists and the gate audit passes.

## Cost

| Item | Value | Source and caveat |
|---|---|---|
| Distinct commit days | 12 (first 2026-07-24, last 2026-10-28) | `git log origin/master`; 132 commits, 127 code files, 445 test functions in 52 test files |
| Hours | 12 × 4 h = 48 h (24 to 72) | Estimate from git ±50 % (`_assumptions.md`). Replace with Rafael's log (open question 4). |
| Three bursts | 2026-07-24 to 08-05: planning and Phase 1 (91 commits, 4 days). 2026-09-16 to 09-21: README and registry (9 commits, 3 days). 2026-10-14 to 10-28: engine, mart, report, polish (32 commits, 5 days). | Between 08-05 and 09-16 nothing was committed (6 weeks). |
| Authors | Rafael Braga-Kribitz 105, Claude 26, Cursor Agent 1 | The author name does not show who typed. 17 of the 19 commits on 10-14 and 10-15 are by "Claude". The October agent loop probably lowers true human hours. The 18-paper research corpus and 10 planning documents pre-date the first commit and are not counted. |

## Opportunity cost

Rafael has not yet said which alternative counts (open question 5). All three are shown. Each row converts 48 h (24 to 72).

| Alternative | What 48 h buys | Source |
|---|---|---|
| Applications not sent | 38 to 48 applications at 1.0 to 1.25 h each (range 19 to 72). That is 4 to 6 weeks at 8 to 10 a week. | `_assumptions.md`, D-035 |
| German hours | 7.5 % of the about 640 h from A1.2 to the B1 exam (3.8 to 11.3 %). B1 alone is named enough in 6 ads (snapshot 2026-10-18). | `_assumptions.md`, owner-stated 2026-10-12 and 2026-10-19 |
| Next scored project | 0.8 of one flagship. Proxy: median of five flagships' commit days (6, 8, 15, 20, 36) = 15 days = 60 h (30 to 90), estimate from git. The next scored project is B2B SaaS revenue retention (D-034). | `_assumptions.md`, D-034 |

The three commit days after D-034 (2026-10-26 to 10-28: design-system charts, CI pin) cost about 12 h (6 to 18). NextMove is not on Track A (about 26 h before 2027-01-04).

## Scenarios

Rubric and finish-cost rule: `_assumptions.md`, "Scoring rubric for the five hiring-evidence items" (2 = 2 h or less left, 1 = more than 2 h and up to 10 h, 0 = more than 10 h; S0 = 2 by convention). Market shares: "ads mention", snapshot 2026-10-18, core n = 699.

| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
|---|---|---|---|---|---|---|
| S0 not built | 0: no repo with experiment design or customer decisions | 0: adds nothing | 0: marketing domain only via the MMM repo | 0: no e-commerce story | 2: by convention, no hours at stake | 2 |
| S1 as published today | 2: SQL mart with SQL tests, Python, quarantine gates, A/B/n test; ads mention SQL 40 %, Python 39 %, data quality 31 %, ETL 20 % | 2: star schema, data-quality report, README with limits and decision (3 of 6 scarce items); no Power BI file | 2: e-commerce CRM; marketing analytics has 18 ads nationally, 0 in Styria | 1: owner ("a CRM team", in the Decision summary), number (+€2,909 vs the rules playbook, 92 % of redeemed discounts wasted) and caveat (simulated; the engine only ties do-nothing) exist, but the lead names no owner; 7 internal codes, 59.6 % STE (`_prose_measures_2026-10-28.md`) | 1: about 2.5 to 3.5 h to S2 (assumption: README rewrite 1.5 h, as the plan budgets for comparable READMEs, plus 1 to 2 h for GitHub description, topics and visibility, this page); gate PASS (`_gate_baseline_2026-10-28.txt`, run B) | 8 |
| S2 after this plan | 2: unchanged | 2: unchanged | 2: persona named in the top box | 2: owner, number and caveat (simulation only) fit in 2 minutes; rewritten README names the owner, 0 codes, 95.1 % STE | 2: 0 h left | 10 |
| S3 extended: Power BI page built from the kit (`reporting/powerbi/`) | 2: adds Power BI (ads mention 17 %); the item is already at 2 | 2: 4 of 6 scarce items | 2: unchanged | 2: unchanged | 1: 5 to 8 h on top of S2 (assumption, judgement; kit has model, 72 lines of DAX, layout) | 9 |

The plan moves the score from 8 to 10: the rewrite names the owner, removes the codes and closes the finish work. S3 scores 1 point below S2: demand match and scarcity are already at 2, and the `.pbix` costs 5 to 8 h. The MMM repo already carries a planned Power BI page in Track A.

## Verdict

**Worth it, finish then freeze.** The 48 h are spent. The finish work is small. The planner's prior "open: half-built flagship" does not hold: milestones M-A to M-F are ticked, CI is green on 1ec5fd0, and the gate passes.

* Finish (about 1 to 2 h): change the GitHub description and topics; decide visibility; check the repo against D-034 so no new module starts.
* Optional after the MMM Power BI page: build the `.pbix` from the kit (S3, 1 point below S2 on this rubric).
* Freeze: no item from the "Later" list in `docs/MILESTONES.md`.
* Change the verdict if: the application log (about 40 rows) shows no response from e-commerce or CRM ads, then freeze at S1 and do not build S3.

README recipe edits needed most (rank order):

1. Rename about 24 code mentions (AC-6, AC-11, AC-12, ADR-004 to ADR-012, DEBT-001 to DEBT-005, M-A to M-F, "3WD" five times) to plain names with a legend. Recipe step 3.
2. Add who decides to the top box (CRM manager at an online retailer). Keep the caveat "simulation only; the engine ties do-nothing" in the first five lines. Recipe step 2.
3. Shorten sentences: 29.8 % of 47 prose sentences exceed 25 words; 59.6 % STE (`_prose_measures_2026-10-28.md`, published README). Recipe step 5.
4. Move "Method" below "Limitations". Recipe step 4.

## Lesson for the next project choice

Write the market-fit check and the first number before the first commit. ADR-011 narrowed the charter on 2026-10-14, after Phase 1 had stalled for 6 weeks, and the result that carries the story (92 % wasted discounts) is the two-week version of the whole project. `.planning/PROJECT.md` named a hiring manager as the customer and "none" as the revenue model.

## Open questions

1. Rafael's own hours per period (open question 4). The October agent loop makes the git estimate uncertain.
2. Is a `.pbix` wanted, given the MMM Power BI page? No hours exist in the repository.
3. Visibility: the 2026-09-17 decision says "private until finished"; the repository is public. Is it finished?
4. Do Austrian ads mention next-best-action, personalization or uplift? The knowledge files do not say. Check the job archive before S3.
5. Which opportunity cost counts: applications, German, or the SaaS retention project (open question 5)?
