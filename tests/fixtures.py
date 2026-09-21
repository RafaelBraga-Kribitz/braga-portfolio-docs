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

# A gitdiagram graph after the design-system restyling in blocks/architecture-mermaid.md:
# every subgraph, node, edge label and click line as generated; only classDef/class replaced.
ARCH_MERMAID = """```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "#E6E6E6", "lineColor": "#A0A0A0"}}}%%
flowchart TD

subgraph group_data["Data Preparation"]
  node_ingest["Order ingest<br/>[run.py]"]
end

node_analyst(("Analyst")) -->|"runs the pipeline"| node_ingest

click node_ingest "https://github.com/rafaelbraga-kribitz/study/blob/main/run.py"

classDef node fill:#E6E6E6,stroke:#A0A0A0,stroke-width:1px,color:#282828
classDef accent fill:#E6E6E6,stroke:#FA6400,stroke-width:1px,color:#282828
class node_ingest,node_analyst node
class node_analyst accent
```

*Generated by gitdiagram (gitdiagram.com) from commit [`a1b2c3d`](https://github.com/RafaelBraga-Kribitz/study/tree/a1b2c3d) on 2026-09-21. The generator declares: "Some orchestration internals are unsampled, so only README- or source-supported relationships are shown."*"""

# An analytical README that satisfies the whole communication family, used as the
# passing side of every communication.* test; each test mutates one thing to fail it.
COMMUNICATION = f"""# Fictional Demand Study

![Generated banner for the Fictional Demand Study](docs/assets/hero.png)

{BADGES}
**Status:** Complete

Which of two order-forecast methods should a small bakery use to plan flour purchases, and how much waste does the better one avoid?

## Decision summary

Use the seasonal model: on the 12-week holdout it cut mean absolute percentage error from 18.0 percent to 9.5 percent against the naive baseline, which at current volumes is about 40 kg of flour per month not thrown away.

![Weekly mean absolute percentage error of both models over the 12-week holdout, seasonal model lower in 10 of 12 weeks](reports/f01_holdout_error.png)

*The seasonal model is below the naive baseline in ten of the twelve holdout weeks; the two crossings are both in the Christmas fortnight.*

## Explore this project

| Audience | Start here |
|---|---|
| Recruiter (2 min) | [Decision summary](#decision-summary) |
| Hiring manager (10 min) | [Results](#results) · [Method](#method) · [Limitations](#limitations) |
| Technical reviewer | [Architecture](#architecture) · [Reproduce](#reproduce) |
| Auditor | [Data](#data) · [Validation](#validation) |

## Results

### The seasonal model halves forecast error, 18.0 to 9.5 percent

| Model | MAPE (12-week holdout) | 90 percent interval coverage |
|---|---|---|
| Naive last-week | 18.0 percent | 88 percent |
| Seasonal model | 9.5 percent | 91 percent |

Waste avoided: 40 kg per month (10th percentile 22 kg, 90th percentile 61 kg).

![Flour waste per month under each model, with the 10th to 90th percentile band](reports/f02_waste_band.png)

*Waste under the seasonal model, with the band the Monte Carlo run produced; the naive line sits above the band in every month.*

![Residuals by weekday, showing the Saturday over-forecast the model does not remove](reports/f03_residuals.png)

*Saturday residuals stay positive, which is the known limitation listed below.*

## Method

Weekly order counts → calendar features → seasonal regression → 12-week holdout → decision rule (adopt if MAPE improves by at least 5 points).

## Data

| Source | Period / grain | Public? | Tag |
|---|---|---|---|
| Point-of-sale export | 2024-01-01 to 2025-12-31, weekly | no | `VERIFIED` |

| Tag | Meaning |
|---|---|
| `VERIFIED` | Directly supported by source data |
| `CALIBRATED` | Derived through documented assumptions |
| `SIMULATED` | Output of a seeded stochastic procedure |
| `ILLUSTRATIVE` | Example only |

## Validation

Holdout of the last 12 weeks, never used in fitting; baseline comparison against naive last-week.

## Architecture

An analyst runs the pipeline; order counts are ingested, features are built, the seasonal model is fitted and scored on the holdout, and the decision rule is applied.

{ARCH_MERMAID}

## Reproduce

```bash
pip install -r requirements.txt
python run.py
```

## Limitations

- Two years of data cover one full seasonal cycle only.
- Saturday is systematically over-forecast.
- **Reconsider this conclusion if** the holdout error rises above 15 percent.

## What I would do with production data

- Use per-product counts instead of totals.

## Repository structure

```text
run.py          pipeline entry point
data/           point-of-sale export (private)
reports/        generated tables and charts
```

## Status

**Status:** Complete

Last validated 2026-01-15.

## License

MIT. See [`LICENSE`](LICENSE).

{AUTHOR_BLOCK}"""
