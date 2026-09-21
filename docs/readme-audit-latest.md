# README Quality Gate — portfolio run

**Standard:** v1.3 · **Manifest:** v1.3.0 · **Run:** 2026-09-21 · **Command:** `BRAGA_REPOS_ROOT=.. python -m readme_quality portfolio`

Every repository passes at `required` severity. The `recommended` warnings below are the v1.3
remediation backlog; they are expected and enumerated, not hidden in a warning count.

## Gate result

```text
Repository                            Type         Status                 Open items
------------------------------------------------------------------------------------------------
decision-analytics-reconstruction     analytical   PASS_WITH_EXCELLENCE   5 warning(s)
warehouse_humanoid_tco                analytical   PASS_WITH_EXCELLENCE   4 warning(s)
austrian-mmm-budget-optimizer         analytical   PASS_WITH_EXCELLENCE   4 warning(s)
austria-data-job-market-intelligence  analytical   PASS_WITH_EXCELLENCE   5 warning(s)
energy-procurement-risk-analyzer      analytical   PASS_WITH_EXCELLENCE   2 warning(s)
governance-bootstrap                  framework    PASS                   2 warning(s)
dsx                                   framework    PASS                   1 warning(s)
funnel_correlation_py                 library      PASS                   2 warning(s)
bk-viz                                library      PASS                   
NextMove                              application  PASS                   1 warning(s)
metric_lineage_simulator              application  PASS                   2 warning(s)
Chart_Audit_Framework                 framework    PASS                   2 warning(s)
braga-portfolio-docs                  docs         PASS                   
------------------------------------------------------------------------------------------------
13/13 PASS
```

## Recommended-warning backlog

30 warnings across 11 repositories. 15 of them are new in v1.3.

| Repository | Requirement | Since | Detail |
|---|---|---|---|
| `decision-analytics-reconstruction` | `technical.stack` | pre-existing | no stack table |
| `decision-analytics-reconstruction` | `communication.chart_theme` | new in v1.3 | bk-viz is not declared in pyproject.toml; charts here will not look like the rest of the portfolio (bk-viz README: "If two charts from different repos do not look… |
| `decision-analytics-reconstruction` | `communication.chart_caption` | new in v1.3 | no caption within two lines of the primary chart (reports/eda/C1_forecast_timeline.png); name what it shows and what the reader should take from it |
| `decision-analytics-reconstruction` | `communication.message_heading` | new in v1.3 | no H2 or H3 in the results section carries a number (5 heading(s) checked); a heading that states the finding beats one that names the topic |
| `decision-analytics-reconstruction` | `excellence.why` | pre-existing | no why section |
| `warehouse_humanoid_tco` | `technical.stack` | pre-existing | no stack table |
| `warehouse_humanoid_tco` | `communication.alt_text` | new in v1.3 | 6 of 8 figure(s) have empty alt text |
| `warehouse_humanoid_tco` | `communication.chart_theme` | new in v1.3 | bk-viz is not declared in pyproject.toml, requirements.txt; charts here will not look like the rest of the portfolio (bk-viz README: "If two charts from different… |
| `warehouse_humanoid_tco` | `communication.chart_caption` | new in v1.3 | no caption within two lines of the primary chart (./reports/executive_charts/01_tco_npv_ranking.png); name what it shows and what the reader should take from it |
| `austrian-mmm-budget-optimizer` | `honesty.falsification` | pre-existing | no 'reconsider if …' / 'would change this conclusion' condition |
| `austrian-mmm-budget-optimizer` | `communication.chart_caption` | new in v1.3 | no caption within two lines of the primary chart (reports/layer_r/channel_contributions.png); name what it shows and what the reader should take from it |
| `austrian-mmm-budget-optimizer` | `communication.message_heading` | new in v1.3 | no H2 or H3 in the results section carries a number (2 heading(s) checked); a heading that states the finding beats one that names the topic |
| `austrian-mmm-budget-optimizer` | `excellence.why` | pre-existing | no why section |
| `austria-data-job-market-intelligence` | `communication.alt_distinct` | new in v1.3 | L12: alt text is copied from the banner; describe what this chart shows |
| `austria-data-job-market-intelligence` | `communication.chart_theme` | new in v1.3 | bk-viz is not declared in requirements.txt; charts here will not look like the rest of the portfolio (bk-viz README: "If two charts from different repos do not lo… |
| `austria-data-job-market-intelligence` | `communication.figure_coverage` | new in v1.3 | 1 of 14 figures in outputs/figures/ shown in the README (need 3); show the ones that carry the argument, or say in Limitations why the rest stay in the repository |
| `austria-data-job-market-intelligence` | `communication.chart_caption` | new in v1.3 | no caption within two lines of the primary chart (outputs/figures/F03_styria_vs_austria_families.png); name what it shows and what the reader should take from it |
| `austria-data-job-market-intelligence` | `communication.message_heading` | new in v1.3 | no H2 or H3 in the results section carries a number (2 heading(s) checked); a heading that states the finding beats one that names the topic |
| `energy-procurement-risk-analyzer` | `communication.chart_theme` | new in v1.3 | bk-viz is not declared in pyproject.toml; charts here will not look like the rest of the portfolio (bk-viz README: "If two charts from different repos do not look… |
| `energy-procurement-risk-analyzer` | `excellence.why` | pre-existing | no why section |
| `governance-bootstrap` | `technical.stack` | pre-existing | no stack table |
| `governance-bootstrap` | `library.install_pin` | pre-existing | no version pin in the install line and no Releases section |
| `dsx` | `technical.stack` | pre-existing | no stack table |
| `funnel_correlation_py` | `technical.stack` | pre-existing | no stack table |
| `funnel_correlation_py` | `communication.chart_theme` | new in v1.3 | bk-viz is not declared in pyproject.toml; charts here will not look like the rest of the portfolio (bk-viz README: "If two charts from different repos do not look… |
| `NextMove` | `technical.stack` | pre-existing | no stack table |
| `metric_lineage_simulator` | `evidence.live_demo` | pre-existing | neither a hosted demo link nor a statement that none exists |
| `metric_lineage_simulator` | `technical.stack` | pre-existing | no stack table |
| `Chart_Audit_Framework` | `technical.stack` | pre-existing | no stack table |
| `Chart_Audit_Framework` | `library.install_pin` | pre-existing | no version pin in the install line and no Releases section |

## Length under the v1.3 counting

`meta.length` counts rendered lines (prose, headings, list items, table rows, images);
`meta.length_total` counts raw file lines. No project is over either ceiling, so neither
number was raised.

| Repository | Rendered / 450 | Raw / 1000 | Rendered headroom |
|---|---|---|---|
| `dsx` | 254 | 428 | 196 |
| `decision-analytics-reconstruction` | 215 | 304 | 235 |
| `bk-viz` | 161 | 246 | 289 |
| `energy-procurement-risk-analyzer` | 147 | 234 | 303 |
| `austrian-mmm-budget-optimizer` | 142 | 216 | 308 |
| `austria-data-job-market-intelligence` | 125 | 263 | 325 |
| `Chart_Audit_Framework` | 95 | 195 | 355 |
| `warehouse_humanoid_tco` | 94 | 190 | 356 |
| `funnel_correlation_py` | 87 | 176 | 363 |
| `metric_lineage_simulator` | 86 | 196 | 364 |
| `NextMove` | 82 | 173 | 368 |
| `braga-portfolio-docs` | 81 | 183 | 369 |
| `governance-bootstrap` | 71 | 182 | 379 |
