# Shared assumptions for the viability and business-case pages (2026-10-28)

Every page in `docs/viability/` and `docs/business-case/` uses these values and cites this file.
They are assumptions until Rafael replaces them (open questions 0, 4 and 5 in the agent brief).

| Item | Value | Source and caveat |
|---|---|---|
| Hours per project | central = distinct commit days on the default branch × 4 h; range ±50 %. Label every use "estimate from git ±50 %". Commit count is a secondary proxy only; agent-assisted repositories inflate it (energy-procurement-risk-analyzer: 395 commits in 12 days). | Estimate from git, 2026-10-28. Replaced by Rafael's own log when supplied (open question 4). |
| Loaded hourly rate | €35 to €60 per hour; central €45 per hour. | Assumption. Anchor: advertised analytics floor `floor_analytics_eur` = €50.0k per year (snapshot vintage 2026-10-18) × 1.3 employer loading ÷ 1,700 h ≈ €38 per hour; the upper bound stands for a senior analyst. Open question 0. |
| Opportunity cost, applications | 2 h weekday block, 8 to 10 applications per week → about 1 to 1.25 h per application. 0 applications sent as of 2026-10-28. | `career-knowledge-core.md`, owner-stated capacity 2026-10-19 (D-035) and owner statement 2026-10-06. |
| Opportunity cost, German | 1 h of project work = 1 h of German study toward B1. Actual level A1.2; the owner expects about 2 months per sublevel at 20 h per week → about 640 h from A1.2 to the B1 exam (4 sublevels × 8 weeks × 20 h). | `career-knowledge-core.md`, owner-stated 2026-10-12 and 2026-10-19. Market evidence: B1 alone unlocks nothing measurable (6 ads name B1 as enough). |
| Opportunity cost, next project | The next scored project is B2B SaaS revenue retention (D-034, score weights profit ×3, cost/risk ×2, strategic ×1). Its size is unknown; use the median git hours estimate across the five flagships as the proxy and label it. | `career-knowledge-core.md`, D-034 (owner-approved 2026-10-19). Open question 5: show all three alternatives on every page. |
| Market shares ("ads mention") | SQL 40 %, Python 39 %, cloud 32 %, data quality 31 %, ETL 20 %, Azure 19 %, GenAI 18 %, Power BI 17 %, statistics 16 %, Excel 14 %, Tableau 3 %. German stated in 42 % of ads; 147 English-no-German ads nationally (Vienna 78, Styria 8, Graz area 6). Marketing analytics 18 ads nationally, 0 in Styria. Fully remote 2 %. Certificates ≤ 2 % each. | `career-knowledge-core.md`, snapshot vintage 2026-10-18, core n = 699. Quote as "ads mention", never "employers require". |
| Scarcity list (public GitHub pool lacks) | SQL, data quality, modelling/warehouse, Azure/Databricks, Power BI, READMEs with question → result → limitations. | Same file, GitHub supply layer. |
| Styrian employers named | KNAPP, adesso, Tieto, CANCOM, niceshops, Anton Paar, Magna, Mercedes-Benz G. | Same file. |
| Advertised floors (legal minimums) | analytics €50.0k, data science €55.4k, junior €46k per year. | Same file, vintage 2026-10-18. Never quote a floor as "salary". |
| Outcome measure | Hiring-evidence score, 0 to 2 on five items (demand match, scarcity, domain angle, interview story, finish cost), not conversions: 0 applications have been sent. Every page states this. | Agent brief §7; owner statement 2026-10-06. |
| Scenarios | S0 not built · S1 as published today (origin/<default> on 2026-10-28) · S2 after this plan (README rewritten, gate green) · S3 extended (the named next step). Total /10. One line of evidence per cell. | Agent brief §7. |
| Verdict vocabulary | Viability: worth it, keep · worth it, finish then freeze · sunk, freeze with summary only · sunk, archive and unpin. Business case: build full · build small first · buy · do nothing. | Agent brief §7 and §7b. |
| Calibrated language | "ads mention", "advertised floor", "estimate", "assumption (range)". Never "employers require/hire". Never "junior" or "transitioning" about Rafael. | `career-knowledge-core.md` standing rule. |

## Scoring rubric for the five hiring-evidence items (one scale for every page)

Each item scores 0, 1 or 2. The total is out of 10. Every page applies this table without local changes.

| Item | 0 | 1 | 2 |
|---|---|---|---|
| Demand match | shows no skill from the top of the ad list (SQL, Python, data quality, cloud, ETL, Azure, Power BI) | shows one or two of them, or shows them only in a minor part | shows several of them as the main work |
| Scarcity | nothing the public GitHub pool lacks | one item from the scarcity list | two or more items from the scarcity list, or a README with question, result and limits that the pool lacks |
| Domain angle | no marketing, customer, e-commerce or Austrian business setting | a related setting | a named setting in the target market (for example intralogistics, energy procurement, marketing mix, e-commerce) |
| Interview story | no decision owner, or no number | owner and number exist but are hard to find or hidden by codes | owner, number and caveat can be told in 2 minutes from the README |
| Finish cost | more than 10 h left | more than 2 h and up to 10 h left | 2 h or less left |

**Finish cost is the hours still needed to reach S2 from that scenario's state.** S0 (not built) scores 2 by convention: no hours are at stake. S1 scores by the hours the README rewrite and the other S2 work still need. S2 scores 2 (nothing left). S3 scores by the hours its named step adds on top of S2. State the hours and their source (git estimate, or assumption) in the cell. Where the hours are an assumption, label them.

**S1 evidence must come from the published commit** (`origin/<default>` on 2026-10-28), not from the stale local clones. Use the gate baseline in `_gate_baseline_2026-10-28.txt` (run B) and the prose measures in `_prose_measures_2026-10-28.md`.
