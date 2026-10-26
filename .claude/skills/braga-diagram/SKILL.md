---
name: braga-diagram
description: Draw or restyle a diagram (Mermaid flowchart, architecture graph, pipeline, sequence) in the Braga design system v2.1 for a README, a vault note or the portfolio site. Use whenever a diagram is added to or changed in any of Rafael Braga-Kribitz's repositories, when a gitdiagram graph is pasted, or when a README's Mermaid block fails technical.diagram_design.
---

# Braga diagram

A diagram in any of the owner's repositories looks like the diagrams on the portfolio site. The rules
are D-036 and D-052 in braga-portfolio-v2 `design-system/DECISIONS.md`; the values come from its
`tokens.json`. Never type a hex value by hand: the tools below write them.

## Rules

1. **Mermaid as text**, in a ```` ```mermaid ```` fence, never a PNG of a diagram: it stays diffable,
   `click` links work, and the gate can check it.
2. **The site's theme** (D-052): `surface` ground; nodes `surface-2` with a 1px `ink` border and `ink`
   text; edges 1px `ink-2`; clusters `surface` with a `rule-c` border; BKribitz. Square corners.
3. **One accent per figure** (D-036): at most one node in class `accent` (a 1px `accent-01` border):
   the entry point the reader starts from, or the output the decision is read off. Text never takes it.
4. **No colour coding of groups.** Subgraphs carry the grouping; categorical hues are for chart marks only.
5. Labels are sentence case and factual; a node that stands for a file links to it with `click`.
6. A diagram that will sit in a README column (≈ 783px) is measured, not guessed: pick `TD` or `LR`
   by rendering both.

## Procedure

Run from a braga-portfolio-docs checkout (`pip install -r requirements.txt`).

- **Hand-written diagram**: write the graph, then put the theme on it:

  ```bash
  python -m readme_quality theme                       # print the %%{init}%% directive and the two classDefs
  python -m readme_quality theme path/to/README.md     # restyle every Mermaid block in place
  python -m readme_quality theme --check path/to/*.md  # report drift, exit 1
  ```

  Mark the one accent node with `class <node> accent` and every other node `class a,b,c node`.

- **Architecture graph from gitdiagram** (analytical, application, framework READMEs): follow
  `docs/ARCHITECTURE_DIAGRAMS.md`. The restyle is a tool, never a hand edit, because the graph is
  evidence:

  ```bash
  python -m readme_quality diagram --repo ../project --input raw.mmd                 # lists accent candidates
  python -m readme_quality diagram --repo ../project --input raw.mmd --accent node_x --out block.md
  ```

  Add the provenance line from `blocks/architecture-provenance.md` under it.

- **Vault notes and the site**: Mermaid in `vault/` is drawn at build by
  `src/lib/vault/mermaid.mjs` with the same theme; write the graph without a `%%{init}%%` or any
  `classDef` there, and let the build colour it.

## Done means

`python -m readme_quality audit --repo <checkout>` reports `technical.diagram_design` as PASS (or
NOT_APPLICABLE), and `technical.architecture_links` PASS when the diagram has `click` lines.
