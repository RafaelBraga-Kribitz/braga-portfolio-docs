# NextMove: business case, written as of 2026-07-17

Persona: CRM manager at an Austrian mid-market online retailer (fashion and home). Decision owned: which customer gets which contact each week (email now or later, recommendation, bundle, discount tier, or nothing), and the yearly discount ceiling. Cycle: weekly run, yearly policy review. Sign-off: head of e-commerce; finance for the discount budget.

Forecast from before the first commit. Every figure is an assumption with a range unless a source is named. EUR, no discounting. Hourly rate: `docs/viability/_assumptions.md`. The 3-year horizon is an assumption (range 2 to 4).

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Online revenue | 40 (10 to 100) | EUR million per year | Assumption, judgement: mid-market, one company |
| Share of revenue influenced by CRM contacts | 25 % (15 to 35) | share | Assumption, judgement |
| Discount cost on those orders | 6 % (3 to 10) | share of CRM revenue | Assumption, judgement |
| Discount spend | 0.6 (0.05 to 3.5) | EUR million per year; about 11.5k per weekly run | Computed from the three rows above |
| Share given to customers who would have bought anyway | 50 % (30 to 70) | share of discount spend | Assumption, judgement. `docs/PROJECT_VISION.md` states over-discounting as a pain point with no rate. |
| Recoverable ceiling | 0.3 | EUR million per year | 0.6 × 50 % |
| Share a tool captures: full 30 % (10 to 50), small 20 % (10 to 30), buy 15 % (5 to 25) | full 90k, small 60k, buy 45k | EUR per year gross | Assumption, judgement. Upper evidence: +27.56 % conversion and +68.09 % order value in one customer cluster (Wasilewski and Ramsey 2025, IEEE Access, as cited in `docs/RESEARCH_SYNTHESIS.md`). That is a UI test, not discount allocation, in one cluster. |
| Not valued | contact fatigue, unsubscribes, brand trust | – | Excluded: no basis for a number |

## Status quo

The CRM manager sets the send calendar and flat discount tiers in the email tool. Success is read from last-click attribution. A holdout test is rare. Cost: the leakage above plus about 0.2 analyst FTE (assumption). Frequency of error: unknown; 30 to 70 % of discount spend is the assumed range. Source: assumption.

## Options

| Option | Cost | Time to answer | Expected value (net, 3 years) | Note |
|---|---|---|---|---|
| Do nothing | €0 | now | €0 | Leakage continues |
| Buy or rent (email or CDP add-on) | €1.8k setup (40 h) + €25k per year licence (10 to 40, assumption, no quote) | 4 to 8 weeks | +€13.5k | Vendor tools optimise opens and clicks, not incremental profit; captures 15 % |
| Build small: 2-week readout. Take 12 months of campaign and order logs. Run a randomised holdout (4 weeks if none exists). Measure redeemed discounts by customers who bought anyway, by propensity decile. Change one rule: suppress discounts for the top decile. | 80 h × €45 = €3.6k + €0.5k per year run = €5.1k | 2 to 6 weeks | +€78.4k | Captures 20 % |
| Build full: the charter (nine pipeline stages, models, decision engine, explanations, API, three-way experiment gateway, bandit as stretch) | 320 h (160 to 640, judgement) × €45 = €14.4k + run + delay (see Cost) = €34.0k | 10 to 14 weeks | +€44.0k | Captures 30 % |

## Outcome tree for "build full"

| Branch | Probability (range, source) | Value if it happens (EUR, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 30 % (15 to 45); judgement; the field result above is an upper bound from one cluster | +270k = 3 years × 90k | +81.0k |
| Confirms the status quo | 25 % (15 to 35); judgement | +15k one-off, avoided doubt (0 to 30k) | +3.75k |
| Built but not adopted | 30 % (20 to 45); judgement: small team, new tool, discount ceiling needs finance sign-off | 0 | 0 |
| Wrong, decision gets worse | 15 % (5 to 25); judgement: weak signal in real behaviour data, miscalibrated suppression | −45k = half of one year's gross value (−20k to −120k) | −6.75k |
| Sum | 100 % | | EV before cost +78.0k |

## Cost

| Item | Value | Basis |
|---|---|---|
| Build | 320 h × €45 per hour = €14.4k (range €5.6k to €38.4k) | Hours: judgement. Rate: €35 to €60, central €45 (`_assumptions.md`; its anchor is the 2026-10-18 snapshot, used here only as a rate). |
| Run | €3.4k per year × 3 = €10.3k | 10 % of build + €2k hosting, assumption |
| Delay | €9.2k | 8 more weeks than "build small" × €60k per year ÷ 52 |
| Total | €34.0k | |

## Result

* EV(build full) = 78.0k − 34.0k = **+€44.0k** over 3 years. Range: −€4.7k (online revenue €10M) to +€141.6k (€100M); +€3.5k to +€84.5k for a pays-off probability of 15 % to 45 %.
* Payback: about 1.05 years (build + delay ÷ expected net value per year).
* Break-even probability of "pays off": 13.7 % (other branches fixed).
* EV(build small) = +€78.4k (gross 83.5k − cost 5.1k); positive down to about €1.3M online revenue. At €10M it is still +€17.7k.
* Value of better information: EV with a tool minus EV without = 78.0k gross for full (83.5k for small); the baseline is €0.
* EV(buy) = +€13.5k.

## Sensitivity

| Assumption | Flips "build full" at | Note |
|---|---|---|
| Online revenue | about €16M (central 40M) | Below this, full costs more than it recovers |
| Wasted share of discount spend | about 20 % (central 50 %) | Below this, full has a negative EV; small stays positive down to about 2 % |
| Capture of "small" vs "full" (20 % vs 30 %) | if small captures under about 12 %, full wins | Judgement; the weakest link |

## Verdict

**Build small first.** The two-week readout answers the question the full engine would answer, for about 15 % of the cost, and it is positive even at €10M online revenue. Evidence that would change it: a holdout showing the wasted share above 60 % with a large gap between rule-based and model-based suppression; then build full.

## Calibration against the retrospective

Retrospective verdict (`docs/viability/NextMove.md`): worth it, finish then freeze. Agree? Partly. Both views say do not extend. They answer different questions: the business case asks if a company should build; the retrospective asks if the portfolio gains.

What the ex-ante view missed:

| Item | Ex-ante forecast | Known on 2026-10-28 |
|---|---|---|
| Customer | CRM manager at a retailer | `.planning/PROJECT.md` names a hiring manager as the customer and "none" as the revenue model. No company case existed. |
| Hours | 320 h (160 to 640) | About 48 h (24 to 72), estimate from git ±50 %. Different scope: ADR-011 cut the charter on 2026-10-14; simulation only, no real data integration; agent-assisted. |
| "Small gets most of the value" | 20 % vs 30 % capture | In the simulation: the oracle ceiling is +€44 over doing nothing, the engine ties do-nothing (€0), and 92 % of redeemed discounts in "always discount" are wasted. This supports the small readout. The simulator author set the response functions, so the support is weak. |
| Hiring value | not in scope | Ads mention SQL 40 %, Python 39 %, data quality 31 %, ETL 20 %; marketing analytics 18 ads nationally, 0 in Styria (snapshot 2026-10-18). The portfolio gain does not depend on company EV. |
