# Metric Driver-Tree Studio: business case, written as of 2026-05-31
Persona: growth or experimentation lead at a mid-size DACH online retailer (direct to consumer). Decision owned: which hypothesis the team tests first in the quarterly test roadmap. Cycle: quarterly (4 per year, assumption). Sign-off: head of e-commerce or CMO.

Shared values (hourly rate, hours rule) come from [`../viability/_assumptions.md`](../viability/_assumptions.md). Every probability below is an assumption with a range. The tool produces information, so the value is the value of better information per year: EV with the tool minus EV without it.

## Money at stake per decision cycle

| Item | Value (range) | Unit | Source |
|---|---|---|---|
| Annual contribution profit of the shop, S | 1.0 M (0.5 to 5 M) | EUR per year | Assumption (judgement). Low end is near the day-0 seed baseline of 48,000 per period × 12 = 0.58 M if one period is one month. The seed is ILLUSTRATIVE, units "currency". |
| Uplift of the best untested lever, u | 3 % (1 to 5 %) of S | share per year | Assumption (judgement). Cross-check: a public study (Deloitte Digital for Google, *Milliseconds Make Millions*, 2020) associates 0.1 s faster mobile pages with higher retail conversion. It is observational and multi-brand, so 5 % is not extreme. |
| Months saved when the best lever is tested first, d | 2 (1 to 3) | months | Assumption (judgement): one to three test slots |
| Value of one correct re-ordering | 5,000 (417 to 62,500) | EUR per cycle | = S × u × d ÷ 12 |
| Team time on today's prioritisation debate | 8 h (4 to 12 h) × EUR 45 = 360 | EUR per cycle | Assumption; rate from `_assumptions.md` |
| Cycles per year | 4 | cycles | Assumption |

## Status quo

The team scores ideas with a spreadsheet (ICE or PIE scoring) or by opinion. Cost: about 8 h per cycle (assumption). Failure: the best lever is not tested first in 50 to 70 % of cycles (assumption, judgement; no public figure used). The score uses guessed numbers and hides how uncertain each guess is.

## Options

| Option | Cost | Time to answer | Expected value | Note |
|---|---|---|---|---|
| Do nothing | EUR 0 | 0 | EUR 0 per year (reference) | Status quo continues |
| Buy or rent | Licence EUR 2,000 to 15,000 per year (assumption; vendor prices not checked) | Days | At most EUR 3,504 gross per year, so net at most +1,504 at a EUR 2,000 licence, zero at EUR 3,504 and negative above that; below build small (net 2,784) at every licence in the range | Platform scoring ranks by score, not by declared uncertainty range (assumption, not verified) |
| Build small: spreadsheet with the driver tree, 3 guessed ranges, simulation | 12 h (8 to 16) × EUR 45 = 540, plus run 180 per year = **EUR 720** | 2 weeks | Gross 3,504; **net 2,784 per year** | Analyst owns it, so adoption risk is lower (p not adopted 0.35, p pays off 0.20) |
| Build full: the studio as scoped (6 phases, app, data test, exports) | 24 h (12 to 36) × EUR 45 = 1,080, plus run 360 per year = **EUR 1,440** | 8 to 12 weeks (judgement) | Gross 4,432; **net 2,992 per year** | See the tree below |

## Outcome tree for "build full"

Values are EUR over the first 12 months (4 cycles).

| Branch | Probability (range, source) | Value if it happens (EUR, source) | Probability × value |
|---|---|---|---|
| Changes the decision and pays off | 0.25 (0.10 to 0.40). Judgement: 0.65 adopted × 0.55 order changes × 0.7 new order is better | 20,000 (1,667 to 250,000) = 4 × 5,000 | 5,000 |
| Confirms the status quo | 0.30 (0.20 to 0.45). Judgement: 0.65 adopted × 0.45 order unchanged | 1,440 (720 to 2,160) = 4 cycles × 8 h × EUR 45 of debate time avoided | 432 |
| Built but not adopted | 0.35 (0.20 to 0.50). Judgement: single-user tool, no link to the shop's data stack, an analyst must author the ranges | 0 (cost stays) | 0 |
| Wrong, decision gets worse | 0.10 (0.05 to 0.20). Judgement: a value-of-information ranking follows the width of the declared ranges, so a wide guess ranks high whether or not it is right | −10,000 (−833 to −125,000) = two wrong re-orderings of 5,000 | −1,000 |
| Sum | 1.00 | | **EV before cost = 4,432 per year** |

## Cost

| Item | Value | Source |
|---|---|---|
| Build | 24 h × EUR 45 = **EUR 1,080** (EUR 420 to 2,160) | Hours: estimate from git ±50 % (12 to 36 h), `_assumptions.md`. Rate EUR 35 to 60 per hour, central 45: anchored on the advertised analytics floor EUR 50.0k per year × 1.3 ÷ 1,700 h ≈ EUR 38 per hour (snapshot vintage 2026-10-18). |
| Run | 8 h per year × EUR 45 = EUR 360 | Assumption; static app, no hosting fee |
| Delay | EUR 0 | The team keeps today's process while the tool is built (assumption) |
| Year 1 total | **EUR 1,440** (EUR 700 to 2,640) | If the real effort is the 48 h seen on all branches: EUR 2,520 |

## Result

| Measure | Value |
|---|---|
| EV(build full), year 1 | 4,432 − 1,440 = **EUR 2,992** (central); pessimistic set −2,496; optimistic set +87,448. Each set moves all inputs together. |
| Payback | 1,440 ÷ 4,432 × 12 ≈ 3.9 months |
| Break-even probability of "pays off" | 0.10, the low end of its range |
| EV(build small), year 1 | 3,504 − 720 = **EUR 2,784** (93 % of build full at 50 % of the cost) |
| Value of better information | EUR 4,432 gross per year (EV with the tool minus EV with today's process) |
| If effort is 48 h | EV(build full) = 4,432 − 2,520 = EUR 1,912 |

## Sensitivity

| Assumption | Flips the verdict at |
|---|---|
| Size of the prize, S × u × d | Build full beats build small only if S × u × d ≥ EUR 47,520 per year. At u = 3 % and d = 2 months this means S ≥ EUR 0.79 M. Below it, build small wins. Do nothing wins only if S × u × d < EUR 4,320 (S < EUR 72k). |
| Adoption gain of full over small | Build full needs a 4-point higher chance of "pays off" than build small (0.25 against 0.20). The central gap is 5 points. |

## Verdict

**Build small first.** A spreadsheet captures about 93 % of the net value for half the cost and tests adoption (35 % not adopted) before the larger spend. Evidence that would change it: a named shop with S above EUR 0.8 M and a growth lead who commits to author the ranges, or a past cycle where the wrong test went first and cost money.

## Calibration against the retrospective

| Item | Finding |
|---|---|
| Retrospective verdict (`../viability/metric_lineage_simulator.md`) | Worth it, finish then freeze. Hiring evidence 7 now, 9 after the README rewrite. About 24 h (estimate from git ±50 %). |
| Agree? | Partly. Both stop before "extend". The ex-ante view says build small. The project was built full, and the retrospective accepts that because it scores hiring evidence, not company value. |
| What the ex-ante view missed | 1. Portfolio value: the SQL and Power BI export (added 2026-10-14) and the online-shop domain add hiring evidence that has no company EV. 2. No real decider or data existed, so adoption was in practice 0 and the launch rule blocks a public demo. 3. Agent-assisted building cut the hours. 4. Governance overhead (22 findings, 10 decision records) sits outside the hours. |
| Persona check | The planner's prior was a BI or data-quality lead (where a wrong KPI comes from). The repository ranks which guess to test, so the persona is an experimentation lead. This fits the 20-year marketing and experimentation background and the online-shop angle (marketing analytics: 18 ads nationally, 0 in Styria, snapshot 2026-10-18). |
