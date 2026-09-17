# BRAGA Portfolio Project README Standard v1.0

**Status:** Active
**Last updated:** 2026-09-16
**Owner:** Rafael Braga-Kribitz

Every public portfolio project has the same documentation contract. The project itself determines the content.

> **Standardize the presentation and evidence architecture, not the intellectual content.**

An MMM project and a charting library both have a Decision / Result slot. They must not have the same kind of result. Sections that are genuinely irrelevant are omitted, not filled with boilerplate.

The README is the **executive interface to the repository**. It is not a dump of the repository into Markdown.

```text
README
   │
   ├── Executive explanation
   ├── Primary evidence
   ├── Key results
   └── Links
        │
        ├── Architecture
        ├── Methodology
        ├── Data provenance
        ├── Validation
        ├── Governance
        └── Detailed reports
```

This document is the human-readable contract. The machine-checkable companion is [`tools/readme_audit.py`](../tools/readme_audit.py), driven by [`tools/portfolio.yaml`](../tools/portfolio.yaml). Project type is declared in that registry. The checker never infers type from folder names or README prose.

---

## 1. Identity

Every project starts with:

```text
# Project Name
[Hero visual]
```

### Required

- Clear project name as the H1.
- One visual identity element in the identity zone (before the first H2):
  - hero banner, or
  - project screenshot, or
  - primary visualization, or
  - for a library, a rendered example plot, or
  - a Mermaid (or equivalent) architecture / workflow diagram when no chart or screenshot exists yet.

**Every serious portfolio project gets a hero visual.** The visual does not have to be decorative. For analytical projects, a strong primary chart can be the hero. Reuse an existing chart, screenshot, or example plot. Do not manufacture decorative banners. Do not add a fake GIF to a library because an application has one.

---

## 2. Status / metadata

Immediately below the identity:

```text
[CI] [Reproducibility] [Python] [License] ...
Status: Active | Foundation | Complete | ...
```

### Required information

- Project status, using the controlled vocabulary in §19.
- Technology / runtime where relevant.
- License.
- CI status where a workflow exists.
- Reproducibility status where a reproducibility workflow exists.

A project must never make a visitor guess whether something is implemented, planned, simulated, or aspirational.

---

## 3. One-line business / problem explanation

**Mandatory.** Maximum approximately two sentences. Answers:

> **What problem does this project solve, for whom, and why does it matter?**

No project begins with "This is a Python project that…" or "This repository contains…". Start with the problem.

---

## 4. Executive answer / result

The visitor must know what they are looking at within the first screenful.

| Project type | Heading | Content |
| --- | --- | --- |
| Analytical | `Decision summary` or `Decision` | What the analysis found |
| Library / tool | `What it does` | Concrete capability |
| Framework | `The idea` | Core mechanism |
| Unfinished / foundation | `Project status` | What exists / what does not |

These headings are **aliases** of one slot. A project needs one of them, not all of them.

---

## 5. Primary evidence

Every project needs one piece of immediate evidence. No project should ask the reader to finish the README before showing that the project exists.

| Project type | Primary evidence |
| --- | --- |
| Analytical | Main result / chart |
| ML | Model / result visualization |
| Decision analysis | Decision / result |
| Dashboard | Screenshot |
| Application | Screenshot / GIF / video |
| Library | Working example |
| Framework | Architecture / workflow |
| Research | Main finding |
| Incomplete project | Architecture + honest status |

---

## 6. See it running

Mandatory for anything interactive.

Possible evidence: screenshot, GIF, video, live demo, dashboard, API documentation, CLI output, rendered report.

If the project has a visual or interactive interface, **show the interface before asking the visitor to install it.**

A library's working example in §5 satisfies this slot. A framework's architecture diagram plus a copy-pasteable quick start satisfies it. Do not invent a GIF.

---

## 7. Audience paths

At least two depths:

| Depth | Question |
| --- | --- |
| Fast path | What did you build and why should I care? |
| Deep path | How exactly did you build and validate it? |

The four-persona table is recommended for analytical case studies, not required for libraries:

```markdown
## Explore this project
| Audience | Start here |
|---|---|
| Recruiter | 2-minute summary |
| Hiring manager | Decision + methodology |
| Technical reviewer | Code + architecture |
| Auditor | Data + validation + governance |
```

A two-row table, or a short "Start here" list with two links, is enough for tools and frameworks.

---

## 8. Results

For analytical projects. Must contain, when the project permits quantitative evaluation:

- Main metrics.
- Important comparisons.
- Decision-relevant outputs.
- Uncertainty where relevant.

Avoid "The model performed well." Prefer "MAPE was 3.0% versus 4.7% for the ridge baseline."

**Incomplete analytical projects** omit this section and say so under `Project status`. They must not invent numbers. An explicit "no results yet" statement satisfies the results slot for `incomplete: true` projects.

---

## 9. Method

Every project must explain input → transformation → analysis/model → output, at a depth that matches the type.

A software library may do this with a three-step workflow diagram. A decision-analysis project uses question → evidence → assumptions → model → uncertainty → decision. Do not paste a generic data-science funnel into a framework README.

---

## 10. Architecture

Mandatory for non-trivial projects. Prefer Mermaid where it renders cleanly; ASCII is acceptable. Link out to a dedicated architecture document when the diagram would dominate the README.

---

## 11. Data provenance

Mandatory for data / analytical projects.

Identify source, period, population, and grain. Tag claims:

| Tag | Meaning |
| --- | --- |
| `VERIFIED` | Directly supported by external / source data |
| `CALIBRATED` | Derived using documented assumptions |
| `SIMULATED` | Generated / modelled |
| `ILLUSTRATIVE` | Example only |

---

## 12. Validation

Every analytical / modeling project answers:

> **How do we know this isn't simply producing plausible-looking numbers?**

Acceptable mechanisms include holdout, cross-validation, known-truth synthetic test, baseline comparison, backtest, simulation validation, sensitivity analysis, external benchmark, unit tests, integration tests.

Preferred analytical pattern: **known truth → model recovery → baseline comparison → holdout → decision.** Report model failure when it happens.

For libraries and frameworks, a named acceptance test or gate table satisfies this slot.

---

## 13. Limitations

**Mandatory.** At least:

- What the work does not establish.
- Important assumptions.
- External validity, data, or model limits.
- What would change the conclusion (a falsification condition), where appropriate.

---

## 14. Reproducibility

Mandatory for analytical and technical projects.

```markdown
## Reproduce
```bash
...
```
```

Prefer: clone → install → test → run → reproduce artifact.

Where applicable: Python version, package manager, lockfile, seed, environment variables, data acquisition, pipeline command, expected artifact.

Libraries use `Installation` + `Quick start` for this slot.

---

## 15. Repository structure

For anything beyond a trivial project, show the meaningful structure and the responsibility of major directories. Do not dump every file.

---

## 16. Technical stack

A concise table. Explain why a technology exists where that is useful. Do not turn this into a keyword dump. Omit for tiny libraries if the install line already names the runtime.

---

## 17. Decision / practical implication

For decision-oriented projects, distinguish:

**Evidence → interpretation → decision rule → action**

---

## 18. What I would do with production data

Mandatory for portfolio projects based on public, synthetic, reconstructed, proxy, or demonstration data.

Answers: "Interesting. But what would happen if this were a real client?"

---

## 19. Status

```markdown
## Status
**Status:** ...
```

Controlled vocabulary (case-insensitive match):

- `Prototype`
- `Foundation`
- `In development`
- `Functional`
- `Complete`
- `Maintained`
- `Archived`

Optional: `Last validated: YYYY-MM-DD`.

`Active` in metadata badges is accepted as an alias of `Maintained` or `In development` only when the `## Status` section also uses a vocabulary term. Prefer the vocabulary term in the Status section itself.

---

## 20. License

Every public project: a `## License` section, or a concise license statement at the bottom, naming the license.

---

## 21. Author

Same structure everywhere. No project-specific improvisation.

```html
<table>
  <tr>
    <td>
      <strong>Rafael Braga-Kribitz</strong><br />
      Seiersberg-Pirka, Austria · Portfolio project, 2026<br />
      <a href="https://www.linkedin.com/in/rafaelbragakribitz/">LinkedIn</a>
      ·
      <a href="mailto:rafaelbragakribitz@gmail.com">rafaelbragakribitz@gmail.com</a>
    </td>
  </tr>
</table>
```

A text block with the same fields is acceptable. Required strings: `Rafael Braga-Kribitz`, `Austria`, `2026`, and the LinkedIn URL above.

---

## Tiers

### Tier A — Universal (every public portfolio project)

- [ ] Project name (H1)
- [ ] Hero visual
- [ ] One-line problem / purpose
- [ ] Status (controlled vocabulary)
- [ ] Primary evidence
- [ ] How to reproduce / use
- [ ] Repository structure or architecture
- [ ] Limitations / scope
- [ ] License
- [ ] Author

### Tier B — Analytical / DS (if the project analyzes data)

- [ ] Decision / question
- [ ] Data provenance
- [ ] Real vs modeled / synthetic distinction (epistemic tags)
- [ ] Method
- [ ] Validation
- [ ] Results, or explicit "no results yet"
- [ ] Uncertainty where applicable
- [ ] Assumptions
- [ ] Limitations
- [ ] Reproducibility
- [ ] Production-data implications (unless the project uses the client's production data)

### Tier C — Interactive / application (if `interactive: true`)

- [ ] Screenshot
- [ ] GIF or short video (if an interface exists that motion helps)
- [ ] Live demo if available
- [ ] Quick-start instructions
- [ ] User workflow
- [ ] Technical architecture
- [ ] Example interaction

---

## Standardized order

Identical across the portfolio. **Omit a section when genuinely irrelevant.**

```text
# PROJECT NAME
[HERO]
[STATUS / BADGES]
ONE-LINE PROBLEM
## Decision / What it does / The idea / Project status
## See it running
## Explore this project
## Results
## Method
## Data
## Validation
## Architecture
## Reproduce
## Limitations
## What I would do differently / Production version
## Repository structure
## Status
## License
## Author
```

---

## Visual identity system

Every public project has the same visual **slots**, not the same banner.

| Slot | Requirement |
| --- | --- |
| Hero | Always |
| Primary result | Analytical projects |
| Interface screenshot | Interactive projects |
| GIF / video | Interactive projects with a UI worth demonstrating |
| Architecture | Non-trivial technical projects |
| Supporting charts | Where they communicate evidence |

---

## Quality contract (machine-checkable)

```text
README QUALITY CONTRACT
IDENTITY
  H1 title
  hero asset
PROBLEM
  problem statement
  intended user / decision
EVIDENCE
  primary evidence
  quantitative result OR functional demonstration OR honest "no results yet"
REPRODUCTION
  installation / use instructions
  reproducibility information where applicable
TECHNICAL
  architecture for non-trivial projects
  repository structure
ANALYTICAL
  data provenance
  epistemic status
  methodology
  validation
  limitations
PORTFOLIO
  audience path
  production implications where applicable
  status
  author
  license
```

Run:

```bash
python tools/readme_audit.py --all
# or, if portfolio checkouts live elsewhere:
BRAGA_REPOS_ROOT=~/code python tools/readme_audit.py --all
```

There is no "better README." There is only a project that satisfies this contract more completely or less completely.

---

## Out of scope for v1.0

- Private repositories (including `braga-design-system-template`).
- Vendoring this checker into `governance-bootstrap`.
- Per-repo CI `make readme-audit` on consumers.
