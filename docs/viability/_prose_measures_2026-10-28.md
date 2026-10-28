# Prose measures of the portfolio READMEs, 2026-10-28

Tool: `python -m readme_quality prose` (gate repository, manifest 1.5.0, paragraph-joining sentence model). Before = the published README at `origin/<default>` on 2026-10-28. After = the README on branch `readme/business-acumen-2026-10`. Passive voice is a heuristic. A sentence is "long" when it has more than 25 words. Targets: ste_share at least 80 %, long_share under 20 %, internal_codes 0, a named decision owner.

| Project | Before: sentences / long % / ste % / codes / owner | After: sentences / long % / ste % / codes / owner |
|---|---|---|
| austria-data-job-market-intelligence | 148 / 14.9 / 72.3 / 6 / no | 237 / 0.0 / 99.6 / 0 / yes |
| warehouse_humanoid_tco | 60 / 21.7 / 75.0 / 8 / no | 118 / 4.2 / 94.9 / 0 / yes |
| austrian-mmm-budget-optimizer | 94 / 27.7 / 56.4 / 17 / yes | 224 / 1.8 / 92.9 / 0 / yes |
| energy-procurement-risk-analyzer | 67 / 22.4 / 62.7 / 2 / yes | 167 / 2.4 / 92.8 / 0 / yes |
| decision-analytics-reconstruction | 87 / 14.9 / 79.3 / 16 / yes | 158 / 2.5 / 91.1 / 0 / yes |
| metric_lineage_simulator | 67 / 10.4 / 80.6 / 2 / no | 154 / 1.3 / 96.1 / 0 / yes |
| NextMove | 47 / 29.8 / 59.6 / 7 / no | 122 / 2.5 / 95.1 / 0 / yes |
| Chart_Audit_Framework | 51 / 3.9 / 86.3 / 0 / no | unchanged |
| funnel_correlation_py | 30 / 6.7 / 90.0 / 0 / yes | unchanged |
| governance-bootstrap | 45 / 8.9 / 86.7 / 0 / no | unchanged |
| brazil_presidential_election_prediction_2026 | 214 / 13.1 / 68.2 / 5 / no | unchanged |

The gate result of the published READMEs (run B in `_gate_baseline_2026-10-28.txt`): 11 of 11 local READMEs pass the required checks. The stale local clones failed only because they were 8 to 185 commits behind GitHub.

Note: the first measures quoted in the plan file and the earlier drafts of the analysis pages (about 15 %, 40 % and 55 % STE) are estimates from the stale-clone audit. They are replaced by the table above.
