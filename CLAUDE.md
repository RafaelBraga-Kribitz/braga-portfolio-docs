# CLAUDE.md — Agent protocol for braga-portfolio-docs

This repository is the **single source of truth** for the BRAGA Portfolio Project README Standard. Claude Code (and any other agent) must treat files here as normative for public-portfolio README work.

## First action of every session

1. Read [`docs/README_STANDARD.md`](docs/README_STANDARD.md).
2. Read [`tools/portfolio.yaml`](tools/portfolio.yaml) for the target project’s declared `type`, `interactive`, `incomplete`, and `production_data_section` flags.
3. Do not invent a parallel documentation methodology.

## When editing a project README

Work in the **target project repository**, not by dumping the standard into that README.

Contract:

- Standardize **presentation and evidence architecture**, not intellectual content.
- Omit sections that are genuinely irrelevant — do not fill with boilerplate.
- README = executive interface to the repository. Push long methodology, governance, and reports into linked artifacts.
- Reuse existing charts / screenshots / architecture diagrams for the hero. Do not manufacture decorative banners or fake GIFs.
- Do not invent metrics, results, licenses, or “complete” claims that are not already on disk in the target repo.
- Use the standard author block (name, Austria, 2026, LinkedIn URL from `portfolio.yaml`).

## Done means the checker passes

From this repository (with portfolio checkouts under `$BRAGA_REPOS_ROOT`, default `~/code`):

```bash
python tools/readme_audit.py --name <registry-name>
# or
python tools/readme_audit.py --repo /path/to/target/checkout
```

Exit code 0 / `PASS` is required before claiming the README satisfies the contract.

`make readme-audit` runs `--all` against the registry.

## Anti-patterns (banned)

- Inferring project type from folder names or README prose when the project is in `portfolio.yaml`.
- Homogenizing an MMM case study and a library into the same prose shape.
- Quoting results that do not exist yet (especially `incomplete: true` analytical projects).
- Claiming “audited / complete / fixed” without a passing checker run.
- Editing this standard and a project README in the same PR without an explicit request.

## Where things live

| You want | Read |
|---|---|
| The contract | `docs/README_STANDARD.md` |
| Project types | `tools/portfolio.yaml` |
| Checker | `tools/readme_audit.py` |
| How humans use this repo | `README.md` |

## What this file does not do

- It does not summarize individual portfolio projects.
- It does not replace each project’s own `CLAUDE.md` / governance protocol.
- It does not authorize inventing product claims to fill README slots.
