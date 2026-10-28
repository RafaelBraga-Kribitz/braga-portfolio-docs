# funnel_correlation_py: business case, written as of 2026-02-18

Persona: marketing analyst at a mid-size Austrian e-commerce or retail company (assumption). The team works in Python; R is not on the approved tool list (assumption). Decision owned: which customer traits to investigate first, before modelling a campaign or churn outcome. Cycle: about 12 per year for the team (4 to 24; assumption). Sign-off: head of marketing or CRM lead.

Forecast written before the first commit. All euro values are assumptions unless a source is named. Rate and rules: `docs/viability/_assumptions.md`. The repository has no euro figures for this project (a library has none).

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Hand screening of 15 to 20 features | 4 (2 to 8) | h per cycle | assumption, judgement (10 to 15 min per feature) |
| Screening with the tool | 1 (0.5 to 2) | h per cycle | assumption, judgement |
| Hours saved | 3 (1 to 6) | h per cycle | derived |
| Loaded hourly rate | 45 (35 to 60) | EUR per h | `_assumptions.md`; anchor is the advertised analytics floor, used here only as a rate |
| Value of saved hours | 135 (35 to 360) | EUR per cycle | 3 h × €45 |
| Rework avoided when a missed driver is caught | 72 (14 to 480) | EUR per cycle | 10 % (5 to 20 %) of cycles × 16 h (8 to 40) × €45; judgement |
| Cycles per year | 12 (4 to 24) | cycles per year | assumption |
| **Money at stake** | **2,484 (about 200 to 20,200)** | EUR per year | (€135 + €72) × 12 |

## Status quo

The analyst cross-tabulates features one by one and charts a few. Cost: about 4 h per cycle (€180). It goes wrong when the traits that are easy to see get checked first and a stronger driver is missed: assumption 1 cycle in 10 (5 to 20 %), judgement, no public benchmark. The R package `correlationfunnel` (Business Science, public) already does this screen, but not in the team's Python stack.

## Options

EV = expected net value over 3 years (horizon 1 to 5 years, judgement), after cost, in EUR. Ranges change one assumption at a time.

| Option | Cost | Time to answer | Expected value | Note |
|---|---|---|---|---|
| Do nothing | €0 | 4 h per cycle | €0 | baseline |
| Buy or rent: an existing Python profiling package, or R | €180 (4 h set-up) | 2 h per cycle if it fits | €1.1k (€0.5k to €1.8k for fit probability 20 to 60 %) | fit probability 40 %, judgement: R needs an install; Python packages cover correlation, not the binarize-then-rank flow |
| Build small: 2-week scope, binarize and correlate in one module, one static plot, one notebook | €630 (8 h build, 2 h per year upkeep, 3 years) | 1 h per cycle | €1.4k (−€0.1k at 4 cycles per year; €3.6k at 24) | 80 % of the full tool's value; branch odds 30 / 25 / 30 / 15 % (assumption) |
| Build full: installable package, tests, interactive plot, example loaders | €1,620 (24 h build, 4 h per year upkeep) | 1 h per cycle | €1.4k (−€0.7k at 4 cycles per year; €4.6k at 24) | build hours = git estimate 6 days × 4 h, as in the retrospective |

## Outcome tree for "build full"

Basis for every probability: judgement. There is no repository evidence before the first commit and no public benchmark was found. Values are 3-year totals.

| Branch | Probability (range) | Value if it happens (EUR) | Probability × value (EUR) |
|---|---|---|---|
| Changes the decision and pays off (used in most cycles) | 35 % (20 to 50 %) | +7,452 = (3 h + 1.6 h) × €45 × 12 × 3 | +2,608 |
| Confirms the status quo (hours saved only) | 25 % (15 to 35 %) | +2,430 = 1.5 h × €45 × 12 × 3 | +608 |
| Built but not adopted | 30 % (10 to 45 %) | 0 | 0 |
| Wrong; decision gets worse (association read as cause, or a driver known only after the outcome) | 10 % (5 to 20 %) | −1,800 = 40 h rework × €45 (20 to 120 h) | −180 |
| **Sum** | 100 % | | **+3,036 (EV before cost)** |

## Cost

| Item | Value | Basis |
|---|---|---|
| Build | 24 h (12 to 36) × €45 = €1,080 (€420 to €2,160) | estimate from git ±50 %; rate range €35 to €60 (`_assumptions.md`) |
| Run | 4 h per year (2 to 8) × €45 = €180 per year; €540 over 3 years | assumption: dependency updates, new column types |
| Delay | €0 | assumption: no deadline; the analyst keeps screening by hand meanwhile |
| **Total, 3 years** | **€1,620** | |

## Result

| Measure | Build full | Build small |
|---|---|---|
| EV | €3,036 − €1,620 = **+€1.4k** (−€0.7k to +€5.0k, one assumption at a time) | €2,004 − €630 = **+€1.4k** |
| Payback | about 13 months (build cost ÷ expected gross benefit of €1,012 per year) | about 6.5 months |
| Break-even probability of "pays off" | 16 % (other branches fixed) | not computed |
| Value of better information (EV with tool − EV without, before cost) | €3,036 | €2,004 |

## Sensitivity

| Assumption | Flips at | Effect |
|---|---|---|
| Cycles per year | below 7 for full (below 5 for small); above 11.5 full beats small | the tool needs a repeated decision |
| Hours saved per cycle | below 1.2 h the full build loses | the case rests on analyst time, not on better decisions |
| Fit probability of an existing package | 48 % | above this, buy beats build small |

## Verdict

**Build small first.** Full and small have the same EV (€1.4k) but small costs 39 % of the money and loses less when use is rare. Before building, spend 2 h to test existing Python packages and the R package; if one fits, buy. Evidence that would change it: 12 or more cycles per year with a named analyst who asks for the plot and the tests, then build full.

## Calibration against the retrospective

Retrospective verdict (`docs/viability/funnel_correlation_py.md`): sunk, freeze with summary only. Agree? **Mostly.** Both reject the full build as a use of hours. The ex-ante view said "build small"; the retrospective says "stop and summarise".

What the ex-ante view missed:

| Missed | Evidence |
|---|---|
| No persona exists. The repository has no user, no decision owner and no use. The benefit stream "analyst hours" never occurred; the only possible payoff is hiring evidence. | 0 applications sent; the retrospective scores S1 at 5/10 and S2 at 6/10 |
| Ads mention tools, not libraries. | Python 39 %, pandas 3 %, R 7 % (snapshot 2026-10-18) |
| Most of the hours went to polish, not to the library. | 5 of 6 commit days are README, gate and design work |
| The "wrong decision" branch is real in the demo. The top driver of the demo target may be known only after the outcome. | Open question 4 in the retrospective |
| The existing R package is the free alternative; the ex-ante "buy" branch should have been tested first. | Open question 3 in the retrospective |
