# Chart_Audit_Framework: business case, written as of 2026-06-16
Persona: BI team lead at a mid-sized Styrian manufacturer or logistics firm (team of 3 to 6 analysts). Decision owned: which dashboards and charts may go to management. Cycle: one review per quarter, with a release check per dashboard. Sign-off: head of controlling.

This is a forecast from one week before the first commit (2026-06-23). All values are assumptions with ranges unless a source is named. Rates and conventions come from `docs/viability/_assumptions.md`. That file anchors its rate on a floor measured on 2026-10-18. This anchor is later than the forecast date. It is the best one available.

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Dashboards released | 20 (10 to 40) | per quarter | Assumption (judgement) |
| Share with at least one misleading chart | 12 % (5 to 25 %) | of dashboards | Assumption (judgement). No verified benchmark |
| Share where the misread changes a decision | 20 % (10 to 30 %) | of misleading dashboards | Assumption (judgement) |
| Cost of one worse decision | €20,000 (€5,000 to €100,000) | EUR per decision | Assumption (judgement) |
| **Expected loss, no review** | **€9,600 (€250 to €300,000)** | EUR per quarter | 20 × 12 % × 20 % × €20,000 |

## Status quo
A second analyst reviews each dashboard by hand: 1 h (0.5 to 2 h) × 20 × €45 per hour = €900 per quarter (rate €35 to €60 per hour, central €45). The review catches 60 % (50 to 70 %) of defects (judgement). Residual loss = 40 % × €9,600 = **€3,840 per quarter, €15,360 per year**. Review time costs €3,600 per year.

## Options

| Option | Cost (EUR) | Time to answer | Expected value (EUR, 3 years) | Note |
|---|---|---|---|---|
| Do nothing | 0 | 0 | 0 | Residual loss stays at €15,360 per year |
| Buy or rent: public checklist plus the chart checks inside the BI tool | 360 (8 h × €45) | 1 week | **+4,130** (range +1,360 to +8,940) | Cuts residual loss 15 % (10 to 25 %); 65 % chance of use (40 to 80 %) |
| Build small: 1-page checklist plus 3 scripted checks on a CSV; 16 h (8 to 24) | 1,260 incl. run cost | 2 weeks | **+3,870** (range −890 to +9,190) | Cuts residual loss 25 % (15 to 35 %); 45 % pays off (30 to 60 %) |
| Build full: skill pack, rule registry, chart library, ratchet; 40 h (20 to 60) | 2,880 incl. run cost | 8 to 12 weeks | **+1,500** (range −6,540 to +15,210) | Hours use the git estimate. An ex-ante guess would be higher (80 to 160 h) |

"Buy" and "build small" count no review-time saving. This is conservative. Ranges are pessimistic and optimistic corners, not confidence intervals.

## Outcome tree for "build full"

| Branch | Probability (range, source) | Value if it happens (EUR over 3 years, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 25 % (15 to 40 %), judgement | +20,000: 40 % of residual loss (€6,144 per year) plus 15 % of review time (€540 per year), × 3 | +5,000 |
| Confirms the status quo | 25 % (15 to 35 %), judgement | +1,500 (0 to 3,000): avoided doubt | +375 |
| Built but not adopted | 40 % (25 to 55 %), judgement: analysts must call the tool by hand | 0 | 0 |
| Wrong, decision gets worse | 10 % (5 to 15 %), judgement: false assurance reduces manual review | −10,000 (−30,000 to −3,000) | −1,000 |
| **Sum** | 100 % | | **EV before cost +4,375** |

## Cost
Build 40 h × €45 = €1,800 (€700 to €3,600). Run 8 h per year × €45 × 3 years = €1,080. Total €2,880. Delay cost versus "do nothing": 0. Delay cost versus "buy": one quarter of forgone benefit, about €1,000.

## Result
EV(build full) = 4,375 − 2,880 = **+€1,495 over 3 years** (range −€6,540 to +€15,210). Payback = 1.6 years. Break-even probability of "pays off" = **17.5 %** (central 25 %). EV(build small) = +€3,870. EV(buy) = +€4,130.
Value of better information (EV with the tool minus EV without) = +€1,495 for the full build. The best option, "buy", gives +€4,130.

## Sensitivity

| Assumption | Central | Build full turns negative at |
|---|---|---|
| Probability the tool pays off | 25 % | below 17.5 % |
| Residual loss per year after manual review | €15,360 | below about €10,300 |

Build full beats "buy" only if the pays-off value exceeds about €30,600 over 3 years (central €20,000). This is 1.5 times the central value.

## Verdict
**Buy.** A checklist and the chart checks inside the BI tool give a higher expected value for one week of work. A 40 h framework has a 40 % chance of not being used. Evidence that would change this: a log of at least 4 chart defects per year that peer review missed, each costing at least €2,500.

## Calibration against the retrospective
Retrospective verdict (`docs/viability/Chart_Audit_Framework.md`): sunk, archive and unpin. Agree? **Yes.** Both reject the full framework.

| What the ex-ante view missed | Evidence |
|---|---|
| A legal branch. The tree has no branch for harm from bundled third-party material | 3,410 scraped chart-site files are tracked; NOTICE grants no licence for them |
| Narrow reach. Only 3 deterministic checks exist; the other rules stay language-model judged | README "Limitations"; `rules/manifest.yaml` |
| One target. The ratchet ran once (2026-07-09) on one frozen repo | `ratchet/state.json`; no automated test for `ratchet.py` |
| Scope was mostly placeholder. 207 chart cards have status placeholder; 1 implementation is verified | `chart-expert/library/CHARTS` |
| The builder is a job seeker. The value that matters is hiring evidence, not company savings | `docs/viability/_assumptions.md` |
