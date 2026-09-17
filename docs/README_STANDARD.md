# BRAGA Portfolio README Quality Standard v1.2

**Status:** Active · **Last updated:** 2026-09-17 (v1.2: banner-first identity order, portrait in the author block, readability revision of the banner generator) · **Owner:** Rafael Braga-Kribitz
**Machine-readable companion:** [`../manifest/requirements.yaml`](../manifest/requirements.yaml) (requirement ids, severities, checks, remediation)
**Gate:** `python -m readme_quality audit --repo <checkout>` · **Agent guide:** [`AGENT_GUIDE.md`](AGENT_GUIDE.md)

Every public portfolio project satisfies the same documentation contract. The project itself determines
the content.

> **Standardize the presentation and evidence architecture, not the intellectual content.**
> Same minimum quality bar, not identical READMEs.

The README is the **executive interface to the repository**, not the repository dumped into Markdown.
Anything longer than a screen of detail (methodology, governance, migration notes, long caveats) lives
in a linked document. The README stays under 450 lines.

## 0. Two layers

| Layer | What it is | How the gate treats it |
|---|---|---|
| **Minimum standard** | The `required` requirements below, filtered by project type and registry flags | `FAIL` blocks the gate |
| **Excellence layer** | `recommended` requirements and every project-specific section outside the standard vocabulary | never fails; reported as `WARN` or `PASS_WITH_EXCELLENCE` |

Existing project-specific material is preserved. Each H2 heading outside the standard vocabulary is
classified `project_specific_excellence` and kept. When the same addition proves valuable in several
repositories, it is promoted into the manifest (version bump, new check, tests, re-audit).

## 1. Project types and registry flags

Type and status are **declared** in `manifest/portfolio.yaml`; the gate never infers them from prose.

| Type | Meaning |
|---|---|
| `analytical` | Data analysis, modelling, forecasting, experimentation, decision analysis |
| `application` | Interactive application, dashboard, API, simulator with a UI |
| `library` | Installable package with a public API |
| `framework` | Governance kit, agent overlay, skill pack, methodology tooling |
| `docs` | Documentation-only or meta repository |

Flags: `interactive` (adds Tier C), `incomplete` (Foundation rules: results-bearing checks become
not-applicable, an explicit "no results yet" statement becomes required), `public_data: false`,
`estimation: none`, `demo: static` + `demo_reason`, `hosted_urls`, `hero`, `license`,
`license_blocked_reason`, `max_lines` + `max_lines_reason`.

## 2. Requirements

Ids are stable and never renamed. Severity `required` = minimum standard; `recommended` = excellence.

### Identity (first screen)

| Id | Requirement | Applies to | Severity | Auto-fix |
|---|---|---|---|---|
| `identity.h1` | Human-readable H1 at the top (no underscore slugs) | all | required | yes (registry title) |
| `identity.hero` | The **vanity banner** is the first element after the H1 (generated design-system banner by default, or a declared banner such as the warehouse hero); the badge row follows; no other image, diagram, or code block precedes the badges. The primary result chart, screenshot, or Mermaid diagram comes after the status line and problem statement | all | required | yes (banner generated; identity zone reordered) |
| `identity.badges` | Badge row: CI when a workflow exists, runtime, license (must match the LICENSE file), status | all | required | yes |
| `identity.problem` | First prose paragraph states the problem, for whom, in 12–110 words; analytical projects pose a question or name a decision; never opens with "This is a…", "Python port of…", "A reusable…" | all | required | manual |
| `identity.status_line` | `**Status:** <term>` before the first H2, equal to the registry status | all | required | yes |

Controlled status vocabulary: `Prototype` · `Foundation` · `In development` · `Functional` · `Complete` · `Maintained` · `Archived`.

### Executive answer and evidence

| Id | Requirement | Applies to | Severity | Auto-fix |
|---|---|---|---|---|
| `executive.summary` | First H2 is one of *Decision summary / Decision / Key findings / What it does / The idea / Project status* with ≥ 20 words of prose | all | required | manual |
| `evidence.primary` | analytical: a result chart or table in the first 150 lines · library: a code example · framework: architecture/workflow · application: a screenshot · incomplete: architecture + status | all | required | assisted |
| `evidence.see_it_running` | *See it running* section (screenshot, capture, or hosted link) appears before the install/reproduce section | interactive | required | manual |
| `evidence.demo_motion` | GIF or video; `NOT_APPLICABLE` with `demo: static` and a reason | interactive | recommended | manual |
| `evidence.live_demo` | Declared hosted URLs present, or a statement that none exists | interactive | recommended | manual |

Evidence hierarchy the README must respect: **source data / repository evidence → reproducible computation → generated artifact → documented interpretation → claim.** A claim never outruns its evidence; numbers come from generated artifacts (an SSOT table, a report file, a digest script) and say so.

### Navigation

| Id | Requirement | Applies to | Severity | Auto-fix |
|---|---|---|---|---|
| `navigation.audience` | *Explore this project* table with ≥ 2 rows (fast path / deep path at minimum; Recruiter / Hiring manager / Technical reviewer / Auditor for case studies), every row linking to a section or file | all | required | links only |

### Analytical (Tier B)

| Id | Requirement | Severity | Notes |
|---|---|---|---|
| `analytical.decision` | Decision, findings, or question stated | required | |
| `analytical.results` | Results / Key findings / Decision section; incomplete projects state that results do not exist | required | |
| `analytical.quantitative` | Numbers with units and a comparator in the results | required | NA when incomplete |
| `analytical.uncertainty` | Interval, percentile, coverage, or probability next to estimates | required | NA when incomplete or `estimation: none` |
| `analytical.data` | Data section naming source, period, and grain (H2 or H3) | required | |
| `analytical.epistemic` | Tags `VERIFIED` / `CALIBRATED` / `SIMULATED` / `ILLUSTRATIVE` applied, with the legend table | required | legend auto-inserted when tags exist |
| `analytical.method` | Method: input → transformation → model → validation → decision | required | |
| `analytical.validation` | Holdout, known truth, baseline, backtest, labelled audit, or acceptance/self-test named | required | also for libraries and frameworks |
| `analytical.production_data` | What changes with production data | required | NA when incomplete or `public_data: false` |

### Technical

| Id | Requirement | Applies to | Severity | Auto-fix |
|---|---|---|---|---|
| `technical.architecture` | Inline diagram: Mermaid, ASCII, or an image under *Architecture* | analytical, application, framework | required | assisted |
| `technical.structure` | Repository structure naming ≥ 3 real paths (checked on disk) | all | required | yes (names and counts only) |
| `technical.reproduce` | Reproduce / Quick start / Install with a command block; every `make`/`just` target and script referenced exists | all | required | manual |
| `technical.stack` | Stack table with reasons | all | recommended | assisted |

### Library and framework

| Id | Requirement | Applies to | Severity |
|---|---|---|---|
| `library.example` | Minimal working example that runs as pasted | library, framework | required |
| `library.contract` | What it enforces / acceptance test / gate table | library, framework | required |
| `library.api` | API or command reference with parameters | library | required |
| `library.install_pin` | Version pin in the install line or a release model | library, framework | recommended |

### Honesty

| Id | Requirement | Applies to | Severity | Auto-fix |
|---|---|---|---|---|
| `honesty.limitations` | Limitations / Known limits / Scope with ≥ 2 items | all | required | manual |
| `honesty.falsification` | At least one "reconsider if …" condition | analytical | recommended | manual |
| `honesty.placeholders` | No `TBD`, `TODO`, `Coming soon`, `{{ }}`, template markers | all | required | manual |
| `honesty.hype` | No superlatives without a number in the same sentence (state-of-the-art, production-ready, seamless, …) | all | required | manual |
| `honesty.status_section` | `## Status` with the vocabulary term and a date, version, or milestone | all | required | yes |
| `honesty.no_results_statement` | Incomplete projects say what does not exist yet | incomplete | required | manual |

### Links and metadata

| Id | Requirement | Severity | Auto-fix |
|---|---|---|---|
| `links.images` | Every relative image resolves on disk | required | unique-basename repair |
| `links.internal` | Every relative link and `#anchor` resolves | required | unique-basename repair |
| `meta.license_file` | LICENSE file present (see [`LICENSE_POLICY.md`](LICENSE_POLICY.md)); `BLOCKED_HUMAN` when ownership is unclear | required | policy-driven |
| `meta.license_section` | `## License` names the same license as the file, or states truthfully that none exists | required | yes |
| `meta.author` | Canonical author block with the portrait ([`../blocks/author.md`](../blocks/author.md); `docs/assets/Author_MDS_Rafael_Braga-Kribitz_kroped.png` vendored from `blocks/assets/`) | required | yes |
| `meta.length` | ≤ 450 lines (`max_lines` override needs a reason) | required | manual |

### Excellence (never required)

`excellence.audience_personas` (four-persona table) · `excellence.claim_tracing` (`<!-- claim: -->`
comments, an SSOT reference, or a digest script) · `excellence.why` (*Why this project* / *What
surprised me*) · `excellence.project_specific` (sections outside the standard vocabulary, always kept).

## 3. Visual identity system

Every project has the same visual **slots**, not the same image. The hero uses the Braga-Kribitz
design system: surface `#E6E6E6`, ink `#282828`, Söhne 800 display / Söhne Mono labels, one orange
`#FA6400` element (the status dot), 1 px hairlines, 8 px grid, no photography, gradients, or decoration.
`readme_quality/hero.py` generates a banner from registry and repository facts only, with layout
guardrails (wrap-and-shrink, line-length caps, no overlap, safe area, per-glyph font coverage, contrast
≥ 4.5, post-render pixel scan).

| Slot | Requirement | Acceptable evidence |
|---|---|---|
| Vanity banner | always, first | generated design-system banner (`readme_quality/hero.py`) or a declared banner image |
| Most-important-data visual | analytical, library, application | primary result chart, rendered library output, interface screenshot; placed after badges and status |
| Primary result | analytical | chart or table |
| Interface | interactive | screenshot before installation |
| Motion | interactive, recommended | GIF ≤ 30 s or video; `demo: static` with a reason when motion adds nothing |
| Architecture | analytical, application, framework | Mermaid, ASCII, or image |
| Supporting charts | where they carry evidence | with tag and source |

Demonstration slot by project kind: interactive application → GIF / video / screenshots · dashboard →
screenshot / video / live link · CLI → terminal capture or example output · library → runnable example
and rendered output · analytical → primary visualization, report, dashboard · framework → architecture,
workflow, runnable example.

## 4. Standardized order

Omit a section when genuinely irrelevant; never fill it with boilerplate.

```text
# PROJECT NAME
[VANITY BANNER]                  always first: generated design-system banner or a declared banner
[BADGES]
**Status:** …
Problem statement (≤ 2 sentences)
[PRIMARY CHART / SCREENSHOT / MERMAID]   the most-important-data visual, after the identity block
## Decision summary | What it does | The idea | Project status
## See it running                 (interactive)
## Explore this project
## Results                        (analytical)
## Method                         (analytical)   | ## Quick start / Minimal example (library)
## Data + tag legend              (analytical)   | ## What it enforces               (library, framework)
## Validation
## Architecture
## Reproduce / Install
## Limitations
## What I would do with production data   (analytical on public or synthetic data)
## Repository structure
## Stack                          (recommended)
## Status
## License
## Author
```

## 5. Reusable blocks

[`../blocks/`](../blocks/): `author.md`, `license.md`, `license-none.md`, `status.md`, `structure.md`,
`epistemic-legend.md`, `audience.md`, `audience-tool.md`, `reproduce.md`, `limitations.md`,
`production-data.md`, `provenance.md`, `badges.md`, and canonical license texts under `licenses/`.
Blocks use `$variable` placeholders filled from the registry or repository facts; none contains a claim.

## 6. Versioning

`manifest/requirements.yaml` carries the version. Adding, removing, or changing a check bumps it.
Retired ids stay in the file with `retired: true`. Every version change re-audits the portfolio.

## 7. Out of scope

Private repositories. Prose quality beyond the structural and honesty checks. Automatic generation of
results, methods, or limitations prose (an agent writes those from repository evidence; see the agent
guide).
