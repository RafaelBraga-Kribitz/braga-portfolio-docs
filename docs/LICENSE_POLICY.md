# License policy for public portfolio repositories

Applies to `meta.license_file` and `meta.license_section` in the README Quality Gate. The fixer
(`readme_quality/fix.py::Fixer.decide_license`) implements exactly this order. It **never changes
an existing license** and **never guesses when ownership or bundled material is unclear**.

## 1. Decision order

| Step | Evidence | Outcome |
|---|---|---|
| 1 | A `LICENSE` / `LICENSE.md` / `LICENCE` / `COPYING` file exists | Keep it. The README `## License` section and badge must name the same license. |
| 2 | Registry sets `license_blocked_reason` | `BLOCKED_HUMAN`. No file is written; the README states truthfully that no license file exists. |
| 3 | Registry sets `license:` | Create that license (registry is the owner's explicit decision). |
| 4 | Package metadata declares a license (`pyproject.toml` `license`, `package.json` `license`, `setup.cfg`) | Create a LICENSE with that text. The metadata is the author's own declaration. |
| 5 | The README already names a license in its License section or status line | Create that license. |
| 6 | None of the above | **MIT**, the portfolio default (§3), **only if** §2 does not apply. |

Copyright line: `Copyright (c) <year of first commit> Rafael Braga-Kribitz`.

## 2. When the policy must escalate instead of deciding

Set `license_blocked_reason` in `manifest/portfolio.yaml` when any of these hold:

- The repository bundles third-party material whose rights are not the author's (downloaded reference
  images, scraped pages, copied datasets, vendored code under another license). An MIT file at the root
  would purport to license that material.
- The repository is framed as a product with commercial or launch intent and no license is declared
  anywhere. Choosing between MIT, Apache-2.0, and a restrictive license is the owner's call.
- The code was produced under a contract or for an employer.
- Two sources disagree (for example `package.json` says ISC while a README says MIT).

Current escalations: `NextMove` (product framing, no declaration anywhere) and
`Chart_Audit_Framework` (bundled third-party references).

## 3. Portfolio default and alternatives

| License | Use when | Canonical text |
|---|---|---|
| **MIT** (default) | Portfolio code, analyses, libraries, frameworks written by the author with no patent concerns. Matches every licensed repository in the portfolio today. | `blocks/licenses/mit.txt` |
| **Apache-2.0** | A library others will embed where an explicit patent grant matters, or when contributions from others are expected. | `blocks/licenses/apache-2.0.txt` |
| **ISC** | Only when package metadata already declares it (npm default). Functionally equivalent to MIT. | `blocks/licenses/isc.txt` |
| **CC BY 4.0** (documents) | Reports, decision documents, and aggregated outputs published alongside code. Declared in the README License section in addition to the code license, as `austria-data-job-market-intelligence` does. | not auto-generated |
| Restrictive (e.g. PolyForm Noncommercial, source-available) | Product repositories where the owner wants to keep commercial rights. | not auto-generated; owner's decision |

## 4. What the README must say

- With a LICENSE file: `## License` names the license and links the file (block `blocks/license.md`).
- Without one: `## License` states that no license file exists and that no rights are granted
  (block `blocks/license-none.md`). Naming a license in the README without a file is a `FAIL`.
- The badge row carries a license badge only when the file exists, and it must name the same license.

## 5. Changing a license later

Changing an existing license is a human action: edit the file, the registry `license:` field, and let
the fixer align the README section and badge. The gate will fail until all three agree.
