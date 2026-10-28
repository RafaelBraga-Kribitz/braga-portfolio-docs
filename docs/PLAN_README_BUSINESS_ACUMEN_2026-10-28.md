# Plan: execute the business-acumen README brief (2026-10-28)

Owner: Rafael Braga-Kribitz. Coordinator: the Claude Code session (Fable 5.1) in the worktree
`C:\Users\Benutzer1\orca\workspaces\braga-portfolio-docs\frogfish`, branch `RafaelBraga-Kribitz/frogfish`.
Source brief: `docs/AGENT_BRIEF_README_BUSINESS_ACUMEN_2026-10-28.md`. Source detail:
`docs/BUSINESS_ACUMEN_PLAN_2026-10-28.md`. This plan does not repeat them; it states what changes after
reconnaissance, how the work is split, and how it is proved.

## 1. Goal and acceptance criteria

Goal: every public portfolio README shows business acumen and clear stakeholder communication, and the
gate repository holds a retrospective viability page and an ex-ante business case per project.

Done is observable when all of the following hold:

| # | Criterion | Proof |
|---|---|---|
| A1 | Every registered repository with a local worktree passes the gate (exit 0). | `BRAGA_REPOS_ROOT=<WORK> python -m readme_quality portfolio` shows PASS or PASS_WITH_EXCELLENCE for the 11 local repositories; `dsx` and `bk-viz` are FAIL rows (no local clone, open question 2). The same command with `--json` shows, for those two, an empty `findings` list and the checkout-not-found note (`run_portfolio` never audits a missing folder; the text renderer does not print the note). |
| A2 | Each rewritten README reaches the three writing rules: STE share ≥ 80 %, 0 bare internal codes in prose outside a legend, decision owner named before the first H2. | `python -m readme_quality prose --repo <path>` prints `ste_share >= 80`, `internal_codes = 0`, `decision_owner = yes`. |
| A3 | Rewritten READMEs keep their intellectual content. | Reviewer diff: no section's substance deleted; renamed or moved only. Inspection by Codex per repository. |
| A4 | `docs/viability/<project>.md` exists for all 11 local projects with the structure in brief §7, plus `docs/viability/README.md` (summary table + 3 lessons). | `ls docs/viability` lists 11 pages + README + `_gate_baseline_2026-10-28.txt` + `_assumptions.md`; each page has the 6 H2 headings of brief §7. |
| A5 | `docs/business-case/<project>.md` exists for all 11 local projects with the structure in brief §7b, plus `docs/business-case/README.md` (calibration table + 3 lessons). | `ls docs/business-case` lists 11 pages + README; each page has the 9 H2 headings of brief §7b (Money at stake per decision cycle, Status quo, Options, Outcome tree for "build full", Cost, Result, Sensitivity, Verdict, Calibration against the retrospective); every probability has a range and a basis; every euro value has unit, period, source. |
| A6 | Three new gate checks exist at `recommended` with tests, a `prose` CLI subcommand, manifest `1.5.0`, promotion rows in `docs/README_STANDARD.md` §6. | `python -m pytest -q` passes; `python -m readme_quality explain communication.plain_language` (and the two others) prints severity `recommended`; the gate repository passes its own gate. |
| A7 | Each portfolio worktree whose README was rewritten (WP2, and WP4 for verdicts "worth it" or "open") has ≥ 1 commit on `readme/business-acumen-2026-10`; worktrees of projects with verdict "sunk" stay unchanged at `origin/<default>` (their proposal lives in the gate repository), with one exception: `decision-analytics-reconstruction` is frozen by D-034 and brief step 4 requires summary-level README edits, so its rewrite is committed; nothing pushed. | For rewritten ones: `git -C <wt> log --oneline origin/<default>..HEAD` non-empty. For sunk ones: that log is empty and `git -C <wt> status --short` is empty. For all: `git -C <wt> status -sb` shows no upstream. |
| A8 | Final report in brief §8 order, in ASD-STE100. | Delivered as the session's final message and saved to `docs/REPORT_README_BUSINESS_ACUMEN_2026-10-28.md`. |

## 2. What reconnaissance changed (read before the work packages)

| Finding | Evidence | Consequence |
|---|---|---|
| Every local clone under `C:\Users\Benutzer1\Dev` is behind GitHub by 8 to 185 commits, and the README differs on every one. | `git fetch` + `git rev-list --count <default>..origin/<default>` on 2026-10-28 (see log). | The brief's audit scores, STE estimates and "no README" claims were measured on stale files. All work targets the published README at `origin/<default>`. |
| `NextMove`, `metric_lineage_simulator`, `Chart_Audit_Framework` have READMEs on GitHub (1,541 / 2,083 / 1,318 words). | Worktree checkouts of `origin/master` and `origin/main`. | Step 9 becomes "apply the recipe to the existing README if the verdict is worth it or open"; templates are not needed. |
| 11 of 14 registered repositories already pass the structural gate on the published README; `fix --dry-run` changes nothing. | `portfolio` run on the worktrees, 2026-10-28; saved as `docs/viability/_gate_baseline_2026-10-28.txt`. | Step 0 is a record, not a repair. All effort goes to the three writing rules, the analyses and the new checks. |
| The three FAILs are `dsx`, `bk-viz` (no local clone) and `braga-portfolio-docs` itself (outside the worktree root; passes with `BRAGA_REPOS_ROOT=Dev`). | Same run. | Flag `dsx` and `bk-viz` (open question 2). Audit the gate repository with `--repo .`. |
| The public market-intel README is in the clone `austria-data-job-market-intelligence-public` (remote = GitHub `austria-data-job-market-intelligence`). The folder `austria-data-job-market-intelligence` is the private repository, with no remote, 12 dirty files, and the overlay source `src/publish/public_overlay/README.md` under uncommitted edit. | `git remote -v`, `git status`, `src/publish/export_public.py` lines 77 to 81. | Rewrite the README in a worktree of the public clone. Do not touch the private repository. Flag: Rafael must copy the final README into the overlay source before the next export, or the export overwrites it. |
| Most clones are on feature branches with uncommitted work (warehouse 12 files, EPRA 14, DAR 6, MLS 6, Chart_Audit_Framework 4,919 staged deletions). | `git status --short`. | Never branch inside those working trees. One worktree per repository under `C:\Users\Benutzer1\Dev\_readme-business-acumen-2026-10\<registry path>`, branch `readme/business-acumen-2026-10` from `origin/<default>`. Created 2026-10-28 (Chart_Audit_Framework needed `-c core.longpaths=true`). |
| Registry path for the Brazil project did not match any folder. | `manifest/portfolio.yaml` line 226. | Changed to `brazil_presidential_election_prediction_2026` (brief step 8). The worktree folder uses that name. |
| The prose probe on the published READMEs gives STE-ok shares of 41 % (NextMove) to 78 % (funnel_correlation_py); internal codes remain in market-intel (BQ45, Layer 1/2/3), MMM (Layer P/R/D, 26 hits), DAR (F-021…, Module A/B/C, 36 hits), warehouse (F-222…). | Probe script, 2026-10-28 (heuristic: ≤ 25 words and no be-verb + participle). | Confirms the brief's three problems. Renames in the plan file are starting points; each agent verifies them against the real README. |

`<WORK>` below means `C:\Users\Benutzer1\Dev\_readme-business-acumen-2026-10`.

## 3. Approach and work packages

The coordinator plans, briefs, verifies and reports. Sub-agents execute. Packages marked ∥ run in parallel.

| WP | Scope | Agent model | Depends on | Definition of done |
|---|---|---|---|---|
| WP0 | Record the baseline: copy the gate table to `docs/viability/_gate_baseline_2026-10-28.txt` (both runs: stale clones and worktrees, labelled). Write `docs/viability/_assumptions.md` (section 5 below). | coordinator (one command) | — | Files exist and are referenced by every analysis page. |
| WP1 | Prose tooling and the three checks in the gate repository: `readme_quality/prose.py` (sentence model), `prose` CLI subcommand, checks `plain_language`, `no_internal_codes`, `decision_owner` at `recommended`, tests, manifest `1.5.0`, standard §6 rows, `docs/readme-audit-latest.md` regenerated. | sonnet | — | `pytest` green; `explain` prints the three ids; `prose --repo` works on every worktree; gate repository passes `audit --repo .`. |
| WP2 ∥ | README rewrite, one agent per repository, five flagships: market-intel, warehouse TCO, MMM, DAR (frozen: summary-level edits only), EPRA. Recipe = brief §6 "The recipe". Measure before and after with WP1's `prose`. Commit on the worktree branch. | sonnet (market-intel: opus, worst STE share and pinned first) | WP1 | `audit --verbose` exit 0; `prose` meets A2; before/after numbers, codes removed and renames applied returned in the agent's report; one commit per repository. |
| WP3 ∥ | Viability page (brief §7) **and** business case (brief §7b) for each of the 11 local projects, one agent per project, reading the real repository and `_assumptions.md`. The planner's priors are hypotheses to test. For NextMove, MLS and Brazil the agent identifies the persona from the repository first. | opus for the five flagships; sonnet for the six others | WP0 | Both pages exist with the required headings; every number has unit, period, source; every probability has a range and a basis; verdict uses the brief's four-term vocabulary; calibration section filled. |
| WP4 | Conditional README work for the six non-flagship projects, after the coordinator has read the WP3 verdicts: verdict "worth it" or "open" → apply the recipe to the existing README (as WP2). Verdict "sunk" → **do not replace the README**; add the proposed 10-line summary README to the viability page under "Proposed summary README" and flag for Rafael (open question 1). | sonnet per repository | WP1, WP3 | As WP2 for rewritten ones; for sunk ones the proposal block exists and the README is unchanged. |
| WP5 | Summaries: `docs/viability/README.md` (table: project, hours, opportunity cost, S1, S2, verdict, lesson; three strongest lessons) and `docs/business-case/README.md` (calibration table; three lessons for choosing the next project). Fill the calibration table in `docs/BUSINESS_ACUMEN_PLAN_2026-10-28.md`. | sonnet | WP3, WP4 | Tables match the pages (coordinator spot-checks 3 rows each). |
| WP6 | Final gate table on the worktrees and on the gate repository; final report (brief §8) written to `docs/REPORT_README_BUSINESS_ACUMEN_2026-10-28.md`; leave the gate repository changes uncommitted for the owner's sign-off (the brief authorizes commits only in the portfolio repositories; see section 11). No push anywhere. | coordinator | all | A1, A7, A8. |

Independent inspection: Codex inspects the gate repository (base `9121622`) and each rewritten portfolio
worktree (base `origin/<default>` sha recorded in the log) in fresh sessions. Fix rounds ≤ 2, inspection
rounds ≤ 2 per repository.

## 4. Key decisions, trade-offs and non-goals

1. **Worktrees from `origin/<default>` instead of branches in the dirty clones.** Keeps Rafael's uncommitted work untouched and audits what GitHub shows. Cost: the worktree root is a new folder under `Dev`; Rafael deletes it after merging. Alternative rejected: `git checkout -b` inside dirty trees (would carry or block on unrelated changes).
2. **Public market-intel README is the deliverable, not the private README.** Hiring managers read the public one; the hard boundaries forbid publishing scraper detail. Cost: a manual sync into the private overlay source.
3. **Sunk projects keep their README.** The brief's "write only the 10-line summary README" was written for missing READMEs. Replacing a gate-passing README with 10 lines deletes content and fails the gate, and open question 1 says that choice is Rafael's. The summary is delivered as a proposal.
4. **Measurement is code, not hand counting.** The `prose` subcommand is the single definition of "STE share" for before and after numbers. Its passive-voice test is a heuristic (be-verb followed by a past participle) and is reported as such. The `plain_language` check uses sentence length only, as the plan file specifies.
5. **Checks land at `recommended`.** Promotion to `required` is open question 3. No existing check is weakened.
6. **Hours are git estimates until Rafael's log arrives** (open question 4). One formula for every page, in `_assumptions.md`.
7. **Hourly rate and company-size ranges are labelled assumptions** anchored on the advertised analytics floor marker (open question 0).

Non-goals: cloning `dsx` or `bk-viz`; pushing or opening pull requests; changing any license; touching the
private market-intel repository; editing code outside the gate repository; generating new charts or
architecture diagrams; promoting any check to `required`; deciding open questions 0 to 5.

## 5. Shared assumptions for the analyses (copied into `docs/viability/_assumptions.md`)

| Item | Value | Source and caveat |
|---|---|---|
| Hours per project | central = distinct commit days on the default branch × 4 h; range ±50 %. Commit count is a secondary proxy and is inflated in agent-assisted repositories (EPRA: 395 commits in 12 days). | Estimate from git, 2026-10-28. Replaced by Rafael's log when supplied (open question 4). |
| Loaded hourly rate | €35 to €60 per hour; central €45. | Assumption: advertised analytics floor `floor_analytics_eur` = €50.0k per year (vintage 2026-10-18) × 1.3 employer loading ÷ 1,700 h ≈ €38; upper bound for a senior analyst. Open question 0. |
| Opportunity cost units | Applications: 2 h per weekday block, 8 to 10 per week → about 1 to 1.25 h per application. German: 1 h = 1 h of study toward B1 (A1.2 actual; owner expects about 2 months per sublevel at 20 h/week → about 640 h to B1). Next project: the B2B SaaS revenue-retention project, size ≈ the median git estimate across the five flagships. | `career-knowledge-core.md` (owner-stated 2026-10-19 capacity; D-034). Open question 5: all three shown on every page. |
| Market shares | SQL 40 %, Python 39 %, data quality 31 %, cloud 32 %, ETL 20 %, Azure 19 %, Power BI 17 %, GenAI 18 %, statistics 16 %; German stated in 42 % of ads; 147 English-no-German ads nationally. | `career-knowledge-core.md`, snapshot vintage 2026-10-18, core n = 699. Quote as "ads mention". |
| Scarcity list | SQL, data quality, modelling/warehouse, Azure/Databricks, Power BI, READMEs with question → result → limitations. | Same file, GitHub supply layer. |
| Outcome measure | Hiring-evidence score (0 to 2 on five items), not conversions: 0 applications sent as of 2026-10-28. | Owner-stated 2026-10-06. Every page states this. |
| Scenario scoring | S0 not built, S1 as published today (origin), S2 after this plan, S3 extended (named step). Total /10. One line of evidence per cell. | Brief §7. |

## 6. Writing rules enforced on every README and on the report

The three rules of brief §4, the hard constraints of brief §5, the recipe of brief §6. Add: the first
prose paragraph names who decides and what they choose; every code that stays in a file name gets a plain
name and a one-line legend; method, priors, sampler, governance and agent notes sit below Limitations.
Keep every heading inside the gate's alias families (`readme_quality/checks.py` lines 44 to 63).

## 7. Toolchain

Python 3.12.10 in the gate repository (`pytest` 68 passed, 1 skipped at the start). Git worktrees as in
section 2. Codex CLI 0.165.0 for review and inspection (model: CLI default, requested none; observed value
recorded from `result.json`). Claude Code 2.1.312 sub-agents build. No other tool is required; the gate
has no network dependency. Image inspection: sub-agents open each chart they caption.

## 8. Verification

Run from the gate worktree unless stated. `<WORK>` as in section 2.

| Step | Command | Expected |
|---|---|---|
| V1 | `python -m pytest -q` | all pass (≥ 68 + new tests), 0 failures |
| V2 | `python -m readme_quality audit --repo . --verbose` | exit 0 |
| V3 | `BRAGA_REPOS_ROOT=<WORK> python -m readme_quality portfolio` (text) and the same with `--json` | Text: 11 of 14 PASS; the 3 FAIL rows are `dsx`, `bk-viz`, `braga-portfolio-docs`. JSON: those three have an empty `findings` list and the checkout-not-found note (the gate repository itself is proved by V2) |
| V4 | for each rewritten `<p>`: `python -m readme_quality audit --repo <WORK>/<p> --verbose` | exit 0 |
| V5 | for each rewritten `<p>`: `python -m readme_quality prose --repo <WORK>/<p>` | `ste_share >= 80`, `internal_codes = 0`, `decision_owner = yes`; the same command on `git show origin/<default>:README.md` gives the "before" numbers |
| V6 | `python -m readme_quality explain communication.plain_language` (and `no_internal_codes`, `decision_owner`) | prints the requirement at `recommended` |
| V7 | `grep -c "^## " docs/viability/<p>.md` / `docs/business-case/<p>.md` | 6 / 9 H2 headings per page, with the names listed in A4 and A5 (plus the optional "Proposed summary README" H2 on sunk viability pages) |
| V8 | for each `<p>`: `git -C <WORK>/<p> log --oneline origin/<default>..HEAD` and `git -C <WORK>/<p> status -sb` | rewritten projects (including the frozen `decision-analytics-reconstruction`): ≥ 1 commit; other sunk projects: 0 commits; all: no upstream, clean tree (A7) |
| V9 | Old and new on the same input: the probe script and the new `prose` command agree on the before numbers within 5 points for the 11 READMEs (sanity check of the sentence model). | table in the log |
| V10 | Manual: coordinator reads every rewritten README once, checks the top box (who decides, decision, answer with unit, caveat, chart), and opens 3 random analysis pages per kind for unit/source completeness. | noted in the log |

Codex inspection (fresh session per repository) is the independent check for A3 and for the analysis pages.

## 9. Open decisions left to Rafael (not decided here)

Brief §9 items 0 to 5, unchanged. Plus from reconnaissance:

6. Sync of the rewritten public market-intel README into `src/publish/public_overlay/README.md` (private repository, under uncommitted edit).
7. Keep or delete the worktree root `<WORK>` after merging the 11 branches.
8. Whether `NextMove`, `metric_lineage_simulator`, `Chart_Audit_Framework` and the Brazil forecast READMEs, which exist on GitHub, should be rewritten even where the viability verdict is "sunk".

## 10. Risks

| Risk | Mitigation |
|---|---|
| A sub-agent invents a number or renames a chart it did not open. | Brief §5 in every agent prompt; coordinator spot-checks numbers against repository files; Codex inspection per repository. |
| STE rewriting flattens meaning or drops caveats. | Rule: every caveat moves, never disappears; inspection diff lists removed sentences. |
| The `prose` heuristics misclassify. | Reported as heuristics; `plain_language` check uses length only; tests pin behaviour on fixtures. |
| Windows long paths in Chart_Audit_Framework. | Worktree created with `core.longpaths=true`; agents do not touch the references tree. |
| Codex quota or malformed review. | No cross-model fallback; wait or record the unreviewed path with Rafael's explicit choice. |

## 11. Deviations recorded during the build (2026-10-28)

| # | Deviation | Reason |
|---|---|---|
| 1 | `decision-analytics-reconstruction` README rewritten at summary level although its verdict is "sunk". | Brief step 4 requires it (frozen project). A7, V8 and WP2 now say so. |
| 2 | The gate repository is not committed. | The brief authorizes commits in the portfolio repositories only. The diff is ready for sign-off. |
| 3 | Plan-file renames replaced: "Worst realistic yearly cost (1 year in 20)" for P95 became "95th-percentile simulated annual cost (exceeded in about 1 year in 20)"; "Today's 8-worker crew" became "Modeled legacy 8-worker reference". | Independent inspection showed both plan-file names state something the evidence does not support (P95 is a percentile, not a worst case; the 8-worker crew is a modeled legacy baseline, not a real site). |
| 4 | For `austrian-mmm-budget-optimizer` the files `scripts/readme_template.md`, `scripts/render_readme.py` and `tests/test_readme_numbers.py` were edited as well as `README.md`. | The README is generated, and a project test fails if the template and the README differ. |
| 5 | For `warehouse_humanoid_tco`, `governance/CLAIMS_LEDGER.md` was regenerated. | A project check ties the claims ledger to README line numbers. |
| 6 | Every README agent also ran the project tests and CI scripts that read the README. | Codex cannot run tests; two rewrites had broken project tests that the gate does not see. |
| 7 | Fix and inspection rounds: README work followed the configured budget (2 fix rounds, 2 inspections); the final fix commits of `decision-analytics-reconstruction`, `metric_lineage_simulator`, `energy-procurement-risk-analyzer` and `austrian-mmm-budget-optimizer` were verified by the host and not re-inspected. | `MAX_INSPECTION_ROUNDS = 2`. Reported as unreviewed edits. |
