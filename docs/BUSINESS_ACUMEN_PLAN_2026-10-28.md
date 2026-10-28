# Plan: business acumen and plain language in every portfolio README

Date: 2026-10-28. Owner: Rafael. Status: plan, not started. Time used for this audit: 20 minutes.

## Goal (owner-stated 2026-10-28)

Every public README must show business acumen and clear communication to stakeholders.
Three writing rules apply to all README text:

1. About 80 % of sentences follow ASD-STE100: short, active, one idea, common words. Keep technical terms. Define each one once.
2. No made-up code references. Do not name internal IDs (finding codes, layer codes, scenario codes, decision codes) as if the reader knows them.
3. Use business-relatable names for sections, charts and components. Say what the thing does for the decision, not what the code calls it.

## Audit result (2026-10-28, 7 READMEs read, 6 missing)

Scores: 0 = missing, 1 = weak, 2 = strong. Columns: Q = business question first, R = result as business outcome, S = stakeholder communication, P = plain language, N = business naming. STE = estimated share of STE-like sentences.

| Project | Q | R | S | P | N | Total /10 | STE now | Gate |
|---|---|---|---|---|---|---|---|---|
| warehouse_humanoid_tco | 1 | 2 | 2 | 1 | 1 | 7 | ~40 % | FAIL |
| energy-procurement-risk-analyzer | 2 | 2 | 1 | 1 | 1 | 7 | ~55 % | FAIL |
| austrian-mmm-budget-optimizer | 1 | 2 | 2 | 1 | 1 | 7 | ~40 % | FAIL |
| decision-analytics-reconstruction | 2 | 0 | 1 | 1 | 1 | 5 | ~35 % | FAIL |
| austria-data-job-market-intelligence | 1 | 1 | 1 | 0 | 1 | 4 | ~15 % | FAIL |
| funnel_correlation_py | 0 | 0 | 0 | 1 | 1 | 2 | ~50 % | FAIL |
| governance-bootstrap | 0 | 0 | 0 | 0 | 0 | 0 | ~25 % | FAIL |
| NextMove, metric_lineage_simulator, Chart_Audit_Framework | - | - | - | - | - | - | no README | FAIL |
| DSX, bk-viz | - | - | - | - | - | - | no local folder | FAIL |
| brazil-2026-election-forecast | - | - | - | - | - | - | folder name differs (`brazil_presidential_election_prediction_2026`, README 5,148 words), not audited | FAIL |

Gate run: `BRAGA_REPOS_ROOT=C:\Users\Benutzer1\Dev python -m readme_quality portfolio` gives 0 of 14 PASS.
Most failures are structural and auto-fixable (hero, badges, status line, author block). Run `fix` first.

## What the gate already covers, and what it does not

* Required today: problem and decision in the first paragraph (`identity.problem`), executive summary as first H2, decision and results sections, limitations with at least 2 items.
* Not covered: sentence length, jargon, internal code names, business naming of sections and charts. Section 7 of the standard puts prose quality out of scope.
* Headings are matched by alias sets, not exact text. Plain names such as "What it does", "How it works", "How it fits together", "Start here", "Known limits" already pass.

## The same five problems in every README

1. The decision owner is never named. Say who decides and what they choose.
2. Internal codes replace names: F-222, D-026, BQ01, Layer 1/2/3, Layer P/R/D, S4_70, S-lean-hybrid-amr, Module A/B/C, OQ-02.
3. Method detail comes before the result and the limits.
4. Sentences run 30 to 60 words. Many hold three ideas.
5. Badges, SSOT notes, governance notes and agent notes sit above the decision.

## Standard rewrite recipe (one README, 60 to 90 minutes)

1. Run `python -m readme_quality fix --repo <path>` to get the structural items green.
2. Write a 5-line top box: who decides, the decision, the answer with number and unit, the main caveat, the one chart.
3. Rename every code to a business name. Add a one-line legend if the code must stay in file names.
4. Move method, priors, sampler, governance and agent notes below Limitations.
5. Rewrite sentence by sentence to STE. Target: 80 % of sentences at 20 words or fewer, active voice, one idea.
6. Run the gate again. Exit 0 is done.

## Per-project top edits and renames

### 1. austria-data-job-market-intelligence (pinned first, D-034), 2 h
* Top box: decider = a data-job seeker in Graz; decision = which roles, skills and cities to target; answer = Vienna 45 % of 699 core ads, Styria 62 to 68; caveat = one snapshot, small Styrian n.
* Split: short README + separate "Repository map, reproduction, weekly refresh" page. Findings block becomes bullets.
* Renames: Layer 1 -> Employer demand. Layer 2 -> Candidate supply (GitHub). Layer 3 -> Demand vs supply gap. Visual decision layer / BQ figures -> Decision charts, one question each. AGENT_CONTEXT.md -> Notes for AI assistants.
* Remove visible marker syntax from any prose a human reads on GitHub, or explain it once.

### 2. warehouse_humanoid_tco, 1.5 h
* Put the decision box and one chart first. Move badges, SSOT note and reproducibility disclaimer below.
* Recommendation in 3 short sentences with unit and the household-data caveat.
* Renames: S-lean-hybrid-amr -> Lean mix: 1 worker + 3 robot carts. S-baseline-human -> Today's 8-worker crew. rho <= 0.85 sizing rule -> Max 85 % workload per resource. NPV -> 5-year total cost in today's money. Tornado chart -> What moves the cost most. Replace F-xxx IDs with plain names.

### 3. decision-analytics-reconstruction (frozen, summary only), 1 h
* Add one business result from the budget module (share of budget moved, coverage gained, unit, caveat). Today the only result is a model check.
* Add "What a campaign would do differently". Move governance and live-URL text to the bottom.
* Renames: Module A -> Voter segments and turnout. Module B -> Campaign budget allocation. Module C -> Poll tracking and scenarios. Verified anchors -> Known real numbers. "retrodiction" -> explain once: "the model is checked against the known result".

### 4. austrian-mmm-budget-optimizer, 1.5 h
* One sentence at the top: decider = head of marketing or CFO; decision = where to move the next euro.
* One headline: "Move budget from out-of-home to TV. Gain about 15 % of media contribution. Units are not euros."
* Renames: Layer P -> Test on made-up data with a known answer. Layer R -> Test on public demo data. Layer D -> Budget shift recommendation. Method -> How the estimate is built. Marginal ROAS at current -> Return on the next euro, today. Define adstock, saturation, R-hat once or move them below Limitations.

### 5. energy-procurement-risk-analyzer, 1 h
* Add a Recommendation line: who chooses, why 70 % forward over the others, the EUR 0.12 M trade-off.
* Renames: S1 -> Spot only. S3 -> Full forward hedge. S4_70 -> 70 % forward, 30 % spot. Forward risk by strategy (P95) -> Worst realistic yearly cost (1 year in 20). NUMERIC_SSOT.md -> Numbers used in this report.
* Write three limitations in the README: constructed load profile, simulated prices, one year ahead.

### 6. funnel_correlation_py, 45 min
* Open with a business question and a real finding from the demo data, with chart and top 3 drivers.
* Add "What this does not show": correlation is not cause; binary targets only.
* Renames: Three-step workflow -> How to find what drives sign-ups. binarize -> Group values into yes/no flags. correlate -> Rank factors by link to outcome. API reference -> Settings. Folder structure -> Project layout, for developers.

### 7. governance-bootstrap, 45 min, or mark as internal tool
* Open with the problem: rules in data projects break again. This kit stops the same mistakes from returning. Add one before/after number from a real project.
* Cut the file tree and gate table. Add a 10-line summary.
* Renames: Adversary -> Re-check of fixed issues. Steward -> Status report. Remediator -> Fixer. Vendored -> Copied into each project, with updates. CRAP score -> Risky untested code score.

### 8. Missing READMEs
* NextMove, metric_lineage_simulator, Chart_Audit_Framework: no README. Start from `templates/<type>.md`. Apply the recipe.
* DSX, bk-viz: no local folder under Dev. Clone them or remove them from the registry.
* brazil-2026-election-forecast: registry path and folder name differ. Fix the registry path or rename the folder, then audit.

## Order of work and hours

| Step | Hours | Why first |
|---|---|---|
| Market-intel README (recipe) | 2 | pinned repo, worst STE share |
| warehouse TCO README | 1.5 | strongest content, quick win |
| MMM README | 1.5 | flagship, strong result already |
| DAR summary | 1 | frozen, summary only |
| EPRA README | 1 | short, clear numbers |
| funnel_correlation_py + governance-bootstrap | 1.5 | low value, do last or mark internal |
| Registry fixes + 3 new READMEs | 3 | gate cannot audit them today |
| Total | 11.5 | fits inside Track A time before 2027-01-04 |

## Gate changes to propose (land as `recommended`, per standard section 6)

1. `communication.plain_language`: share of prose sentences over 25 words must be under 20 %. Promotion condition: all registered repos conform.
2. `communication.no_internal_codes`: prose must not contain bare ID patterns (F-123, D-012, BQ01, S4_70, Layer X) outside a legend. Promotion condition: same.
3. `communication.decision_owner`: the first paragraph names a role that decides. Promotion condition: same.
Each needs a test, a manifest version bump, and a portfolio re-audit.

## Retrospective viability analysis (added 2026-10-28, owner-requested)

One analysis per project. Question: given what the project cost, and what the same hours could have bought, was it worth building? Output: one page per project in `docs/viability/<project>.md`, plus a summary table in this file.

### Method

1. **Cost.** Hours spent. Source order: Rafael's own log if he supplies it; else estimate from the commit span and commit count below, and label it "estimate from git, ±50 %". Never present an estimate as a measured number.
2. **Opportunity cost.** The best alternative use of the same hours at the time. Candidates, from the career knowledge: (a) applications (target 8 to 10 per week from 2027-01-04; 0 sent so far), (b) German study (the main blocker; A1.2 actual), (c) the next project by D-034 score (B2B SaaS revenue retention), (d) the application system build. State the alternative in hours and in the unit it buys (applications not sent, German hours not studied, flagship not started).
3. **Scenarios.** Score the business outcome of each project in four scenarios:
   * S0 Not built: hours go to the best alternative.
   * S1 As published today: README as it is.
   * S2 After this plan: README rewritten, gate green.
   * S3 Extended: the next planned step (for example MMM Power BI page, EPRA Azure refit).
4. **Outcome measure.** There is no application-log data yet (0 applications). So the outcome is a hiring-evidence score, not a conversion number. Score 0 to 2 on five items, with the source:
   * Demand match: the project shows skills that ads mention most (SQL 40 %, Python 39 %, data quality 31 %, cloud 32 %, ETL 20 %, Azure 19 %, Power BI 17 %). Source: market-intel snapshot 2026-10-18.
   * Scarcity: the project shows what the public GitHub pool lacks (SQL, data quality, modelling, Azure/Databricks, Power BI, READMEs with question, result, limits).
   * Domain angle: marketing, customer, e-commerce, or a Styrian/Austrian business setting (Graz employers: KNAPP, Anton Paar, Magna, niceshops).
   * Interview story: a decision owner, a number, a caveat, and a "what I would do differently" that Rafael can tell in 2 minutes.
   * Finish cost: hours still needed to reach S2. Lower is better.
5. **Verdict.** One of: worth it, keep; worth it, finish then freeze; sunk, freeze with summary only; sunk, archive and unpin. Plus one lesson for the next project choice.
6. **Rules.** Use calibrated language ("ads mention", "advertised floor"). Never say employers require. Never invent hours, numbers or results. Where a fact is missing, write the open question.

### Effort proxies from git (collected 2026-10-28, local clones)

| Project | Commits | First to last commit | Python files | Status in registry |
|---|---|---|---|---|
| austria-data-job-market-intelligence | 28 | 2026-09-16 to 2026-10-19 | 136 | Complete |
| warehouse_humanoid_tco | 80 | 2026-05-21 to 2026-07-17 | 179 | Complete |
| decision-analytics-reconstruction | 399 | 2026-05-07 to 2026-08-20 | 394 | Complete, frozen |
| austrian-mmm-budget-optimizer | 57 | 2026-08-04 to 2026-09-19 | 42 | Complete |
| energy-procurement-risk-analyzer | 395 | 2026-07-19 to 2026-07-31 | 102 | Functional |
| governance-bootstrap | 5 | 2026-06-16 | 22 | Maintained |
| funnel_correlation_py | 1 | 2026-02-25 | 15 | Functional |
| NextMove | 91 | 2026-07-24 to 2026-08-05 | 74 | In development |
| metric_lineage_simulator | 70 | 2026-06-07 to 2026-08-08 | 38 | In development |
| Chart_Audit_Framework | 4 | 2026-06-23 to 2026-06-24 | 6 | Foundation |
| brazil_presidential_election_prediction_2026 | 34 | 2026-09-29 to 2026-10-07 | 134 | In development |

Commit counts are a weak proxy. Agent-assisted repos (EPRA: 395 commits in 12 days) inflate the count. Prefer Rafael's own hours.

### Planner's prior per project (to test, not to copy)

| Project | Prior verdict | Why | What would change it |
|---|---|---|---|
| austria-data-job-market-intelligence | worth it, keep | drives every career decision; SQL, ETL, data quality; scarce README style; pinned first by D-034 | none; it is the base of the system |
| warehouse_humanoid_tco | worth it, keep | decision analysis with a recommendation, a number and a caveat; Styrian logistics domain (KNAPP) | if hours were far above 80, the lesson is scope, not value |
| austrian-mmm-budget-optimizer | worth it, finish (Power BI page) | marketing domain angle; budget decision with a number; Power BI page adds the top BI tool from ads | Bayesian method is rarely named in ads; keep it below the decision |
| energy-procurement-risk-analyzer | worth it, freeze after README | Styrian manufacturer setting, euro result, risk framing; Azure refit is conditional (D-034) | application-log gate of about 40 rows |
| decision-analytics-reconstruction | sunk, freeze with summary | 399 commits, no business domain, election retrodiction; D-034 already froze it | a business result from the budget module would raise the interview-story score |
| governance-bootstrap | sunk, archive or mark internal | no ad demand, no result, tooling for the author | none expected |
| funnel_correlation_py | sunk, archive or mark internal | 1 commit; ads name tools, not libraries | a real finding on marketing data in the README |
| NextMove | open | 91 commits, in development, no README; risk of a fourth half-built flagship | a 2-minute business story with a number |
| metric_lineage_simulator | open | 70 commits, no README; data quality and lineage match ads (31 %) | a finished demo and a business result |
| Chart_Audit_Framework | sunk, archive | 4 commits, 6 files | none expected |
| brazil-2026-election-forecast | sunk, freeze | political forecast, no domain angle, 5,148-word README; competes with the January start | a clear reason it helps an Austrian data application |

## Ex-ante business case (added 2026-10-28, owner-requested; the retrospective above stays)

This is the analysis that should exist **before** a project is built. Point of view: Rafael is an employee of the company that would use the tool. He must forecast whether building it is a good use of the company's resources. Output: one page per project in `docs/business-case/<project>.md`, written as if dated the week before the first commit, plus a calibration table that compares the ex-ante verdict with the retrospective verdict.

### Method

1. **Persona and decision.** Name the role (for example "operations analyst at a Styrian warehouse operator"), the decision that role owns, how often it is taken, and who signs it off.
2. **Money at stake.** The size of the decision in euros per cycle: budget moved, capex committed, cost exposure, revenue affected. Take it from the repository where a number exists (TCO €0.453M vs €0.647M; EPRA exposure €6.99M; MMM 15.1 % of media contribution). Where none exists, give a range and label it "assumption".
3. **Status quo.** How the company takes this decision today (gut feel, spreadsheet, consultant, vendor quote). What that costs and how often it goes wrong.
4. **Options.** Do nothing · buy or rent (vendor tool, consultant, spreadsheet) · build small (one-page model, two weeks) · build full (the project as scoped).
5. **Outcome tree for "build".** At least four branches with a probability and a value each:
   * The tool changes the decision and the change pays off.
   * The tool confirms the status quo (value = avoided doubt, lower).
   * The tool is built but not adopted (value ≈ 0, cost stays).
   * The tool is wrong and the decision is worse (negative value).
   Probabilities are assumptions with a range. State the source of each: repository evidence, public benchmark, or judgement.
6. **Cost.** Build hours × a loaded hourly rate, plus run and maintenance cost per year. Rate: an assumption anchored on the advertised analytics floor (about €50k per year; see career-knowledge-core.md for the current marker). Label it. Add the delay cost if the decision waits for the build.
7. **Expected value.** EV(build) = Σ probability × value − cost. Also give: payback period, the break-even probability of the "pays off" branch, and the value of the "build small" option. Where the project is mainly information, frame it as the value of better information: EV with the tool minus EV without it.
8. **Sensitivity.** Name the one or two assumptions that flip the verdict, and the value at which they flip.
9. **Verdict.** Build full · build small first · buy · do nothing. One sentence of reason. One sentence on what evidence would change it.
10. **Calibration.** Compare with the retrospective verdict from `docs/viability/<project>.md`. Where they differ, write what the ex-ante view missed. This is the learning loop and an interview story.

Rules: calibrated language, every number with unit and source, every probability labelled as an assumption with a range, no numbers presented as facts that are not in the repository or a cited public source. Keep each page to one screen. Tables, not prose.

### Starting points per project (to verify against the repository, not to copy)

| Project | Persona (employee of) | Decision owned | Money at stake per cycle | First guess of verdict |
|---|---|---|---|---|
| warehouse_humanoid_tco | automation or operations analyst at a Styrian warehouse operator or integrator (KNAPP-type) | capex: humans vs robot carts vs humanoids per picking cell | 5-year cost per cell €0.45M to €0.65M (README); wrong choice ≈ the gap, times the number of cells | build small first (spreadsheet TCO), build full only if several cells are in scope |
| austrian-mmm-budget-optimizer | marketing analyst at an Austrian advertiser | yearly media budget split across channels | 15.1 % of media contribution (README, units not euros) × the advertiser's media budget (assumption range) | build full if media budget is above a threshold the analysis must find; otherwise buy or rent |
| energy-procurement-risk-analyzer | energy buyer or controller at a 50 GWh/year Styrian manufacturer | hedge strategy for the next 12 months | P95 exposure €6.99M vs hedge premium €0.12M; €25.62M past mis-buy (README, CALIBRATED/SIMULATED tags) | build small first; the premium-to-exposure ratio decides |
| austria-data-job-market-intelligence | the "company" is a one-person job search; alternatively a career service or a recruiting team | where to apply, what to learn, which city | months of search × advertised floor (€46k junior, €50k analytics); mis-targeting costs months | build small (one snapshot); the weekly refresh is a separate decision |
| decision-analytics-reconstruction | analyst in a campaign team with a fixed budget | budget allocation across regions, poll reading | the campaign budget (README: fixed budget, amount to confirm) | build small; the full three-module build is hard to justify ex ante |
| governance-bootstrap | engineering lead of a small data team | adopt a governance kit or not | rework hours avoided per quarter (assumption) | do nothing or buy (existing linters), unless rework hours are documented |
| funnel_correlation_py | marketing analyst who needs the R package in Python | which customer traits to investigate first | analyst hours saved (assumption) | build small (a port is small) if R is not available; otherwise do nothing |
| NextMove | to identify from the repository | to identify | to identify | open until the persona is known |
| metric_lineage_simulator | BI or data-quality lead | where a wrong KPI comes from; which metric definitions to fix | cost of a wrong KPI decision (assumption; data quality appears in 31 % of ads) | open; build small if a real incident exists |
| Chart_Audit_Framework | BI team lead | which dashboards mislead | cost of a misread chart (assumption) | do nothing or buy; a checklist beats a framework |
| brazil-2026-election-forecast | analyst at a media house or a campaign | editorial or campaign allocation | to identify | do nothing from an Austrian employer's point of view; the persona is outside the target market |

### Calibration table (fill after both analyses exist)

Filled 2026-10-28: see `docs/business-case/README.md` (calibration table, 11 projects) and `docs/viability/README.md` (summary table).

## Open questions for Rafael

0. Ex-ante business case: which loaded hourly rate and which media or capex ranges may the agent assume? If none, it uses labelled ranges anchored on the advertised floors.
1. governance-bootstrap and funnel_correlation_py: rewrite them, or label them "internal tool" and unpin?
2. DSX and bk-viz: clone them, or remove them from the registry?
3. Do the three gate checks above go into the standard now, or after the first three rewrites prove the pattern?
4. Viability analysis: can you supply hours per project from your own log? If not, the agent uses the git estimate with a ±50 % label.
5. Which alternative counts as the opportunity cost for 2026: German study, applications, or the SaaS retention project?
