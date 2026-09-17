"""README fixtures used by the tests (each is a complete, honest README for a fictional repo)."""
from tests.conftest import AUTHOR_BLOCK

BADGES = """[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status: Complete](https://img.shields.io/badge/status-Complete-brightgreen)](#status)
"""

ANALYTICAL = f"""# Fictional Demand Study

![Weekly demand forecast against the holdout, 90 percent intervals](docs/assets/hero.png)

{BADGES}
**Status:** Complete

Which of two order-forecast methods should a small bakery use to plan flour purchases, and how much waste does the better one avoid?

## Decision summary

Use the seasonal model: on the 12-week holdout it cut mean absolute percentage error from 18.0 percent to 9.5 percent against the naive baseline, which at current volumes is about 40 kg of flour per month not thrown away. The rule is stated below; it should be revisited if the holdout error rises above 15 percent.

## Explore this project

| Audience | Start here |
|---|---|
| Recruiter (2 min) | [Decision summary](#decision-summary) |
| Hiring manager (10 min) | [Results](#results) · [Method](#method) · [Limitations](#limitations) |
| Technical reviewer | [Architecture](#architecture) · [Reproduce](#reproduce) |
| Auditor | [Data](#data) · [Validation](#validation) |

## Results

| Model | MAPE (12-week holdout) | 90 percent interval coverage |
|---|---|---|
| Naive last-week | 18.0 percent | 88 percent |
| Seasonal model | 9.5 percent | 91 percent |

Waste avoided: 40 kg per month (10th percentile 22 kg, 90th percentile 61 kg).

## Method

Weekly order counts → calendar features → seasonal regression → 12-week holdout → decision rule (adopt if MAPE improves by at least 5 points).

## Data

| Source | Period / grain | Public? | Tag |
|---|---|---|---|
| Point-of-sale export | 2024-01-01 to 2025-12-31, weekly | no | `VERIFIED` |
| Flour price | supplier invoices, monthly | no | `VERIFIED` |
| Waste per unit | assumption from the owner | — | `CALIBRATED` |

| Tag | Meaning |
|---|---|
| `VERIFIED` | Directly supported by source data |
| `CALIBRATED` | Derived through documented assumptions |
| `SIMULATED` | Output of a seeded stochastic procedure |
| `ILLUSTRATIVE` | Example only |

## Validation

Holdout of the last 12 weeks, never used in fitting; baseline comparison against naive last-week.

## Architecture

```mermaid
flowchart LR
    A[POS export] --> B[features] --> C[seasonal model] --> D[holdout scoring] --> E[decision]
```

## Reproduce

```bash
pip install -r requirements.txt
python run.py
```

## Limitations

- Two years of data cover one full seasonal cycle only.
- Waste per unit is an owner estimate, not measured.
- **Reconsider this conclusion if** the holdout error rises above 15 percent.

## What I would do with production data

- Use per-product counts instead of totals.

## Repository structure

```text
run.py          pipeline entry point
data/           point-of-sale export (private)
reports/        generated tables and the hero chart
```

## Status

**Status:** Complete

Last validated 2026-01-15.

## License

MIT. See [`LICENSE`](LICENSE).

{AUTHOR_BLOCK}"""

LIBRARY = f"""# tinycsv

![Rendered output of the minimal example](docs/assets/example.png)

{BADGES}
**Status:** Functional

Reading a CSV with Python's standard library takes six lines and still silently accepts a ragged row; tinycsv reads it in one call and refuses ragged input.

## What it does

`read(path)` returns a list of dictionaries keyed by header, validates that every row has the header's width, and raises `RaggedRow` with the offending line number otherwise. Nothing else.

## Quick start

```python
import tinycsv
rows = tinycsv.read("orders.csv")
```

## Explore this project

| Path | Start here |
|---|---|
| Fast path | [Quick start](#quick-start) |
| Deep path | [API reference](#api-reference) · [What it enforces](#what-it-enforces) |

## Install

```bash
pip install tinycsv==0.2.0
```

## What it enforces

| Rule | Where |
|---|---|
| Every row has the header's width | `read()` raises `RaggedRow` |
| Headers are unique | `read()` raises `DuplicateHeader` |

## API reference

| Function | Purpose |
|---|---|
| `read(path, encoding="utf-8")` | Read a CSV file into a list of dicts |
| `RaggedRow` | Raised on a row of the wrong width |

## Validation

`pytest` runs 14 tests covering both errors and the happy path.

## Limitations

- No streaming: the whole file is read into memory.
- No quoting dialect detection beyond the standard library's defaults.

## Repository structure

```text
tinycsv.py      the module
tests/          pytest suite
docs/           example image
```

## Status

**Status:** Functional — v0.2.0, 2026-02-01.

## License

MIT. See [`LICENSE`](LICENSE).

{AUTHOR_BLOCK}"""

FOUNDATION = f"""# Fictional Tide Model

![Pipeline diagram](docs/assets/hero.png)

[![Status: Foundation](https://img.shields.io/badge/status-Foundation-orange)](#status)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Status:** Foundation

How much earlier could a harbour issue flood warnings if tide gauges were fused with pressure forecasts, and what would a false alarm cost?

## Project status

The gauge ingest and the warehouse are built and tested. The fusion model, the warning rule, and the cost analysis are not built. No results exist yet; they land at milestone M3.

## Explore this project

| Audience | Start here |
|---|---|
| Reviewer | [Project status](#project-status) · [Architecture](#architecture) |
| Implementer | [Reproduce](#reproduce) · [`docs/SPEC.md`](docs/SPEC.md) |

## Method

Gauge readings → hourly warehouse → (planned) fusion model → (planned) warning rule → (planned) cost table.

## Data

| Source | Period / grain | Tag |
|---|---|---|
| Harbour tide gauge | 2020-01-01 onward, 10-minute | `VERIFIED` |

| Tag | Meaning |
|---|---|
| `VERIFIED` | Directly supported by source data |
| `CALIBRATED` | Derived through documented assumptions |
| `SIMULATED` | Output of a seeded stochastic procedure |
| `ILLUSTRATIVE` | Example only |

## Validation

Ingest gates: no gaps longer than one hour; readings inside the gauge's physical range. Model validation is planned for M3.

## Architecture

```mermaid
flowchart LR
    G[gauge] --> I[ingest] --> W[warehouse] --> M[fusion model, planned]
```

## Reproduce

```bash
pip install -r requirements.txt
python ingest.py
```

## Limitations

- **No results yet.** Nothing here answers the warning-time question.
- One gauge only; the pressure forecast source is not yet chosen.

## Repository structure

```text
ingest.py       gauge ingest
docs/           SPEC.md
tests/          ingest gate tests
```

## Status

**Status:** Foundation

M0 and M1 complete; M2 and M3 pending. 2026-03-01.

## License

MIT. See [`LICENSE`](LICENSE).

{AUTHOR_BLOCK}"""

MINIMAL = """# my_project

This is a Python project that does things.

## Installation

pip install .
"""
