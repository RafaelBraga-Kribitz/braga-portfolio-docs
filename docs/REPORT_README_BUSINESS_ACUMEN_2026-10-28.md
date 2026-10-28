# Report: README business acumen, plain language and viability analysis

Date: 2026-10-28. Written for Rafael. Source: `docs/AGENT_BRIEF_README_BUSINESS_ACUMEN_2026-10-28.md`. Plan: `docs/PLAN_README_BUSINESS_ACUMEN_2026-10-28.md`.

## Summary

* Seven READMEs are rewritten and committed. Four READMEs stay unchanged because their projects are "sunk" and the decision is yours.
* All 12 audited repositories pass the gate. Two registered repositories have no local clone and are not audited.
* Eleven viability pages and eleven business cases exist, with a summary page for each.
* Three plain-language checks are added to the gate at `recommended`. Nothing is pushed. The gate repository is not committed.
* Stale local clones were the biggest surprise. All plan figures built on them were out of date. The work uses the published branches.

## 1. Gate table before and after

| Run | What it audits | Result |
|---|---|---|
| Before, stale clones | local folders in `Dev`, 8 to 185 commits behind GitHub | 1 of 14 PASS |
| Before, published READMEs | fresh worktrees of `origin/<default>` | 11 of 14 PASS |
| After, rewritten READMEs | same worktrees, branch `readme/business-acumen-2026-10` | 11 of 14 PASS in the raw run; 12 of 12 audited PASS |

* The three non-PASS rows in the raw run are `dsx`, `bk-viz` (no local clone) and `braga-portfolio-docs` (outside the worktree root; it passes with `audit --repo .`).
* The brief expected 0 of 14 PASS and many auto-fix items. That was true only for the stale clones. `fix --dry-run` on the published READMEs proposed no change.
* Raw files: `docs/viability/_gate_baseline_2026-10-28.txt`, `docs/readme-audit-latest.md`.

## 2. READMEs: prose measures, codes, gate

Measure: `python -m readme_quality prose`. Before = published README. After = rewritten README. "ste_share" is the share of sentences with at most 25 words and no passive voice. The passive test is a heuristic. Target: at least 80 %.

| Project | ste_share before → after | Long sentences before → after | Internal codes before → after | Decision owner | Gate |
|---|---|---|---|---|---|
| austria-data-job-market-intelligence | 72.3 % → 99.6 % | 14.9 % → 0.0 % | 6 → 0 | no → yes | PASS_WITH_EXCELLENCE, no WARN |
| warehouse_humanoid_tco | 75.0 % → 94.9 % | 21.7 % → 4.2 % | 8 → 0 | no → yes | PASS_WITH_EXCELLENCE, 1 old WARN (no stack table) |
| austrian-mmm-budget-optimizer | 56.4 % → 92.9 % | 27.7 % → 1.8 % | 17 → 0 | yes → yes | PASS_WITH_EXCELLENCE, no WARN |
| energy-procurement-risk-analyzer | 62.7 % → 92.8 % | 22.4 % → 2.4 % | 2 → 0 | yes → yes | PASS_WITH_EXCELLENCE, 1 WARN (chart caption) |
| decision-analytics-reconstruction (summary level) | 79.3 % → 91.1 % | 14.9 % → 2.5 % | 16 → 0 | yes → yes | PASS_WITH_EXCELLENCE, 1 old WARN (no why section) |
| metric_lineage_simulator | 80.6 % → 96.1 % | 10.4 % → 1.3 % | 2 → 0 | no → yes | PASS, no WARN |
| NextMove | 59.6 % → 95.1 % | 29.8 % → 2.5 % | 7 → 0 | no → yes | PASS, no WARN |

Unchanged (verdict "sunk", your decision): `funnel_correlation_py` (90.0 %), `governance-bootstrap` (86.7 %), `Chart_Audit_Framework` (86.3 %), `brazil_presidential_election_prediction_2026` (68.2 %, 5 codes, no owner).

The first draft of the prose tool counted each source line as one sentence. Codex found that this misreads hard-wrapped files. The tool now joins wrapped lines. The "before" figures above use the corrected tool.

### Renames applied (section, chart, component)

* **All seven:** "Explore this project" → "Start here". "Method" → "How it works", placed below "Known limits". "Architecture" → "How it fits together". "Limitations" → "Known limits". A five-line box (who decides, what they choose, the answer, the main caveat, the chart) sits before the first section.
* **Market intelligence:** Layer 1/2/3 → Employer demand, Candidate supply, Demand vs supply gap. BQ45 → "controlled pay model". Table codes (T05, JB01, D05, and others) → plain names with a legend. AGENT_CONTEXT.md → "Notes for AI assistants" in prose.
* **Warehouse:** Lean Human + AMR Team → Lean mix: 1 worker + 3 robot carts. Legacy Overstaffed Team → Modeled legacy 8-worker reference. ρ ≤ 0.85 → Max 85 % workload per resource. NPV → 5-year total cost in today's money. Tornado → What moves the cost most. F-222, F-230, F-237, F-241, ADR-0014, ADR-0017 → plain words.
* **MMM:** Layer P / R / D → Test on made-up data with a known answer / Test on public demo data / Budget shift recommendation. Marginal ROAS → Return on the next unit of spend. "Units are not euros" sits next to every media-contribution number.
* **Energy:** S1 / S3 / S4_70 and similar keys → Full spot / Fixed annual / 70 percent forward, 30 percent spot, with a legend. NUMERIC_SSOT.md → "Numbers used in this report". ADR-022, ADR-023, M0 to M7, A1 to A4, SPEC-03, SPEC-05 → plain names.
* **Decision analytics:** Module A / B / C → Voter segments and turnout / Campaign budget allocation / Poll tracking and scenarios. F-021, F-034, F-069 → plain names with a legend. Verified anchors → Known real numbers.
* **Metric driver tree:** ADR-0004 → launch rule. ADR-0010 → scope decision record. F-001 to F-021 → plain words with a legend.
* **NextMove:** ADR-004 to ADR-012, AC-6/11/12, DEBT-001 to 005, M-A to M-F, 3WD → plain names with a legend.

### Two plan-file renames were wrong and are replaced

* "Worst realistic yearly cost (1 year in 20)" for P95: P95 is a percentile, not a worst case. The energy README now says "95th-percentile simulated annual cost (exceeded in about 1 year in 20)".
* "Today's 8-worker crew": the model defines it as a legacy overstaffed baseline, not a real site. The warehouse README now says "Modeled legacy 8-worker reference". The top box also shows the fair comparison, the 3-worker crew (€0.45M against €0.65M).

## 3. Viability summary

Rafael has sent 0 applications, so each score measures hiring evidence, not conversions. Hours are estimates from git with a range of ±50 %. One rubric scores all pages (`docs/viability/_assumptions.md`).

| Project | Hours | S1 today | S2 after plan | Verdict |
|---|---|---|---|---|
| austria-data-job-market-intelligence | 24 h | 7 | 9 | worth it, keep |
| warehouse_humanoid_tco | 80 h | 7 | 9 | worth it, finish then freeze |
| austrian-mmm-budget-optimizer | 32 h | 8 | 9 | worth it, finish then freeze |
| energy-procurement-risk-analyzer | 60 h | 9 | 10 | worth it, finish then freeze |
| metric_lineage_simulator | 24 h | 7 | 9 | worth it, finish then freeze |
| NextMove | 48 h | 8 | 10 | worth it, finish then freeze |
| decision-analytics-reconstruction | 144 h | 6 | 8 | sunk, freeze with summary only |
| funnel_correlation_py | 24 h | 5 | 6 | sunk, freeze with summary only |
| governance-bootstrap | 24 h | 3 | 3 | sunk, freeze with summary only |
| brazil_presidential_election_prediction_2026 | 16 h | 5 | 5 | sunk, freeze with summary only |
| Chart_Audit_Framework | 40 h | 3 | 4 | sunk, archive and unpin |

Three lessons across the portfolio:

1. **Write the buyer and the first number before the first commit.** The projects with the best scores each answer one money decision with one number. Cap a project at 8 h if its persona sits outside the Austrian target market.
2. **Cap governance and process before the build.** The warehouse project has 140 governance files and 33 source files. About 60 % of the commits in the decision analytics project are governance, audit or CI work.
3. **Put the skill that ads mention most into the smallest scope that ships.** SQL (ads mention 40 %) appears in one query in the market-intelligence project. The SQL warehouse was the first layer cut from the MMM project.

## 3b. Business case: ex-ante verdict against retrospective verdict

| Project | Ex-ante verdict | Retrospective verdict | Agree? |
|---|---|---|---|
| austria-data-job-market-intelligence | build small first | worth it, keep | Partly |
| warehouse_humanoid_tco | build small first | worth it, finish then freeze | Partly |
| austrian-mmm-budget-optimizer | build full | worth it, finish then freeze | Yes on "build" |
| energy-procurement-risk-analyzer | build small first | worth it, finish then freeze | Partly |
| decision-analytics-reconstruction | build small first | sunk, freeze | Yes in direction |
| metric_lineage_simulator | build small first | worth it, finish then freeze | Partly |
| NextMove | build small first | worth it, finish then freeze | Partly |
| Chart_Audit_Framework | buy | sunk, archive and unpin | Yes |
| funnel_correlation_py | build small first | sunk, freeze | Mostly |
| governance-bootstrap | build small first | sunk, freeze | Yes on the core |
| brazil_presidential_election_prediction_2026 | do nothing | sunk, freeze | Yes |

The full table with "what the ex-ante view missed" is in `docs/business-case/README.md`. Three lessons for the next project:

1. Run the ex-ante page first and let "build small first" cap the scope. Eight of eleven pages say so.
2. Name the buyer, the euro stake and the free alternative in the first line.
3. Add a branch for hiring evidence, legal risk and reuse to every decision tree. The company trees missed all three.

Every probability on these pages is an assumption with a range. The hourly rate (€35 to €60, central €45) is an assumption.

## 4. Diffs: branches and commits

All worktrees are under `C:\Users\Benutzer1\Dev\_readme-business-acumen-2026-10\`. Each branch is `readme/business-acumen-2026-10`. Nothing is pushed. No branch tracks a remote branch. Every worktree is clean.

| Project (folder) | Base on GitHub | Commits (oldest first) |
|---|---|---|
| austria-data-job-market-intelligence (worktree of the `-public` clone) | 1648808 | de13f68 |
| warehouse_humanoid_tco | 9027334 | b9e205e, dfe5363, 92f4bf1, 084f4cb, 571e29d |
| austrian-mmm-budget-optimizer | 948dbcb | c7907db, f6430e8, f86893f, 124c89e |
| energy-procurement-risk-analyzer | dc62a20 | 1c5305a, 74b2e64, d8cad54 |
| decision-analytics-reconstruction | b530214 | 7066359, 1479320, 3237ccd |
| metric_lineage_simulator | 663d046 | 069aba7, bc927db, f24c42b |
| NextMove | 1ec5fd0 (master) | f2e9476, b911c85 |
| Chart_Audit_Framework, funnel_correlation_py, governance-bootstrap, brazil_presidential_election_prediction_2026 | — | none (unchanged) |

Notes:

* Several commits end with `Co-Authored-By: Claude Fable 5.1`. Sub-agents of other models wrote them, and one commit names Opus 5.5. The text came from the brief's template. Change the trailer if you want it exact.
* The MMM project also changed `scripts/readme_template.md`, `scripts/render_readme.py` and `tests/test_readme_numbers.py`. The README is generated, and a project test compares it with a fresh render.
* The warehouse project also regenerated `governance/CLAIMS_LEDGER.md`. A project check ties it to README line numbers.
* Gate repository (`C:\Users\Benutzer1\orca\workspaces\braga-portfolio-docs\frogfish`, branch `RafaelBraga-Kribitz/frogfish`, base 9121622): changes are NOT committed. The brief allows commits in the portfolio repositories only. Changed: `readme_quality/prose.py` (new), `checks.py`, `cli.py`, `manifest/requirements.yaml` (version 1.5.0, three `recommended` checks), `manifest/portfolio.yaml` (Brazil path), `docs/README_STANDARD.md`, `README.md`, `docs/readme-audit-latest.md`, `tests/test_prose.py` (new), and the new folders `docs/viability/` and `docs/business-case/`.
* Tests: 118 pass, 1 skipped in the gate repository. The gate repository passes its own gate.

## 5. Decisions for you

| # | Question | Recommendation and evidence |
|---|---|---|
| 0 | Which hourly rate and company-size ranges may the business cases assume? | Keep €35 to €60 per hour until you answer. It rests on the advertised analytics floor (€50.0k, snapshot 2026-10-18). |
| 1 | `governance-bootstrap`, `funnel_correlation_py`: full rewrite, or "internal tool" label? Same question for `Chart_Audit_Framework` and the Brazil forecast. | Freeze with the ten-line summary on each viability page. A rewrite adds 0 to 1 point for `governance-bootstrap`, `funnel_correlation_py` and the Brazil forecast (S2 against S1). Archive `Chart_Audit_Framework`: it tracks 3,410 third-party files with no licence grant. |
| 2 | `dsx`, `bk-viz`: clone or remove from the registry? | Clone them. The gate cannot audit them, and `bk-viz` is the chart theme the other repositories should declare. |
| 3 | Promote the three plain-language checks to `required` now, or later? | Later. All audited READMEs pass `plain_language`. Only the Brazil README fails `no_internal_codes` (forecast horizons `T-14`, `T-30`). Three READMEs still miss a decision owner. Promote after you decide on the "sunk" READMEs. |
| 4 | Send your own hours per project. | The estimate is 4 h per commit day with ±50 %. It undercounts squashed and pre-commit work. |
| 5 | Which alternative is the 2026 opportunity cost? | The pages show all three: applications, German, next project. |
| 6 | Copy the new public market-intelligence README into `src/publish/public_overlay/README.md` in the private repository. | The next export overwrites the public README otherwise. That file has uncommitted edits, so I did not touch it. |
| 7 | Update the registry for facts that changed. | Energy: the descriptor is already fixed on `main` (PR 11); check whether `incomplete: true` should go. Metric driver tree: `demo_reason` says the UI is not built, but the README shows it. MMM: the primary chart does not show the answer; the gain histogram does. |
| 8 | Fix the gate check `communication.chart_caption`. | It stops at an HTML comment line between a chart and its caption. That is why the energy README warns. Fix it in the gate repository with a test. |
| 9 | Regenerate chart images that still show internal codes or mixed signs. | Decision analytics ("C1", "Retrodiction"), NextMove ("ADR-004"), MMM ("Layer R", "Layer P") and warehouse charts 1, 4 and 6 (sign and axis label). Agents may not edit images. |
| 10 | Check the warehouse numbers. | The Monte Carlo mean (€461,414) is above the table cost (€452,706). The repository does not say whether the Monte Carlo run includes residual value. |
| 11 | Check the MMM sampler export. | `reports/exports/proof_sampler_gates.csv` says target acceptance 0.99 and 1000 draws. `diagnostics.json` says 0.95 and 2000. The README follows `diagnostics.json`. |
| 12 | Choose names the repositories pin. | The warehouse tests pin the old wording, such as "Lean Human + AMR Team" and a 57-word recommendation that contains "F-222". A cleaner fix changes the charter and the check. |
| 13 | Delete the worktree folder after you merge. | `C:\Users\Benutzer1\Dev\_readme-business-acumen-2026-10\`. |
| 14 | Split the market-intelligence README into a short page and a separate map page (plan item 1). | Not done. The brief limited the change to `README.md`. |
| 15 | Is "campaign manager" the right role for the decision analytics README? | The repository says only "a campaign". The role comes from the plan. |

## 6. What I could not verify

* **Hours.** All hours are estimates from git. The first commit of several projects already holds weeks of work.
* **Euro values and probabilities** in the business cases are assumptions. No public benchmark exists for most of them.
* **Tests I could not run.** Metric driver tree: three governance tests need npm packages, knip and radon. Warehouse: six tests need data, dbt, pdftotext or pyright (the original README fails the same six). NextMove: the Power BI test needs pandas. Energy: two tests need the private `bk_theme` package. MMM: one chart test fails on the base commit too (borrowed environment).
* **Codex review limits.** Codex ran with a read-only shell. It could not run tests, hash files or open images. I ran the project tests myself. The first NextMove approval missed a broken project test. The warehouse rewrite broke six project checks that Codex never saw. The agents and I found both by running the tests.
* **Not re-inspected.** The last fix commits for decision analytics (3237ccd), metric driver tree (f24c42b), energy (d8cad54) and MMM (124c89e) used up the inspection budget of 2 rounds. I verified each myself with the gate, the prose tool and the project tests that read the README. I did not send them to a third inspection.
* **Known gap in the MMM README (open, not fixed).** In partial-artifact states the "Start here" table still links to `#dashboard` (and `#validation`), which the renderer omits or replaces. The normal full-artifact README is correct. The fix: in `scripts/readme_template.md` condition each navigation link on the same flag as its target section, and add an assertion to `test_render_survives_missing_artifacts` that every local heading link in the rendered README resolves. The project used its two fix rounds, so I left it open.
* **Prose tool.** The passive-voice share is a heuristic. The sentence splitter treats an abbreviation list as exceptions only.
* **Plan facts.** The git table in `BUSINESS_ACUMEN_PLAN_2026-10-28.md` is stale. The viability pages say where they differ from it.
* **Review of the gate repository.** Codex inspected it twice. Round 1 found six issues (prose tool: soft-wrapped lines and indented code; scoring scales; stale evidence for the market-intelligence page; the DAR contradiction in the plan; one arithmetic slip). All six are fixed. Round 2 found four issues: two prose-tool edge cases (codes that wrap over a line end; quoted and long code fences) and a flaw in the energy business case (a P95 reduction is not a cash saving; the page now values two stated buyer objectives). All three are fixed. The fourth is the open MMM link gap above. **The fixes after round 2 are verified by me (118 tests pass, gate audit exit 0) but not re-inspected**, because the inspection budget of 2 rounds is used up. The plan itself was re-reviewed after its amendment and approved in round 5 of 5. The full log, with every finding, is `PLAN-REVIEW-LOG.md` in `C:/Users/Benutzer1/AppData/Roaming/orca/chat-scratch/77d3e2c3766197b2999d17e78bfbfb70/claudex/`, outside the repository.
