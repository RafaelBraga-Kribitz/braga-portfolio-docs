# Agent guide — README Quality Gate

For coding agents (Claude Code, Cursor, Codex) working on any public BRAGA repository. Read this
before touching a README. The human-readable contract is [`README_STANDARD.md`](README_STANDARD.md);
the machine-readable one is [`../manifest/requirements.yaml`](../manifest/requirements.yaml).

## The one command

```bash
# from a checkout of braga-portfolio-docs, with the portfolio clones as sibling folders
python -m readme_quality audit --repo /path/to/project --verbose
```

Exit code `0` = PASS or PASS_WITH_EXCELLENCE, `1` = FAIL, `2` = BLOCKED_HUMAN (nothing fails, but a
human decision is pending). `make readme-audit REPO=/path/to/project` is the same thing.

## Mode A — you are building one project

The README is a living artifact. Run the gate whenever you change scope, add a result, or touch
`README.md`, and keep it green:

```bash
python -m readme_quality detect  /path/to/project        # what type does the repo look like? (registry wins if listed)
python -m readme_quality audit   --repo /path/to/project  # what is missing, with evidence
python -m readme_quality fix     --repo /path/to/project  # apply the safe fixes, re-audit
python -m readme_quality explain identity.hero            # what a requirement id means and how it is remediated
```

If the project is not yet in `manifest/portfolio.yaml`, add it (type, status, title, descriptor, hero,
demo). The registry is the only place where type and status are declared; the gate never infers them
from prose.

No README yet? Copy `templates/<type>.md`, then replace every `<!-- TEMPLATE: ... -->` comment with
content taken from the repository. The gate fails on leftover template markers and on placeholders
(`TBD`, `Coming soon`, `{{ }}`), so an unfilled template cannot pass.

## Mode B — you are remediating the portfolio

```bash
make readme-audit                      # table of every registered repository
make readme-fix                        # safe automatic remediation everywhere, then re-audit
python -m readme_quality portfolio --fix --only bk-viz funnel_correlation_py   # a subset
```

Then work through the remaining `FAIL` items by hand (see "What you may and may not do").
Stop when every repository is `PASS`, `PASS_WITH_EXCELLENCE`, or `BLOCKED_HUMAN` with a stated reason.

## Status vocabulary the gate emits

| Status | Meaning | Counts against the gate? |
|---|---|---|
| `PASS` | requirement satisfied | no |
| `PASS_WITH_EXCELLENCE` | an optional excellence requirement is satisfied (persona table, claim tracing, why-section, project-specific sections) | no |
| `NOT_APPLICABLE` | requirement does not apply to this project type or registry flags | no |
| `WARN` | a `recommended` requirement is not met | no |
| `FAIL` | a `required` requirement is not met | **yes** |
| `BLOCKED_HUMAN` | cannot be decided from repository evidence (today: license ownership, missing registry status) | no, but reported |

The gate is pass/fail on `required` requirements only. It never scores prose.

## What the fixer does automatically (and what it never does)

Automatic, from repository evidence or the registry: H1 from the registry title; the vanity banner
generated in the design system (or the declared banner) placed first, with the identity zone reordered to
banner, badges, status line, prose, then other visuals; badge row (CI / reproducibility /
governance workflows that exist, runtime from `pyproject.toml` or `.python-version`, license from the
`LICENSE` file, status from the registry); `**Status:**` line; `## Status` section with the last-commit
date; `LICENSE` file per [`LICENSE_POLICY.md`](LICENSE_POLICY.md); `## License` section that matches
the file; canonical `## Author` block with the portrait vendored to `docs/assets/`; factual `## Repository structure` (names and file counts only);
broken relative paths repaired when the basename is unique; audience rows linked to their sections;
the epistemic-tag legend inserted where tags are used but unexplained.

Never automatic: problem statements, executive summaries, results, methods, validation, limitations,
production-data implications, architecture prose, API references. These need reading the repository.
When you write them:

1. Every number, date, source, URL, and capability must already exist in the repository. Say where it
   came from in your commit or report.
2. Preserve existing content. Reorder and reframe; delete only what is obsolete, wrong, duplicated,
   or misleading.
3. Sections outside the standard vocabulary are **kept** and reported as `project_specific_excellence`.
   If the same extra section proves useful in several repositories, propose promoting it into the
   manifest (bump `version`, add tests).
4. Set `NOT_APPLICABLE` states through the registry (`demo: static` with `demo_reason`,
   `public_data: false`, `estimation: none`), never by writing filler sections.

## Requirement ids at a glance

`identity.*` (h1, hero, badges, problem, status_line) · `executive.summary` · `evidence.*` (primary,
see_it_running, demo_motion, live_demo) · `navigation.audience` · `analytical.*` (decision, results,
quantitative, uncertainty, data, epistemic, method, validation, production_data) ·
`technical.*` (architecture, structure, reproduce, stack) · `library.*` (example, contract, api,
install_pin) · `honesty.*` (limitations, falsification, placeholders, hype, status_section,
no_results_statement) · `links.*` (images, internal) · `meta.*` (license_file, license_section,
author, length) · `excellence.*` (audience_personas, claim_tracing, why, project_specific).

`python -m readme_quality explain <id>` prints applicability, severity, evidence, and remediation.

## CI

Copy [`../ci/readme-quality.yml`](../ci/readme-quality.yml) into a repository's `.github/workflows/`.
It runs in about ten seconds and fails only on `FAIL`.

## Verify you are done

```bash
make test                                   # the gate's own tests
python -m readme_quality audit --repo .     # this repository passes its own gate
make readme-audit                           # portfolio table: no FAIL rows
```
