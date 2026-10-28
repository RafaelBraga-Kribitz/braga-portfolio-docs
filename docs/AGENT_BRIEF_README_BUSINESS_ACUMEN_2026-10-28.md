# Agent brief: portfolio READMEs for business acumen, plain language, and a viability retrospective

Issued 2026-10-28 by the planning session. Owner: Rafael Braga-Kribitz. You are the executing agent. This brief is self-contained; the files it names hold the detail.

## 1. Goal

Make every public portfolio README demonstrate business acumen and clear stakeholder communication, and write a retrospective viability analysis per project. Done means: each registered repository passes the README gate (exit 0), each README follows the three writing rules, and `docs/viability/` holds one page per project plus a summary table.

## 2. Read first, in this order

1. `C:\Users\Benutzer1\orca\workspaces\braga-portfolio-docs\crinoid\CLAUDE.md` (agent protocol of the gate repository).
2. `docs/AGENT_GUIDE.md` (how to run the gate, what it fixes, what it never fixes).
3. `docs/BUSINESS_ACUMEN_PLAN_2026-10-28.md` (audit scores, per-project edits and renames, viability method, effort proxies, planner priors). This brief does not repeat it.
4. `manifest/portfolio.yaml` (declared type, status, hero, demo, license per project; the gate never infers these from prose).
5. `~/.claude/knowledge/career-knowledge-core.md` (market facts, decisions in force, hard boundaries). Every number you cite about the market comes from there, with its vintage date.

## 3. Where the repositories are

* Gate repository (this one): `C:\Users\Benutzer1\orca\workspaces\braga-portfolio-docs\crinoid`, branch `RafaelBraga-Kribitz/install-claudex-loop-skill`. It is a git worktree. Do not `cd` to the main checkout. Do not use bare `git stash`.
* Portfolio clones: `C:\Users\Benutzer1\Dev\<project>`. Set `BRAGA_REPOS_ROOT=C:\Users\Benutzer1\Dev` when you run the gate.
* Known path problems: `DSX` and `bk-viz` have no local folder. `brazil-2026-election-forecast` in the registry is `brazil_presidential_election_prediction_2026` on disk. `NextMove`, `metric_lineage_simulator`, `Chart_Audit_Framework` have no README.

Gate commands:

```bash
BRAGA_REPOS_ROOT=/c/Users/Benutzer1/Dev python -m readme_quality portfolio              # table, all repos
python -m readme_quality fix   --repo /c/Users/Benutzer1/Dev/<project>                  # safe auto-fixes, then re-audit
python -m readme_quality audit --repo /c/Users/Benutzer1/Dev/<project> --verbose         # exit 0 = PASS
python -m readme_quality explain <requirement_id>
```

Baseline on 2026-10-28: 0 of 14 PASS. Most failures are structural and auto-fixable.

## 4. The three writing rules (owner-stated 2026-10-28)

1. **About 80 % of sentences in ASD-STE100 style.** Short (20 words for instructions, 25 for descriptions), active voice, one idea per sentence, common words. Keep technical terms. Define each one once, at first use.
2. **No made-up or internal code references in prose.** Do not write finding IDs, layer codes, scenario codes, decision codes, or module letters (F-222, D-026, BQ01, Layer 1/2/3, Layer P/R/D, S4_70, S-lean-hybrid-amr, Module A/B/C, OQ-02) as if the reader knows them. If a code must stay because files carry it, give it a plain name and a one-line legend.
3. **Business-relatable names** for sections, charts and components. Name the thing by what it does for the decision. The plan file lists the renames per project.

Measure rule 1 before you finish each README: count sentences in prose (exclude code blocks, tables, headings, link lists), count those over 25 words or in passive voice, and report the share. Target at least 80 % compliant.

## 5. Hard constraints

* **Never invent** numbers, results, hours, licenses, screenshots, URLs or capabilities. Every fact in a README exists in the repository first. Every market number comes from the career-knowledge files with its date.
* **Preserve intellectual content.** Reorder, reframe, rename, shorten. Delete only what is obsolete, wrong, duplicated or misleading. Keep every existing section's substance.
* **Keep the gate's heading families.** Headings match alias sets, not exact text. Safe plain names: "What it does" (first H2), "Start here", "Results", "How it works", "Data", "Validation", "How it fits together", "Known limits", "Status", "License", "Author". See `readme_quality/checks.py` lines 44 to 63 for the full sets.
* **Do not weaken a check** to make a repository pass. If a check is wrong, fix it in the gate repository with a test, bump the manifest version, re-audit.
* **Never write placeholders** (TBD, Coming soon, {{ }}). Set not-applicable states in the registry.
* **Never write alt text for a chart you have not looked at.** Open the image.
* **Do not change any license.** Follow `docs/LICENSE_POLICY.md`.
* **Hard boundaries from the career knowledge:** never publish scrapers, ad text, URLs or personal data; never rank individual candidates; no new scraping.
* **Seniority wording:** never write "junior" or "transitioning". Write "German A2" with CEFR when German appears.
* **Calibrated language:** "ads mention", "advertised floor". Never "employers require".
* **Commits:** commit in each portfolio repository on a new branch named `readme/business-acumen-2026-10`. Do not push. Do not open pull requests. Rafael reviews and pushes.

## 6. Work plan and order

Do the steps in this order. Report after each numbered step.

| Step | Work | Budget |
|---|---|---|
| 0 | Run the portfolio gate, save the table to `docs/viability/_gate_baseline_2026-10-28.txt`. Run `fix` on every repository that has a README. Re-run the table. | 0.5 h |
| 1 | `austria-data-job-market-intelligence`: apply the recipe (plan file, "Standard rewrite recipe" and item 1). | 2 h |
| 2 | `warehouse_humanoid_tco` (plan item 2). | 1.5 h |
| 3 | `austrian-mmm-budget-optimizer` (plan item 4). | 1.5 h |
| 4 | `decision-analytics-reconstruction` (plan item 3; frozen, summary-level edits only). | 1 h |
| 5 | `energy-procurement-risk-analyzer` (plan item 5). | 1 h |
| 6 | Retrospective viability analysis for the five repositories above (section 7 of this brief). | 2.5 h |
| 6b | Ex-ante business case for the same five repositories (section 7b of this brief), then the calibration table. | 3 h |
| 7 | `funnel_correlation_py`, `governance-bootstrap`: viability page and business case first. If the verdict is "sunk", write only the 10-line summary README and flag for Rafael. Do not rewrite in full until he answers open question 1. | 1 h |
| 8 | Registry: fix the Brazil path. Flag `DSX` and `bk-viz` as "no local clone" in your report; do not remove them (open question 2). | 0.5 h |
| 9 | `NextMove`, `metric_lineage_simulator`, `Chart_Audit_Framework`, `brazil_presidential_election_prediction_2026`: viability page and business case first. Write a README from `templates/<type>.md` only if the verdict is "worth it" or "open". Template names: analytical, framework, library, foundation, interactive (use interactive for registry type `application`). Otherwise write the 10-line summary and flag. | 3 h |
| 10 | Propose the three gate checks (plan file, "Gate changes to propose") as `recommended`, each with a test and a promotion condition in `docs/README_STANDARD.md` section 6. Bump the manifest version. Do not promote to `required`. | 2 h |
| 11 | Final report (section 8). | 0.5 h |

Steps 1 to 5, 6 and 6b are independent of Rafael's open answers. Steps 7, 8 and 9 contain decisions that are his; do the analysis, do not decide.

### The recipe for one README (from the plan file)

1. `fix` first.
2. Five-line top box: who decides, what they choose, the answer with number and unit, the main caveat, the one chart.
3. Rename every code to a business name. Legend if needed.
4. Move method, priors, sampler, governance and agent notes below Limitations.
5. Rewrite sentence by sentence to STE. Measure the share.
6. `audit --verbose`. Exit 0 is done.

## 7. Viability retrospective: what to produce

One file per project at `docs/viability/<project>.md` in the gate repository, 1 page, this structure:

```
# <Project>: was it worth building?
Date · status in registry · hours (source: owner log | git estimate ±50 %)

## Cost
Hours spent. Period. Source and caveat.

## Opportunity cost
Best alternative at the time, in hours and in what it buys
(applications not sent at 8 to 10 per week · German hours at the A1.2 to B1 stage · the next scored project).

## Scenarios
| Scenario | Demand match | Scarcity | Domain angle | Interview story | Finish cost | Total /10 |
| S0 not built | ... |
| S1 as published today | ... |
| S2 after this plan | ... |
| S3 extended (<named next step>) | ... |
One line of evidence per cell. Market shares from career-knowledge-core.md with the vintage date.

## Verdict
worth it, keep · worth it, finish then freeze · sunk, freeze with summary only · sunk, archive and unpin

## Lesson for the next project choice
One or two sentences.

## Open questions
Facts you could not establish from the repository or the knowledge files.
```

Rules for this analysis:

* Hours: use Rafael's log if he supplies it (open question 4). Until then, estimate from the git table in the plan file, label every estimate, and note that agent-assisted repositories inflate commit counts.
* Outcome: there are 0 applications sent, so no conversion data exists. Score hiring evidence, not conversions. Say this in every page.
* The planner's priors in the plan file are hypotheses. Test them against the repository. If your verdict differs, say why with evidence.
* End with `docs/viability/README.md`: a summary table (project, hours, opportunity cost, S1 score, S2 score, verdict, lesson) and the three strongest lessons across the portfolio.

## 7b. Ex-ante business case: what to produce

This is the analysis a company employee should have written **before** the project was built. The retrospective in section 7 looks back; this one forecasts. Both are required. The method and the per-project starting points (persona, decision, money at stake, first-guess verdict) are in the plan file, section "Ex-ante business case". Read them first.

One file per project at `docs/business-case/<project>.md` in the gate repository. Write it as if dated the week before the first commit (dates in the plan file's git table). One screen, tables not prose, this structure:

```
# <Project>: business case, written as of <date before first commit>
Persona: <role> at <type of company>. Decision owned: <decision>. Cycle: <how often>. Sign-off: <who>.

## Money at stake per decision cycle
| Item | Value | Unit | Source (repo file / public source / assumption + range) |

## Status quo
How the decision is taken today, what it costs, how often it goes wrong. Sources or "assumption".

## Options
| Option | Cost | Time to answer | Expected value | Note |
| Do nothing | | | | |
| Buy or rent (vendor, consultant, spreadsheet) | | | | |
| Build small (named 2-week scope) | | | | |
| Build full (the project as scoped) | | | | |

## Outcome tree for "build full"
| Branch | Probability (range, source) | Value if it happens (EUR, source) | Probability x value |
| Changes the decision and pays off | | | |
| Confirms the status quo | | | |
| Built but not adopted | | | |
| Wrong, decision gets worse | | | |
| Sum | | | EV before cost |

## Cost
Build hours x loaded hourly rate (assumption, anchored on the advertised analytics floor, state the marker and date) + run cost per year + delay cost.

## Result
EV(build full) = ... · payback = ... · break-even probability of "pays off" = ... · EV(build small) = ...

## Sensitivity
The one or two assumptions that flip the verdict, and the value at which they flip.

## Verdict
Build full · build small first · buy · do nothing. One sentence of reason. One sentence on the evidence that would change it.

## Calibration against the retrospective
Retrospective verdict (from docs/viability/<project>.md): ... Agree? ... What the ex-ante view missed: ...
```

Rules for this analysis:

* Every probability is an assumption with a range and a stated basis (repository evidence, public benchmark with citation, or judgement). Never a bare number.
* Every euro value has a unit, a period and a source. Numbers from the repository (for example TCO €0.453M vs €0.647M, EPRA exposure €6.99M vs premium €0.12M, MMM 15.1 % of media contribution) keep their caveats (CALIBRATED, SIMULATED, "units are not euros").
* Hourly rate and company-size ranges: use Rafael's answer to open question 0 if given; otherwise a labelled range anchored on the advertised analytics floor in `career-knowledge-core.md`, with its vintage date.
* Where the project's main product is information, compute the value of better information: EV of the decision with the tool minus EV without it.
* For `NextMove`, `metric_lineage_simulator` and the Brazil forecast, identify the persona from the repository first. If no credible persona exists inside the Austrian target market, say so; that is itself a verdict.
* End with `docs/business-case/README.md`: the calibration table (project, ex-ante verdict, retrospective verdict, agree, what the ex-ante view missed) and three lessons on how Rafael should decide the next project before building it.

## 8. What to return

A single report, in this order:

1. Gate table before and after (PASS count out of 14).
2. Per README: STE share measured before and after, number of codes removed, list of renames applied, gate result.
3. Viability summary table and the three cross-portfolio lessons.
3b. Business-case calibration table (ex-ante vs retrospective verdict per project) and the three lessons for choosing the next project.
4. Diffs: branch name and commit hashes per repository. No pushes.
5. Decisions left for Rafael, each as one question with your recommendation and the evidence.
6. Anything you could not verify, stated plainly.

Write the report in ASD-STE100 style: short sentences, active voice, one idea each, tables for comparisons. Rafael reads it.

## 9. Open decisions, owned by Rafael, not by you

0. Ex-ante business case: which loaded hourly rate and which company-size ranges (media budget, number of picking cells, annual energy spend) may you assume? Until answered, use labelled ranges.
1. `governance-bootstrap` and `funnel_correlation_py`: full rewrite, or "internal tool" label and unpin?
2. `DSX` and `bk-viz`: clone or remove from the registry?
3. Three new gate checks: now, or after the first three rewrites?
4. Hours per project from his own log?
5. Which alternative counts as the opportunity cost in 2026: German study, applications, or the SaaS retention project? Until answered, show all three in each viability page.
