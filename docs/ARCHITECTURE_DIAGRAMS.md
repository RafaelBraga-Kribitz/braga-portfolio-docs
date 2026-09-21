# Architecture diagrams — gitdiagram procedure

**Status:** Active · **Introduced:** standard v1.3, 2026-09-21 · **Owner:** Rafael Braga-Kribitz
**Blocks:** [`../blocks/architecture-mermaid.md`](../blocks/architecture-mermaid.md) · [`../blocks/architecture-provenance.md`](../blocks/architecture-provenance.md)
**Requirements:** `technical.architecture` (required) · `technical.architecture_links` (recommended in v1.3)

For `analytical`, `application` and `framework` projects the inline architecture diagram is a
[gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram) graph restyled to the Braga-Kribitz design
system, unless the registry declares `architecture_diagram: manual` or `none` with a reason.

## 1. What gitdiagram is, and what it is not

gitdiagram turns a GitHub repository into a Mermaid architecture graph plus a short prose overview of
the principal workflow. Each node can carry a `click` line linking to the real file it stands for. It
reads the default branch's tree and README plus a bounded set of source excerpts, then asks a model to
produce the graph; the server validates every linked path against the repository before returning it.

It is a **model-generated description of the repository**, not a derivation from it. Two runs over the
same commit can differ. That is why the provenance line in §5 pins the commit and the date, and why
`technical.architecture_links` re-checks every linked path against the checkout on every gate run.

## 2. How it actually runs — verified 2026-09-21

Checked against the repository at `github.com/ahmedkhaleel2004/gitdiagram` (`README.md`,
`docs/architecture.md`, `package.json`, `scripts/`):

| Interface | Exists? | Evidence |
|---|---|---|
| Command-line entry point | **No** | `package.json` declares no `bin`. The four files in `scripts/` are dev and ops utilities (`check-performance-budgets.mjs`, `complimentary-quota-today.mjs`, `dev-turbo.sh`, `migrate-browse-index.ts`); none generates a diagram. |
| Public HTTP API for third parties | **No** | `docs/architecture.md` documents `/api/generate/cost`, `/api/generate/stream`, `/api/generate/cancel`, `/api/diagram-state`, `/api/healthz` as **same-origin** Next.js Route Handlers, rate limited. They serve the app's own front end; no external contract is published. |
| Self-hosting | **Yes, but it is the same web app** | `bun install` then `bun run dev`, and it "Requires Bun, Cloudflare R2, Upstash Redis, and an OpenAI or OpenRouter API key". A `Dockerfile` and `railway.json` exist as a documented cold-recovery recipe. |
| Hosted web app | **Yes — this is the interface we use** | `https://gitdiagram.com/<owner>/<repo>`, or replace `hub` with `diagram` in any GitHub URL. Exports PNG or copies the Mermaid source. |

**There is no headless invocation.** Running it locally still means starting a Next.js application, an
object store, a Redis instance and a paid model key, in order to open a page in a browser and copy the
output by hand. For thirteen repositories that is not worth the operational surface. **The procedure below
uses the hosted web app, and the workflow is built around a human step by design.**

If that changes — a `bin` entry, a documented public endpoint, a generate-and-exit script — this section
is what to re-verify, and the procedure in §3 becomes automatable.

## 3. Procedure

1. **Pin the commit.** `git -C <checkout> rev-parse --short HEAD`. The diagram describes *this* commit.
   Push it first: gitdiagram reads the default branch on GitHub, not your working tree.
2. **Generate.** Open `https://gitdiagram.com/<owner>/<repo>`. For a private repository, supply a GitHub
   token through **Private Repos** in the header — it is the user's token, entered by the user.
3. **Copy the Mermaid source**, not the PNG. The README carries the graph as text so the `click` links
   work, the diagram stays diffable, and `technical.architecture_links` can check it.
4. **Copy the overview paragraph** as well. It goes above the diagram (§4).
5. **Restyle it with the tool, not by hand.** Save the copied Mermaid to a file and run:

   ```bash
   python -m readme_quality diagram --name <project> --input raw.mmd --accent <node_id> --out block.md
   ```

   Omit `--accent` and it lists the candidates (nodes with no incoming edge, nodes with no outgoing
   edge) and exits without guessing — which node carries the orange is a per-project decision. The
   tool replaces only the `%%{init}%%`, `classDef` and `class` lines, keeps every `subgraph`, node,
   edge, edge label and `click` line byte-for-byte, and verifies every click target against the
   checkout as it goes. A hand transformation is a transformation that can silently change the graph;
   [`../blocks/architecture-mermaid.md`](../blocks/architecture-mermaid.md) documents what it produces
   and why.
6. **Record provenance** under the diagram using
   [`../blocks/architecture-provenance.md`](../blocks/architecture-provenance.md).
7. **Record it in the registry** in `manifest/portfolio.yaml`:

   ```yaml
   architecture_diagram: gitdiagram
   architecture_diagram_commit: a1b2c3d
   architecture_diagram_generated: 2026-09-21
   ```

8. **Re-run the gate.** `python -m readme_quality audit --repo <checkout> --verbose`.
   `technical.architecture_links` must be `PASS`, not `NOT_APPLICABLE`.

Regenerate when the module layout changes, not on every commit. A diagram whose `click` targets still
resolve is still true about the structure it claims; `technical.architecture_links` is what tells you
when that stops being the case.

## 3a. What the generator will not tell you: a resolving link is not an implemented module

`technical.architecture_links` proves a path exists. It cannot prove the file behind it does anything.
gitdiagram samples source excerpts and infers a workflow; a module that is a written contract with
`raise NotImplementedError` in every function looks, from the outside, exactly like a module that runs.

The first portfolio run hit this. In `energy-procurement-risk-analyzer` (registry `incomplete: true`,
status `Foundation`, descriptor *"Ingest and warehouse built; strategy results not yet"*) all eighteen
click targets resolved, and four of them are stubs:

| Node | File | State |
|---|---|---|
| `node_retrospective_engine` | `src/epra/strategies/retrospective.py` | `raise NotImplementedError` |
| `node_forward_risk` | `src/epra/strategies/forward_risk.py` | `raise NotImplementedError` |
| `node_regime_analytics` | `src/epra/analytics/regimes.py` | `raise NotImplementedError` |
| `node_consumer_profile` | `src/epra/consumer/profile.py` | `raise NotImplementedError` |
| `node_exports` | `exports/` | `.gitkeep` only |
| `node_dashboards` | `dashboards/` | `.gitkeep` + a README |

The graph drew those with **solid** edges — `"writes costs"`, `"writes risk"`, `"feeds dashboards"`,
`"presents decisions"` — which asserts a workflow the repository does not yet perform. The generator's
prose did hedge (*"several corresponding modules are explicitly not implemented yet"*), but a reader
looks at the graph.

**Use a dashed edge (`-.->`) for a stage that is specified but not built**, and say so in the sentence
above the diagram. gitdiagram does this correctly when it notices: the `NextMove` run marked every
Phase 2 stage dashed and stated the boundary in its overview. Changing an edge's *style* to match the
repository is a presentation fix of the kind this standard already sanctions; changing the graph's
topology is not.

Check this before committing a diagram for any project with `incomplete: true`.

## 3b. Link the nodes gitdiagram left unlinked

gitdiagram links the nodes it sampled from source. It leaves external services, input artifacts and
abstractions unlinked, and the tool reports them (`N node(s) with no click line`). Most of those are
worth linking; the rule is the standard's existing one — **the target must already exist in the
repository, or be the thing the repository names.** Never a URL from memory.

| Node kind | Link it to | Example |
|---|---|---|
| External data source or service | the URL the repository itself cites, in source, config or an ADR | `node_entsoe_api` → `https://transparency.entsoe.eu`, cited in EPRA |
| Hosted output | the registry `hosted_urls` entry | `node_tableau` → the Tableau Public dashboard |
| Upstream dataset | the publisher's page for the pinned ids | `node_huggingface` → `https://huggingface.co/unitreerobotics`, the owner of all five pinned `repo_id`s |
| A declared artifact or contract | the file that declares it | `node_processed_artifacts` → `dvc.yaml` |
| An internal abstraction | the class or function that is it, with a `#L` anchor | `node_audit_result` → `dsx/findings.py#L92` |
| A **person** (analyst, operator, decision maker) | **nothing** — leave it unlinked | `node_analyst` |

Two rules that keep this honest:

- **Where two candidate URLs exist, the repository decides.** EPRA cites both
  `.../fakten/strompreisindex` and `.../fakten/strompreisindizes`; ADR-008 pins the first as the *sole*
  source, so that is the link. Do not pick the one that looks newer.
- **A `tree/` link to a gitignored or DVC-tracked directory is a trap.** It resolves on disk and the
  GitHub URL works, but a reader lands on an empty folder, and `technical.architecture_links` cannot
  see the difference — it tests the working tree. `python -m readme_quality diagram` does check git and
  warns; link the artifact declaration instead of the empty directory.

Off-GitHub targets are reported by both the check and the tool and failed by neither: nothing here
reaches the network. Verify them by hand once, at authoring time.

## 3c. Direction: measure it, do not assume it

GitHub renders a Mermaid block in a fixed-width sandboxed iframe inside the README column.
Measured on a repository page, 2026-09-21:

| Viewport | README column | What a wide graph does |
|---|---|---|
| 1920 px | **838 px** (GitHub's cap) | scaled down to fit |
| 1240 px | **783 px** | scaled down to fit |
| 375 px (phone) | **309 px** | scaled down to fit |

A graph wider than ~800 px is not clipped, it is *shrunk*, and the node labels go with it. At
scale 0.3 a `[module_03_tco.py]` label is unreadable.

**The direction that fits depends on the graph's shape, and the intuition is often backwards.**
`TD` runs the *flow* vertically but lays sibling subgraphs out **side by side**, so a graph with four
parallel subgraphs is wider in TD than in LR. Measured on two real graphs:

| Graph | Direction | Natural size | Fits 783 px? | Scale needed |
|---|---|---|---|---|
| `warehouse_humanoid_tco`, 4 subgraphs, 20 nodes | TD *(as gitdiagram emits it)* | 2968 × 766 | no | 0.26 |
| same graph | LR | 1671 × 1600 | no | 0.47 |
| this repository's README, 8 nodes, no subgraphs | LR | 1848 × 302 | no | 0.42 |
| same graph | **TD** | **646 × 569** | **yes** | 1.21 |

Sizes are measured with the design system's mono label font applied; a different font changes them. A near-linear chain is wide in LR and fits in TD — that is why this repository's own diagram is TD.
A graph with several parallel subgraphs is wide in TD and merely less wide in LR — neither fits, and
the direction flag is not the fix. **Reduce the node count or split the diagram** when even the
better direction needs a scale below ~0.6. The `warehouse_humanoid_tco` graph is in that bracket in
both directions: 0.26 in TD, 0.47 in LR. LR is the better of the two and still not enough, so the real
remedy there is fewer nodes or two diagrams, not a flag.

**Set `fontFamily` at the top level of the `%%{init}%%` config, not only under `themeVariables`.**
Mermaid 11 ignores the `themeVariables` copy: rendered side by side, a themeVariables-only directive
falls back to the surrounding page font while a top-level one applies. The tool and the blocks set
both. Font metrics change layout, so a font that silently fails to apply also changes every width
measured above.

### How to measure

`--direction` changes layout only; no node, edge or click line moves:

```bash
python -m readme_quality diagram --name <project> --input raw.mmd --accent <node> --direction TD
```

To check before committing, render the block in a page whose container is 783 px wide and read the
SVG's `viewBox` width — that is the natural width Mermaid needs. Anything at or under 783 renders at
full size.

## 4. A diagram is not an explanation

gitdiagram produces a workflow overview paragraph alongside the graph. **That paragraph belongs in the
README, above the diagram.** A graph with no sentence naming the principal workflow is a picture: a
reader can see that eighteen boxes are connected without learning what runs, in what order, to produce
what. The sentence carries the argument; the graph carries the structure.

Write it as prose in the repository's own voice if the generated wording does not fit — the requirement
is that the principal workflow is stated, not that the generator's sentence is quoted.

## 5. Provenance is required, including the generator's own caveat

Every architecture diagram carries a provenance line naming the generator, the commit, the date, and any
limitation the generator itself declared.

The last clause is the one that gets dropped, and it is the one the evidence hierarchy needs. gitdiagram's
overview for `warehouse_humanoid_tco` ends: *"Some orchestration internals are unsampled, so only README-
or source-supported relationships are shown."* That is the generator stating the boundary of its own
evidence. Carrying it forward is the difference between a diagram that documents the repository and a
diagram that looks like it documents the repository. Where the generator declared no caveat, say that
explicitly rather than leaving the clause out.

## 6. Why the colour is removed

Raw gitdiagram output ships seven decorative `classDef` tones — `toneBlue`, `toneAmber`, `toneMint`,
`toneRose`, `toneIndigo`, `toneTeal`, `toneNeutral` — in pastel fills with coloured strokes and coloured
text, one tone per subgraph.

That contradicts the design system on every axis: surface `#E6E6E6`, ink `#282828`, 1 px mid-grey
(`#A0A0A0`) hairlines, no decoration, and orange `#FA6400` spent on exactly one element. More
specifically, the system **has no categorical colour ramp** — `bk-viz` states it as a limitation: *"No
categorical colour ramp. The system defines none on purpose."*

**Subgraph grouping replaces colour as the structural device.** The `subgraph` boxes already express the
grouping the seven tones were duplicating, so removing the tones removes a redundant encoding, not
information. The single orange node is the only categorical signal the diagram gets, and it is spent on
the entry point or on the output the decision is read off — chosen per project, one node, never two.

## 7. Licence and vendoring

| Question | Answer |
|---|---|
| gitdiagram's licence | **MIT**, `Copyright (c) 2024 Ahmed Khaleel` (verified against the repository's `LICENSE`, 2026-09-21). |
| Is any gitdiagram code vendored into this repository? | **No.** Nothing from gitdiagram is copied, bundled, forked or re-implemented here. `blocks/architecture-mermaid.md` is design-system CSS-equivalent styling written for this standard; the Mermaid syntax it uses is Mermaid's, not gitdiagram's. |
| Is any gitdiagram code vendored into a project repository? | **No**, and none is expected to be. |
| What is committed | **Generated output only**: the Mermaid graph describing the author's own repository, restyled, plus the overview paragraph. That output is a description of the author's code, produced on the author's request. |
| Does anything need a NOTICE file? | **No.** MIT's attribution condition attaches to copies of the software; no copy of the software is distributed here. The provenance line under each diagram names the generator regardless, because the standard requires provenance, not because the licence does. |

If any gitdiagram source is ever vendored, this table changes and `docs/LICENSE_POLICY.md` applies:
MIT attribution and a NOTICE entry.

## 8. When not to use it

| Registry value | Use it when | Requires |
|---|---|---|
| `gitdiagram` (default for analytical, application, framework) | the repository's structure is the thing worth showing | commit + date once a diagram is committed |
| `manual` | the useful diagram is a decision flow, a state machine, or a data-flow the code layout does not express | nothing extra; the provenance line still applies |
| `none` | no architecture diagram belongs in this README | `architecture_diagram_reason`, exactly as `demo: static` requires `demo_reason` |

`none` without a reason is a `FAIL` on `technical.architecture`, not a way to opt out quietly.
