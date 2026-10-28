# Brazil 2026 Election Forecast: business case, written as of 2026-09-22

Persona: data editor at a newsroom that publishes poll-based election probabilities (assumption; the repository names no persona). Decision owned: which poll aggregate to publish and how to word its uncertainty. Cycle: once per election (Brazilian presidential cycle, every 4 years; two rounds). Sign-off: editor-in-chief (assumption).

**Persona test for the Austrian target market: fail.** The target market is applied Data Scientist and Data Analyst roles, marketing/customer/e-commerce angle, Graz and Vienna (`career-knowledge-full.md` §5). No media or polling employer appears in that definition. A Brazilian election forecast is not a decision an Austrian target employer owns. This is a verdict in itself. The numbers below give the newsroom lens and the Austrian-employer lens. Shared values: `docs/viability/_assumptions.md`.

Scope as planned: pre-registered Bayesian poll aggregation, backtest on the 2014, 2018 and 2022 elections, forecast frozen before the first round (2026-10-04; freeze 2026-10-03), runoff on 2026-10-25.

## Money at stake per decision cycle

| Item | Value | Unit | Source |
|---|---|---|---|
| Value of a calibrated forecast feature against a free aggregate, one outlet | 30,000 (10,000 to 100,000) | EUR per election | Assumption. No benchmark found; judgement. |
| Value of avoided doubt (tool confirms the aggregate) | 3,000 (1,000 to 8,000) | EUR per election | Assumption. |
| Cost of a confidently wrong published call (correction, trust) | -25,000 (-10,000 to -80,000) | EUR per election | Assumption. |
| Buying an outside forecast | 0 to 5,000 | EUR per election | Judgement, no quote. |
| Probability q that an Austrian target employer owns such a decision | 2 % (0 to 5 %) | probability | Judgement from the target-market definition above. |
| Build cost | 720 (280 to 1,440) | EUR once | 16 h (8 to 24 h) estimate from git ±50 %, taken from the retrospective because no earlier hours estimate exists; €45 per hour (€35 to €60). |

## Status quo

The newsroom uses a public poll aggregate or the latest polls, plus prediction-market prices. Cost: about 0 EUR in licences, some analyst hours. How often it goes wrong: assumption, the "who leads" call fails in 10 to 20 % of elections, mostly in close races (judgement, no citation).

## Options

Newsroom lens, EUR per election. Expected value (EV) = net of cost.

| Option | Cost | Time to answer | Expected value | Note |
|---|---|---|---|---|
| Do nothing | 0 | 0 | 0 (reference) | Public aggregate stays the answer. |
| Buy or rent | 0 to 5,000 | 1 week | about 0 (-3,350 to +1,650) | Gross 1,650 = "confirms" branch only (0.55 × 3,000); no tailoring. |
| Build small: 14-day latest-poll average per pollster, error band from the last 3 elections, spreadsheet, no sampler, 2 weeks | 270 (105 to 540) for 6 h (3 to 9 h, assumption) | 2 weeks | +2,330 | Gross 2,600 with p(pays) 0.06, p(confirms) 0.60, p(wrong) 0.04. |
| Build full (the project as scoped) | 720 (280 to 1,440) | 11 days to the freeze; hard stop 2026-10-04 | +2,680 (stress corners -12,540 to +25,120) | Tight against the deadline. |

## Outcome tree for "build full"

| Branch | Probability (range, source) | Value if it happens (EUR per election, source) | Probability x value |
|---|---|---|---|
| Changes the decision and pays off | 0.10 (0.05 to 0.20); judgement: an aggregate seldom changes the headline call outside close races | 30,000 (10,000 to 100,000); assumption | 3,000 |
| Confirms the status quo | 0.55 (0.40 to 0.70); judgement | 3,000 (1,000 to 8,000); assumption | 1,650 |
| Built but not adopted | 0.30 (0.08 to 0.40); judgement: a hard external deadline gives schedule risk | 0 | 0 |
| Wrong, decision gets worse | 0.05 (0.02 to 0.15); judgement: a short backtest (3 elections) supports weak calibration claims | -25,000 (-10,000 to -80,000); assumption | -1,250 |
| Sum | 1.00 | | **3,400** (EV before cost; corners -11,100 to +25,400) |

Stress corners combine the extreme of every range in one direction. They are not a confidence interval.

## Cost

| Item | Value | Basis |
|---|---|---|
| Build | 16 h × €45 = €720 (€280 to €1,440) | `_assumptions.md` |
| Run, per year | about 1 h per week during the campaign (€45 per week), 0 after 2026-10-25 | Assumption |
| Delay | If the tool is not frozen by 2026-10-03, its value for this election is 0. The next cycle is 2030. | Public election calendar |

## Result

| Measure | Newsroom lens | Austrian-employer lens (q = 2 %) |
|---|---|---|
| Value of better information (EV with tool minus EV without, before cost) | +3,400 EUR per election | +68 EUR per election (q × 3,400) |
| EV(build full) | **+2,680 EUR** (-12,540 to +25,120) | **-652 EUR** (-720 to -550 for q 0 to 5 %) |
| EV(build small) | +2,330 EUR | -218 EUR |
| Payback | 0.21 of one election, so inside the first cycle | 10.6 cycles, about 42 years at one cycle per 4 years |
| Break-even for "pays off" | p = 1.1 % (taken from the "not adopted" branch) | q = 21 % for full, 10 % for small |

## Sensitivity

| Assumption | Flips the verdict at | Range used |
|---|---|---|
| q, that an Austrian target employer owns the decision | q ≥ 21 % (full) or 10 % (small): "do nothing" becomes "build" | 0 to 5 % |
| p(wrong), newsroom lens | EV(full) below 0 when p(wrong) > 15.7 % | 2 to 15 % |
| Hours | At 60 h (flagship proxy), newsroom EV(full) is still +700; the Austrian lens never turns positive | 8 to 24 h |

## Verdict

**Do nothing** as a project for an Austrian target employer. The persona and its decision sit outside the target market (q about 2 %, break-even 21 %), so the cost has no business buyer. A named Austrian employer or ad family that owns a poll or forecast decision, taking q above 21 %, would change this to "build small first".

## Calibration against the retrospective

Retrospective verdict (`docs/viability/brazil_presidential_election_prediction_2026.md`): sunk, freeze with summary only; S1 5/10, S2 5/10. Agree: yes. Both say the employer value is close to zero.

What the ex-ante view missed:

| Missed | Evidence |
|---|---|
| Schedule risk happened | The registered freezes (2026-10-03, 2026-10-24) did not take place; the registered scorecard cannot run. This matches the "built but not adopted" branch (0.30). |
| Personal evidence has a value the employer lens cannot see | The repository is the only public evidence for forecasting and Bayesian work (`career-knowledge-full.md` §1). The retrospective scores it 5 of 10 on hiring evidence (S1 and S2). |
| The tree priced the wrong output | Backtest share error was lower than the 14-day average (1.38 vs 2.07 pp) but first-place Brier was worse (0.075 vs 0.034). In 2026, first place was called wrong (36 %) and the baseline pointed the same way. Branch 1 (changes the call) was probably too likely; shares, not calls, were the product. |
| No euro figure was ever produced | The README holds no euro value and names no decision owner (gate warning). The money at stake stayed an assumption. |
