# austria-data-job-market-intelligence: business case, written as of 2026-09-10
Persona: data-career job seeker in Graz who runs his own search as a one-person "company" (Rafael). Decision owned: which role families, skills and cities to target, and which skills the next portfolio projects show. Cycle: one search-strategy cycle, about 3 months (2–6, assumption). Sign-off: Rafael, the only decider.

Why this persona (chosen from the repository on 2026-10-28): the repository holds one seeker profile (`config/profile.json`) and a private log of "the owner's own applications" (`schemas/application_log_schema.md`). It never ranks individuals and has no composite score (README, Method), so a recruiting team's core decision, ranking candidates, is out of scope and against a hard boundary. A career service could use the public aggregates, but the repository has no client or multi-profile workflow.

Rate, hours and opportunity-cost units: [`docs/viability/_assumptions.md`](../viability/_assumptions.md). Every probability below is an assumption.

## Money at stake per decision cycle

| Item | Value | Unit | Source (repo file / public source / assumption + range) |
|---|---|---|---|
| Value of one month in work at the public entry floor | €4.2k (€3.3k–€5.1k) | € gross per month | Public source: AMS Berufslexikon, Data Scientist, collective-agreement entry floor €2,800–4,350 per month × 14 ÷ 12, 2025 basis. Recorded in the repo at `docs/research-landscape.md` §1.4. A floor is not a salary. |
| Value of one search week | €0.96k | € per week | €4.2k × 12 ÷ 52 |
| P(status-quo strategy is mis-targeted) | 30 % (15–50 %) | probability per cycle | Assumption (judgement): career change after about 20 years in marketing, German A2 certificate, a small regional market, no known posting-level data for Austrian data ads |
| Extra search if mis-targeted | 2 months (1–4) | months | Assumption (judgement) |
| Expected loss of the status quo | €2.5k (€0.5k–€10.2k) | € per cycle | 30 % × 2 months × €4.2k |
| Manual market reading per cycle | 10 h (5–20 h) × €45 = €450 (€175–€1,200) | € per cycle | Assumption |
| Portfolio value of the build (second product) | not in the base EV | — | No data before the first application. See Sensitivity. |

## Status quo

| Item | Today (2026-09-10) | Source |
|---|---|---|
| How the decision is taken | Read job boards by hand; prior preference for title and region | Assumption |
| Free public inputs | AMS JobBarometer (yearly ad counts by occupation × state), Cedefop skills dashboards (region level, no download), salary pages that show collective-agreement floors | Public sources (existence check: about 1 h desk work) |
| What they cannot answer | Skills, German statement and advertised floor per ad, at Graz/Styria level | Assumption, to verify in the desk check |
| Cost | €450 per cycle of manual reading, plus the expected mis-targeting loss of €2.5k per cycle | Table above |
| How often it goes wrong | 30 % of cycles (15–50 %) | Assumption |

## Options

| Option | Cost | Time to answer | Expected value | Note |
|---|---|---|---|---|
| Do nothing | €0 | now | €0 (baseline) | The €2.5k expected loss per cycle stays |
| Buy or rent (free public series + spreadsheet tags on about 50 ads) | 6 h (4–10 h) × €45 = €270 | 1 week | €439 (−€0.5k to +€1.4k) | No vendor sells this cut (assumption); sample too small for Styria; no candidate side |
| Build small (2 weeks: one-day snapshot of 2–3 public boards; rule tags for skill, state, German statement, advertised floor; 5 tables, 3 charts; aggregates only) | 10 h (6–16 h) × €45 = €450 | 2 weeks | €653 (−€1.1k to +€1.9k) | Captures about 3/4 of the targeting value (judgement) |
| Build full (ad demand + GitHub candidate supply + demand-vs-supply join, precision audits, tested public export) | €1,080 build + €481 delay = €1,561 | 3–5 weeks | −€63 (−€3.6k to +€2.3k) | Adds "which skills do portfolios rarely show" |

## Outcome tree for "build full"

| Branch | Probability (range, source) | Value if it happens (EUR, source) | Probability x value |
|---|---|---|---|
| Changes the decision and pays off | 0.20 (0.10–0.35); judgement: 30 % mis-targeted × about 2/3 that the tool finds it and the seeker acts | €8,334 (€3.3k–€20.3k): 2 months (1–4) of search avoided × €4.2k | €1,667 |
| Confirms the status quo | 0.55 (0.45–0.55); remainder | €450 (€175–€1,200): manual reading avoided | €248 |
| Built but not adopted | 0.15 (0.10–0.20); judgement: the owner is the user, but the answer can come after the search starts, or be ignored | €0 | €0 |
| Wrong, decision gets worse | 0.10 (0.10–0.15); judgement: rule-based tags, one-day stock, small regional counts | −€4,167 (−€1.6k to −€10.2k): 1 month (0.5–2) of extra search | −€417 |
| Sum | 1.00 | | **€1,498 EV before cost** (€456–€2,703; probabilities varied, branch values central) |

Value of better information: EV with the full tool − EV without = €1,498 per cycle (small build: €1,103).

## Cost

| Item | Value | Source |
|---|---|---|
| Build hours | 24 h (12–36 h) | Estimate from git ±50 %, used as the forecast (`_assumptions.md`) |
| Loaded rate | €45 per hour (€35–60) | `_assumptions.md`, which anchors it on the advertised analytics floor (marker `floor_analytics_eur`, snapshot 2026-10-18). That marker is a later output of this project. Ex-ante check: public entry floor €39.2k–€60.9k per year × 1.3 ÷ 1,700 h = €30–47 per hour; consistent. |
| Build cost | €1,080 (€420–€2,160) | hours × rate |
| Run cost | €0 in one cycle; about €720 per year if refreshed quarterly (4 h × 4 × €45) | Assumption; a refresh is a separate decision |
| Delay cost | €481 (€0–€1,924): 0.5 week (0–2) of search delay × €962 | Assumption: applications can run in parallel; the risk is waiting for the answer |

## Result

EV(build full) = €1,498 − €1,561 = **−€63 per cycle (−€3.6k to +€2.3k)** · payback ≈ 1.0 cycle (about 3 months) · break-even probability of "pays off" = 0.21 (assumed 0.20) · EV(build small) = €1,103 − €450 = **€653 (−€1.1k to +€1.9k)**, payback ≈ 0.4 cycle.

## Sensitivity

| Assumption | Base | Flips at | Effect |
|---|---|---|---|
| Portfolio value of the full build over the small build | €0 (not in base EV) | > €717, i.e. the full build shortens the search by more than 0.75 week (about 4 working days) | Build full beats build small |
| P(status quo mis-targeted) | 30 % | > 31 % (build hours fixed at 24 h) | EV(build full) turns positive |
| Build hours | 24 h | < 23 h at €45 | EV(build full) turns positive |

## Verdict

**Build small first.** The small build gives about 3/4 of the targeting value for less than half the cost; the full build only breaks even on information value. Evidence that would change it: a first snapshot that shows the status quo is clearly mis-targeted, or a reason to expect the full build to shorten the search by about a week as a portfolio piece.

## Calibration against the retrospective

| Item | Finding (learned after 2026-09-10) |
|---|---|
| Retrospective verdict | worth it, keep (S1 7/10, S2 9/10), [`docs/viability/austria-data-job-market-intelligence.md`](../viability/austria-data-job-market-intelligence.md) |
| Agree? | Partly. The project did start small: the public decision log scopes demand only on 2026-09-16 and adds the supply and join layers on 2026-09-17. Then it grew in one day. |
| Missed 1: the second product | The repository became the first pinned flagship (D-034) and the base of the weekly refresh (D-031), the career-knowledge markers, the D-034 project scores and the D-036 pipeline. The tree had no reuse or option value. |
| Missed 2: the "changes the decision" branch happened | Decisions in force rest on it: Graz + Vienna hybrid (Graz-only at A2 ≈ 1 relevant ad per week), English-written ads (147 nationally, 6 in the Graz area), skip Tableau (3 % of ads); snapshot 2026-10-18. The payoff is not observable: 0 applications. |
| Missed 3: adoption failed in a place the tree did not model | Its advice to send about 3 applications per week from late September 2026 was not followed. The information was used for targeting, not for action. |
| Missed 4: hours | 24 h is a lower bound (the first public commit squashes 220 files, 31,784 lines). Above about 23 h, the full build is negative on information value alone; the case then rests on portfolio and reuse value. |
| Missed 5: the build did not show its own top gap | The project found SQL in 40 % of ads and in 10 % of observed candidates, but it shows SQL in one query only. The ex-ante scope never asked which skills the build itself shows. |
