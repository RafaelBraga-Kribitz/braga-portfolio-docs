# Project value evaluation — reusable prompt

Version 2.0 | 30 October 2026 | Owner: Rafael Braga-Kribitz

This is the selection step for every new BRAGA project. Run it, and commit `docs/economic-evaluation.md`
in the project repository, before the first implementation commit. The shared costing convention is in
[`value-evaluation/COST_BASIS.md`](value-evaluation/COST_BASIS.md); the portfolio results are in
[`value-evaluation/README.md`](value-evaluation/README.md); the lessons to retrieve before a build are in
[`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

The prompt below is kept verbatim.

---

Apply this prompt to the project identified in the current request and its supplied repository, documents, or proposal.

## Task and purpose

Evaluate whether the project is worth building before substantial implementation. Start from the business or personal decision, its possible gains and losses, and the cost of not knowing. Explain what this project could change, how much that change could be worth, and what building and using it would cost.

This financial evaluation is one component of a broader portfolio-selection framework. Keep market fit, company relevance, geographic preference, technical depth/breadth, and learning value separate from financial amounts.

The inspiration is an Instagram post: before building a data-science solution, simulate several possible technical results and calculate the financial outcome at each level. Extend that idea to projects without predictive models. Choose a value mechanism that fits the project; never reuse an accuracy curve or a percentage-of-budget formula merely because it worked for another example.

## 1. Establish the decision before the build

Read the relevant source material first. Identify the decision owner, beneficiary, current decision process, feasible alternatives, actionable scale, deadline, currency, and benefit horizon. Prefer EUR. Keep currencies and price dates consistent.

Ask: What money or useful capacity might be left unrealized? What could a mistaken decision cost? What changes if the vendor claim is true, partly true, or inapplicable? Would the answer actually change a decision, and can anyone act before the opportunity expires?

Use only information available at the evaluation date. For an existing project, emulate the original pre-build decision when requested. Exclude later results from the prior assumptions. Mark the exercise briefly as a pre-build scenario exercise, rather than repeatedly discussing reconstruction. Preserve genuine historical forecasts where they exist. Never present a newly constructed forecast as historical evidence.

Compare current practice with the proposed project and the best realistic alternative. A smaller study, an experiment, an existing tool, or manual analysis may answer the question more cheaply. Quantify a smaller version only when it could change the recommendation.

## 2. Connect performance to financial value

Use this chain:

Technical or operational performance → action or decision → operational consequence → incremental financial value.

Select the relevant performance variable. Simulate plausible levels, including failure or harm. If meaningful, test the claimed performance and 10%, 20%, and 30% deterioration. Explain whether deterioration concerns speed, reliability, forecast error, adoption, or something else. Recalculate the consequences; do not assume proportional financial effects.

For predictive models, apply each simulated prediction/error pattern to the actual decision rule. Measure the consequences against the baseline. Accuracy, MAPE, AUC, and other technical scores do not uniquely determine financial value. Errors differ in timing, direction, and cost. Two models with the same score can produce different profits. A technically better model may have little decision value.

For classification, use the relevant error costs, prevalence, threshold, intervention cost, and capacity constraints. For marketing interventions, predictiveness does not establish incremental customer response.

Use contribution profit rather than revenue for profit claims. Deduct variable costs through a stated margin. Identify whether marketing spend or implementation costs are already deducted. Keep cash savings, additional output valued at replacement cost, and usable capacity distinguishable. Do not count the same benefit twice.

Choose the method that fits:

| Project type | Suitable financial bridge |
|---|---|
| Procurement or technology evaluation | Lifecycle cost, throughput, availability, additional output margin, disruption, and loss from choosing the wrong option |
| MMM or budget optimization | Budget actually moved × difference in incremental revenue per euro × contribution margin, less incremental operating costs |
| Forecasting | Simulated prediction errors → inventory, staffing, procurement, or other actions → shortage, holding, service, or operating costs |
| Classification or prioritization | Decisions at a threshold → incremental benefit minus intervention and error costs |
| BI or dashboard | Useful decisions changed and usable time released; account for adoption, actionability, and decision delay |
| Data quality, pipelines, or automation | Avoidable manual effort, failure frequency, detection delay, incident loss, and operating/support costs |
| Market intelligence or career research | Better choices → avoided rework or earlier earnings; use incremental earnings over the alternative and include time spent researching |
| Reusable framework or tooling | Expected future uses × effort/error reduction per use, less maintenance; compare with existing tools |
| Portfolio or website | Useful engagement and downstream outcomes; monetize only with a defensible link, otherwise state operational value and break-even requirements |

Use multiple pathways only when they are distinct and can be added without overlap. If financial conversion is weak, report the measurable result and the missing conversion evidence. Do not manufacture a euro figure.

## 3. Simulate scenarios and calculate expected value

Keep the scenario table small, normally four or five rows. Include useful improvement, limited/no usable benefit, and adverse outcomes. Specify the baseline and horizon. Scenarios must be mutually exclusive and collectively exhaustive if probabilities are assigned.

For each scenario, calculate incremental benefit and incremental cost. State whether outcomes are conditional on adoption or already include delivery, adoption, and implementation risk. Do not multiply by another generic success probability when those risks are already included.

Estimate probabilities from comparable cases, experiments, benchmarks, or structured expert judgment. Label subjective assumptions. Do not select probabilities to achieve approval. If evidence is insufficient, use explicitly illustrative assumptions for a requested ballpark, show sensitivity, and label approval conditional. Otherwise report ranges and break-even thresholds without claiming a measured expected return.

Use the correct quantity:

- Expected gross value = Σ probability × incremental benefit before project costs.
- Expected total cost = Σ probability × total project cost in that scenario.
- Expected net value = expected gross value − expected total cost.
- Opportunity cost = value of the best feasible forgone alternative. Compare alternatives consistently; do not deduct the same forgone earnings twice.
- Decision advantage = expected net value of this option − expected net value of the best alternative.

When the project provides information, evaluate how information changes the decision. Do not credit it automatically with the entire value of the intervention studied.

- Expected value of perfect information = Σ p(s) × max over actions V(action,s) − max over actions Σ p(s) × V(action,s).
- This is the upper bound on the value of learning the uncertain state before deciding, under the specified model.
- A realistic study provides imperfect information. Estimate its expected decision improvement using plausible signals, their reliability, resulting actions, and residual error. A rough fraction of the perfect-information value is acceptable only as an explicitly assumed sensitivity parameter.

Do not calculate perfect-information value when ordinary operational cost-benefit analysis answers the question more directly. Do not use that quantity as a synonym for every project's opportunity cost.

Use discounting for material multi-year effects. Use Monte Carlo simulation only when interacting uncertainties warrant it. If used, document distributions, dependence, seed, and calculation method. A scenario table is often sufficient.

## 4. Estimate costs consistently

Use the same costing method across projects being compared. Hold the employee hourly rate and overhead conventions constant unless different staffing or expertise is justified explicitly.

Use tracked hours first. If unavailable, estimate active effort from dated repository history, work logs, milestones, and task scope. Commit counts, code volume, and calendar spans are not working-hour records. If evidence cannot support historical hours, label the estimate and use a clear task breakdown. Incorporate the user's known relative effort across projects. Never let an unsupported task estimate silently contradict it.

Show central effort plus 0.5× and 1.5× hours. These mean 50% fewer/more hours. Assign probabilities to cost scenarios only when justified; otherwise use them as sensitivity cases and call the central case central, not probability-weighted expected cost.

Find the closest appropriate role and salary evidence in Austria Data-Job Market Intelligence. Cite the source date and distinguish advertised floors from actual compensation. For one employee doing several projects, select one justified common rate for the comparison.

Loaded hourly rate = (annual gross salary + employer contributions and payroll costs) / stated productive annual hours.

Use sourced employer-cost assumptions when possible. Label placeholders. Gross salary already includes employee deductions; do not add them again. Include paid nonproductive time through the productive-hours denominator rather than charging it twice.

Total project cost includes discovery, data preparation, development, validation, documentation, deployment, implementation, and maintenance over the evaluation horizon. Include rework and failure where relevant.

Estimate AI/token cost from model, input/output token volume, retries, and rates, or label an allowance. Count subscription/API charges consistently. Include compute, hosting, data, electricity, equipment, and allocated internet costs where applicable. Separate marginal expenditure from allocated overhead. Do not charge machine runtime as employee hours without active human effort. Do not cost equivalent human effort and actual human effort twice.

For an AI-assisted build, identify whether hours represent actual employee effort or a human-equivalent delivery estimate. Keep elapsed duration separate. If uncertain, show the cost basis and its effect on approval.

Apply the same lifecycle boundary to all alternatives. Do not add implementation or maintenance to one project and omit it from another without a reason. State genuinely zero costs as zero.

## 5. Apply the 4× financial hurdle

Financial value/cost multiple = expected incremental value before project costs / total project cost on the same horizon and perspective.

The financial approval threshold is at least 4.0×. At that threshold, net ROI is 300%, because ROI = (benefit − cost) / cost. Include harmful outcomes in expected value; do not average only successful outcomes.

Show central, lower-cost, and higher-cost results. Use expected cost instead when supported probabilities exist. Do not call a central-case ratio a probability of passing. Report approval as conditional when the benefit assumptions are illustrative.

Calculate the maximum affordable cost: expected incremental value / 4. Also calculate one useful break-even driver, such as minimum margin, movable budget, adoption, useful reuses, or decision improvement. Distinguish the ordinary 1× break-even threshold from the 4× approval threshold.

Return: passes financial hurdle, fails financial hurdle, or insufficient evidence. Then recommend build, bounded pilot, smaller version, defer, or reject. A project selected for other portfolio criteria must retain its actual financial result. Do not relabel a financial failure as a pass.

## 6. Two worked patterns; adapt rather than copy

These figures demonstrate arithmetic only. They are not forecasts or approved comparisons of Rafael's projects. Re-estimate effort consistently before comparing real projects.

**A. Warehouse decision support: cost of not knowing.** Assume deployment has a 25% chance of +€400k, 30% of +€200k, 25% of −€50k, and 20% of −€350k over five years, versus waiting at €0. Expected deployment value is €77.5k. Perfect information permits deployment only in the profitable states, giving €160k. The information upper bound is therefore €82.5k. If a study is assumed to recover 30% of that decision loss, its gross information value is €24.75k. Its maximum total cost at the 4× hurdle is €6,187.50. Validate the study's ability to distinguish the states; simulation cannot by itself establish real operational compatibility.

**B. MMM: profit from changing a fixed allocation.** Assume €200k can actually move and contribution margin is 40%. A €1 increase in incremental revenue per euro moved yields €80k additional contribution profit. With scenario probabilities 20%, 35%, 20%, 15%, and 10%, and revenue-per-euro changes +€2, +€1, +€0.25, €0, and −€1, expected gross contribution gain is €56k. Maximum total cost at 4× is €14k, including implementation and lifecycle expenses. Do not subtract the unchanged media budget again. The technical test is whether the model supports profitable decisions, not whether it minimizes forecast error alone.

For career research, replace media returns with incremental earnings and avoided delay. For automation, use usable time and incident costs. For reusable tools, use realistic reuse counts. Preserve the decision logic; change the economic mechanism.

## 7. Freeze expectations, measure actuals, and learn

Before substantial implementation, preserve the dated evaluation and assumptions in version control. Define what will be measured, against which baseline, over what period, and with what evidence. Do not overwrite the original forecast after outcomes are known.

After delivery, compare original expectations with actual effort, total cost, technical performance, adoption, operational outcomes, and attributable value. Keep horizons comparable. Mark unknown results as unmeasured. Technical validation alone does not establish realized financial return.

Record project-specific lessons in `docs/lessons-learned.md`. Update the canonical shared `LESSONS_LEARNED.md` with scoped lessons, evidence, dates, and originating projects. Before future builds, retrieve that document and identify applicable lesson IDs. If no canonical location is configured or retrieval fails, report the gap briefly; do not claim automatic access by every assistant.

Keep `docs/economic-evaluation.md` as the evaluation source, or reuse an existing authoritative equivalent. Link the actuals and lessons without duplicating large reports. Respect existing repository conventions. Do not change repositories unless the user authorizes adoption or implementation.

Place "Why this project exists" near the start of `README.md` from the beginning. In 60–100 words, state the problem, intended decision/value, expected result and cost, financial-hurdle status, observed result or "Not yet measured," and a link to the evaluation. Keep original expectations visible when actuals arrive.

Preserve broader preferences separately: revenue 3×; cost/risk reduction 2×; efficiency/strategic 1×; meta 0.5×. Geographic preferences: Graz 10×; other Styria 5×; Vienna 1×; elsewhere 0.5×. These are future preference-score inputs, never multipliers of financial value. Use actual ADJMI evidence for local/company/archetype fit. Do not invent an aggregate selection score.

## Mandatory response contract

Keep the evaluation short and direct. Target 450–650 words; hard maximum 700 words, including tables. If the user asks only for a verdict or comparison, answer within 150 words. Do the full reasoning internally; show only decision-relevant assumptions and calculations. Do not create a long report or appendix unless asked.

Use this order:

1. One sentence naming the decision and value mechanism.
2. Essential scale, baseline, and horizon assumptions, with source links beside sourced facts.
3. One compact scenario table connecting performance or operational outcomes to financial value and probabilities where justified.
4. The expected-value calculation and a three-row cost-sensitivity table. State the hourly rate and cost basis once.
5. The value/cost multiple, 4× verdict, maximum affordable cost, and one or two assumptions that reverse the result.
6. A brief recommendation and what actual outcomes must be measured. Include README-ready wording only when requested or when applying the requirement to a repository.

Label sourced facts, estimates, and illustrative assumptions compactly. Round uncertain figures appropriately. Explain unfamiliar notation in one short phrase. Do not repeat disclaimers, discuss what the money is not, narrate internal instructions, or reproduce the framework in the evaluation. No invented financial precision. No forced positive conclusion. No automatic reuse of the worked numbers, probabilities, cost rates, or project rankings.
