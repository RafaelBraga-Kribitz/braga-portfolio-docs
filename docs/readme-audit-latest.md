# README Quality Gate — portfolio run

**Standard:** v1.5 · **Manifest:** v1.5.0 · **Run:** 2026-10-28 · **Command:** `BRAGA_REPOS_ROOT=<worktrees of origin/<default>> python -m readme_quality portfolio`

This run audits the published READMEs as rewritten on branch `readme/business-acumen-2026-10` in each
repository (one commit series per repository, not pushed). The earlier run of 2026-09-21 (v1.3) is in the
git history of this file. The baseline before the rewrites is in
[`viability/_gate_baseline_2026-10-28.txt`](viability/_gate_baseline_2026-10-28.txt).

`dsx` and `bk-viz` have no local checkout, so the gate cannot audit them. Their rows show FAIL in a raw run
for that reason only. `braga-portfolio-docs` sits outside the worktree root and is audited with `--repo .`.
`brazil-2026-election-forecast`, `governance-bootstrap`, `funnel_correlation_py` and `Chart_Audit_Framework`
keep their published README: the viability verdict is "sunk" and the owner has not decided (agent brief,
open question 1).

## Gate result

```text
Repository                            Type         Status                 Open items
------------------------------------------------------------------------------------------------
decision-analytics-reconstruction     analytical   PASS_WITH_EXCELLENCE   1 warning(s)
warehouse_humanoid_tco                analytical   PASS_WITH_EXCELLENCE   1 warning(s)
austrian-mmm-budget-optimizer         analytical   PASS_WITH_EXCELLENCE   
austria-data-job-market-intelligence  analytical   PASS_WITH_EXCELLENCE   
energy-procurement-risk-analyzer      analytical   PASS_WITH_EXCELLENCE   1 warning(s)
governance-bootstrap                  framework    PASS                   1 warning(s)
dsx                                   framework    FAIL                   no local checkout
funnel_correlation_py                 library      PASS                   
bk-viz                                library      FAIL                   no local checkout
NextMove                              application  PASS                   
metric_lineage_simulator              application  PASS                   
Chart_Audit_Framework                 framework    PASS                   1 warning(s)
brazil-2026-election-forecast         analytical   PASS                   4 warning(s)
braga-portfolio-docs                  docs         PASS                   audited with `--repo .`
------------------------------------------------------------------------------------------------
12 of 12 audited repositories PASS. 2 of 14 (`dsx`, `bk-viz`) have no local checkout and are not audited.
```

## Recommended-warning backlog

9 warnings across the audited repositories. Warnings marked "new in v1.5" come from the three
plain-language checks added in this version.

| Repository | Requirement | Since | Detail |
|---|---|---|---|
| `decision-analytics-reconstruction` | `excellence.why` | pre-existing | no why section |
| `warehouse_humanoid_tco` | `technical.stack` | pre-existing | no stack table |
| `energy-procurement-risk-analyzer` | `communication.chart_caption` | pre-existing | no caption within two lines of the primary chart (reports/executive_charts/01_wrong_strategy_cost.png); name what it shows and what the reader should take from it |
| `governance-bootstrap` | `communication.decision_owner` | new in v1.5 | the text before the first H2 names no role that decides; write who decides and what they choose |
| `Chart_Audit_Framework` | `communication.decision_owner` | new in v1.5 | the text before the first H2 names no role that decides; write who decides and what they choose |
| `brazil-2026-election-forecast` | `communication.no_internal_codes` | new in v1.5 | 5 bare internal code(s) in prose outside a legend: L61 T-14, L156 T-30, L156 T-14, L270 T-14, L270 T-30; give each a plain name or a legend |
| `brazil-2026-election-forecast` | `communication.decision_owner` | new in v1.5 | the text before the first H2 names no role that decides; write who decides and what they choose |
| `brazil-2026-election-forecast` | `excellence.claim_tracing` | pre-existing | no claim tracing |
| `brazil-2026-election-forecast` | `excellence.why` | pre-existing | no why section |
