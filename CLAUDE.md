# CLAUDE.md — agent protocol for braga-portfolio-docs

This repository is the single source of truth for the BRAGA README Quality Standard. Any agent that
touches a public portfolio README works against it.

## First action of every session

1. Read [`docs/AGENT_GUIDE.md`](docs/AGENT_GUIDE.md) (how to run the gate, what it fixes, what it never fixes, and the chart review items that must never become checks).
2. Read [`manifest/portfolio.yaml`](manifest/portfolio.yaml) for the target project's declared `type`, `status`, `hero`, `demo`, `architecture_diagram`, and license facts.
3. Read [`docs/README_STANDARD.md`](docs/README_STANDARD.md) only when a requirement's intent is unclear; `python -m readme_quality explain <id>` is faster.

## Done means the gate passes

```bash
python -m readme_quality audit --repo /path/to/project --verbose    # exit 0 = PASS
```

Exit 1 is `FAIL`; exit 2 is `BLOCKED_HUMAN` (report the reason, do not work around it).

## Rules

- Standardize presentation and evidence architecture, not intellectual content. Preserve every existing section; reorder and reframe; delete only what is obsolete, wrong, duplicated, or misleading.
- Never invent numbers, results, licenses, screenshots, URLs, or capabilities. Every fact in a README exists in the repository first.
- Never write placeholders (`TBD`, `Coming soon`, `{{ }}`); the gate fails on them.
- Set not-applicable states through the registry (`demo: static` + reason, `public_data: false`, `estimation: none`, `incomplete: true`, `architecture_diagram: none` + reason), never with filler sections.
- Never write alt text or a caption for a chart you have not looked at. The alt text of a primary chart comes from `primary_chart_alt` in the registry, written by the author; the descriptor describes the project, not the chart.
- Architecture diagrams come from [gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram) through its **web app** — it has no CLI and no public API. Do not invent a command line for it. Procedure: [`docs/ARCHITECTURE_DIAGRAMS.md`](docs/ARCHITECTURE_DIAGRAMS.md).
- A new check lands at `recommended`, with a promotion condition recorded in `docs/README_STANDARD.md` §6. A check introduced as `required` pressures the next person to weaken it.
- Do not weaken a check to make a repository pass. If a check is wrong, fix it here with a test, bump the manifest version, and re-audit the portfolio.
- Do not change an existing license. Follow [`docs/LICENSE_POLICY.md`](docs/LICENSE_POLICY.md); escalate with `license_blocked_reason` when ownership is unclear.

## Where things live

| You want | Read |
|---|---|
| The contract | `docs/README_STANDARD.md`, `manifest/requirements.yaml` |
| Architecture diagrams | `docs/ARCHITECTURE_DIAGRAMS.md`, `blocks/architecture-mermaid.md`, `blocks/architecture-provenance.md` |
| Project facts | `manifest/portfolio.yaml` |
| The checks | `readme_quality/checks.py` |
| Safe fixes | `readme_quality/fix.py`, `blocks/` |
| Hero banner | `readme_quality/hero.py` |
| Starting structures | `templates/` |
| CI | `ci/readme-quality.yml` |
