# decision-analytics-reconstruction: business case, written as of 2026-04-30
Persona: analyst in the campaign team of a national candidate (test case: Paraguay, election 2018-04-22). Decision owned: split a fixed budget across departments and channels, and change the split when the polls move. Cycle: one campaign, one plan at the start and one re-plan at mid-campaign. Sign-off: campaign manager.

Hours and rate from [`../viability/_assumptions.md`](../viability/_assumptions.md). Money at stake is in USD. This page treats 1 USD = 1 EUR as a labelled simplification; the verdict holds for any rate within ±50 % of parity.

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Campaign budget B | $6M | USD per campaign | Assumption, range $3M to $10M (judgement; no audited campaign spend in hand) |
| Gain if a better split pays off | 2 % of B = $120k | USD budget-equivalent reach per campaign | Assumption, range 1 to 5 % ($60k to $300k); judgement, no public benchmark in hand |
| Value if the tool only confirms the plan | 0.2 % of B = $12k | USD per campaign (doubt avoided) | Assumption, range 0 to 0.5 % ($0 to $30k); judgement |
| Loss if the tool is wrong | −1 % of B = −$60k | USD per campaign | Assumption, range −0.5 to −2.5 % (−$30k to −$150k); judgement: few public polls, synthetic voter data |

## Status quo

| Item | Value | Source |
|---|---|---|
| How the split is made | Campaign manager judgement and a spreadsheet; polls read one at a time | Assumption |
| Cost | 16 to 40 h of analyst time per campaign = €560 to €2,400 | Assumption; rate €35 to €60 per hour, `_assumptions.md` |
| How often it goes wrong | Not known | Open; the gain range above stands in for it |

## Options

| Option | Cost | Time to answer | Expected value (net of cost) | Note |
|---|---|---|---|---|
| Do nothing | €560 to €2,400 per campaign | days | 0 (baseline) | Status quo above |
| Buy or rent (campaign data consultant) | 1 to 3 % of B = $60k to $180k (assumption, no quote in hand) | 2 to 4 weeks | about −$87k (−$27k to −$147k) | Value taken as equal to build full ($33.0k before cost) |
| Build small: one allocation model (18 departments × channels, Python or spreadsheet) and a simple poll average; no synthetic voter file, no API, no governance | 60 h (40 to 80 h, judgement) × €45 = €2,700 (€1,400 to €4,800) | about 2 weeks | +€23.4k | Pays off 0.35 at 75 % of the full value; confirms 0.30; not adopted 0.20; wrong 0.15 (no uncertainty band) |
| Build full: three modules (voter segments and turnout, budget allocation, Bayesian poll tracking) plus governance | 144 h (72 to 216 h) × €45 = €6,480 (€2,520 to €12,960) | 4 weeks full time, 10 to 14 weeks part time (judgement) | +€26.5k (−€23.5k to +€126.5k) | Tree below |

## Outcome tree for "build full"

| Branch | Probability (range, source) | Value if it happens (USD per campaign, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 0.30 (0.20 to 0.40; judgement: allocation models are standard, but reach and unit costs are assumed inputs) | $120k ($60k to $300k; table above) | $36.0k |
| Confirms the status quo | 0.25 (0.15 to 0.35; judgement) | $12k ($0 to $30k) | $3.0k |
| Built but not adopted | 0.35 (0.20 to 0.50; judgement: a large build can be late for the first plan, and a manager may not trust synthetic voters) | $0 | $0 |
| Wrong, decision gets worse | 0.10 (0.05 to 0.15; judgement: few public polls, so the tracker leans on its prior) | −$60k (−$30k to −$150k) | −$6.0k |
| Sum | 1.00 | | EV before cost $33.0k (−$10.5k to +$129k) |

## Cost

| Item | Value | Source |
|---|---|---|
| Build | 144 h × €45 = €6,480 (€2,520 to €12,960) | Hours: estimate from git ±50 %. Rate: €35 to €60 per hour, anchored on `floor_analytics_eur` = €50.0k per year (vintage 2026-10-18) × 1.3 ÷ 1,700 h, `_assumptions.md` |
| Run | €0 to €500 per campaign | Assumption: laptop or free-tier hosting |
| Delay | Inside the "not adopted" branch: 0.35 for full against 0.20 for small | Judgement: full needs about 4 weeks, small about 2 weeks before the first plan |

## Result

| Measure | Value |
|---|---|
| Value of better information, full (EV with the tool − EV without) | $33.0k per campaign before cost |
| EV(build full) | +€26.5k per campaign (all-low −€23.5k to all-high +€126.5k; extremes, not an interval) |
| Payback | Inside the first campaign (about 4 months) if the "pays off" branch happens |
| Break-even probability of "pays off" | 8 % (others fixed) |
| EV(build small) | +€23.4k per campaign (value $26.1k before cost) |
| Full minus small | +€3.1k, smaller than the spread of the build cost (€2.5k to €13.0k) |

## Sensitivity

| Assumption | Central | Flips at | Effect |
|---|---|---|---|
| Campaign budget B | $6M | below about $1.2M | Build full falls below do nothing (EV before cost = 0.55 % of B against €6,480) |
| Not adopted, full | 0.35 | above 0.38 (pays off below 0.27) | Build small beats build full on EV |

## Verdict

**Build small first.** Full and small have about the same EV (+€26.5k against +€23.4k), but small answers in 2 weeks, costs 42 % as much, and keeps the option to extend. A signed commitment from the campaign manager to use the tool, plus 4 or more weeks before the first plan, would change the verdict to build full.

## Calibration against the retrospective

| Item | Finding |
|---|---|
| Retrospective verdict | sunk, freeze with summary only ([`../viability/decision-analytics-reconstruction.md`](../viability/decision-analytics-reconstruction.md)) |
| Agree? | Yes in direction. Both say the full three-module build with governance was more than the decision needed. |
| Realised result vs the forecast | Week-8 re-plan moves $766k and gives +1.20 % persuasion-weighted contacts (ILLUSTRATIVE; contacts, not dollars). At about $72k budget-equivalent (1.20 % × $6.03M, only if reach is linear in spend) it sits at the low end of the forecast "pays off" range. |
| "Wrong" branch | Real: at the low edge of the 94 % interval the shift reverses (`reports/CASE_STUDY.md`). |
| Budget | The repository uses $6M as a PRIOR envelope (`budget_envelope.yaml`), not audited spend. The forecast had the same gap. |
| Solver comparator | +54.77 % linearized contacts against a uniform plan (SIMULATED). It does not measure the gap to an expert plan, which is the status quo the forecast used. |
| What the ex-ante view missed | 1. Governance cost: about 60 % of non-merge commit subjects are governance, audit or CI. 2. Company value is not hiring value: the persona is outside the Austrian target market, and the build shows no SQL, Power BI or Azure. 3. Time: 36 commit days spread over almost 6 months, not 4 weeks. |
