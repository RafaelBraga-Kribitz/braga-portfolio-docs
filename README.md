# braga-portfolio-docs

SSOT for the **BRAGA Portfolio Project README Standard v1.0**.

Every public portfolio project has the same documentation contract. This repository holds the contract, the machine-checkable checker, and the project-type registry. It does **not** rewrite project READMEs — those stay in each project’s own repository.

## What it does

| Path | Role |
|---|---|
| [`docs/README_STANDARD.md`](docs/README_STANDARD.md) | Human-readable contract (tiers A/B/C, section order, visual slots) |
| [`tools/readme_audit.py`](tools/readme_audit.py) | Structural slot checker |
| [`tools/portfolio.yaml`](tools/portfolio.yaml) | Declared project types — the checker never infers type from prose |

## Status

**Status:** Maintained

## Explore this project

| Audience | Start here |
|---|---|
| Recruiter / hiring manager | [`docs/README_STANDARD.md`](docs/README_STANDARD.md) §§1–7 |
| Cursor / Claude Code | [`CLAUDE.md`](CLAUDE.md) |
| Technical reviewer | `python tools/readme_audit.py --help` |

## Quick start

```bash
git clone https://github.com/RafaelBraga-Kribitz/braga-portfolio-docs.git
cd braga-portfolio-docs
python -m pip install -r requirements.txt

# Audit one checkout (type defaults to library if the path is not in the registry)
python tools/readme_audit.py --repo ~/code/warehouse_humanoid_tco

# Audit every registered public project (sibling directories under BRAGA_REPOS_ROOT)
export BRAGA_REPOS_ROOT=~/code   # folder that contains the portfolio clones
python tools/readme_audit.py --all
```

Or: `make readme-audit`.

## Use with Claude Code

1. Clone this repo next to your portfolio checkouts (or anywhere; set `BRAGA_REPOS_ROOT`).
2. Open **this** repo in Claude Code, or open a project repo and `@`-mention files here.
3. Claude Code reads [`CLAUDE.md`](CLAUDE.md) at session start: README work must satisfy the standard and pass the checker.

Example first message in a project repo:

```text
Read ../braga-portfolio-docs/docs/README_STANDARD.md and
../braga-portfolio-docs/tools/portfolio.yaml for this project's type.
Retrofit README.md to the contract. Stop when:
python ../braga-portfolio-docs/tools/readme_audit.py --repo . exits 0.
```

## Use with Cursor

Same contract. Point agents at this repository (or keep a Project-store mirror in sync with it). Prefer this GitHub repo as the canonical copy going forward.

## Repository structure

```text
.
├── CLAUDE.md                 # Claude Code / agent protocol
├── README.md                 # this file
├── Makefile                  # make readme-audit
├── requirements.txt          # PyYAML
├── docs/
│   ├── README_STANDARD.md    # the contract
│   ├── readme-audit-baseline.md
│   └── readme-audit-after.md
└── tools/
    ├── portfolio.yaml        # type registry
    └── readme_audit.py       # checker
```

## Limitations

- The checker validates **slots**, not prose quality.
- Project type must be declared in `portfolio.yaml` (or passed via `--repo` defaults).
- Private repos are out of scope for the public registry.
- Creating or installing GitHub App access on new repos is a human step.

## License

MIT — see [`LICENSE`](LICENSE).

## Author

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
