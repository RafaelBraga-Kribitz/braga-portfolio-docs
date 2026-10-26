<!--
  Architecture diagram — design-system restyling of a gitdiagram graph.

  Procedure and provenance rules: docs/ARCHITECTURE_DIAGRAMS.md
  Provenance line that must follow the diagram: blocks/architecture-provenance.md

  WHAT THE TRANSFORMING AGENT DOES

  1. Generate the graph (gitdiagram has no CLI; see ARCHITECTURE_DIAGRAMS.md §2).
  2. Keep EVERY `subgraph`, node, edge, edge label and `click` line from the generator
     EXACTLY as produced. Do not rename nodes, do not re-group, do not redraw edges,
     do not shorten click URLs to relative paths. The graph is evidence about the
     repository; restyling is presentation. Changing the graph is changing the claim.
  3. Replace ONLY these lines:
       - the `flowchart TD` / `flowchart LR` line: prefix it with the %%{init}%% directive below
       - every `classDef tone*` line: delete, and use the two classDefs below instead
       - every `class …, tone*` line: rewrite so every node is in `node`, and at most ONE
         node is additionally in `accent`
  4. Choose the accent node deliberately: the entry point a reader starts from, or the
     output the decision is read off. One per diagram, never two: one accent per figure
     (D-036), and it is the only colour the diagram carries.
  5. Put the generator's workflow paragraph ABOVE the diagram as prose, and the
     provenance line immediately BELOW it.

  WHY NO COLOUR CODING

  gitdiagram ships seven pastel `classDef` tones and colour-codes the groups with them.
  The Braga design system keeps its categorical hues for chart marks (D-053); a diagram
  is not coloured by group (D-052). Subgraph grouping, not colour, is the structural device: the boxes already carry the grouping the tones were
  duplicating, so dropping the tones loses no information.

  Tokens (tokens.json via readme_quality/design, D-052 — the site's own diagram theme):
  ground surface · nodes surface-2 with a 1px ink border · edges ink-2 · clusters rule-c ·
  one node bordered in accent-01 · BKribitz · no gradients, no shadows, no rounding.
  `python -m readme_quality diagram` writes exactly this; do not copy hex values by hand.
-->

```mermaid
%%{init: {"theme":"base","fontFamily":"BKribitz, system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif","themeVariables":{"background":"#E4E6EA","primaryColor":"#DCDEE2","primaryTextColor":"#26282C","primaryBorderColor":"#26282C","secondaryColor":"#E4E6EA","secondaryTextColor":"#26282C","secondaryBorderColor":"#5A5C61","tertiaryColor":"#E4E6EA","tertiaryTextColor":"#26282C","tertiaryBorderColor":"#C2C4CA","lineColor":"#5A5C61","textColor":"#26282C","mainBkg":"#DCDEE2","nodeBorder":"#26282C","clusterBkg":"#E4E6EA","clusterBorder":"#C2C4CA","edgeLabelBackground":"#E4E6EA","titleColor":"#26282C","fontFamily":"BKribitz, system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif","fontSize":"14px"},"flowchart":{"curve":"linear","htmlLabels":true,"padding":8}}}%%
flowchart TD

%% ---------------------------------------------------------------------------
%% Every subgraph, node, edge and click line below comes from gitdiagram unchanged.
%% ---------------------------------------------------------------------------

subgraph group_example["Group label"]
  node_example["Component<br/>[path/to/file.py]"]
end

node_actor(("External actor"))

node_actor -->|"edge label"| node_example

click node_example "https://github.com/OWNER/REPO/blob/BRANCH/path/to/file.py"

%% ---------------------------------------------------------------------------
%% Design system: one neutral node class, one accent applied to a single node.
%% These two lines replace gitdiagram's seven `classDef tone*` lines.
%% ---------------------------------------------------------------------------

classDef node fill:#DCDEE2,stroke:#26282C,stroke-width:1px,color:#26282C
classDef accent fill:#DCDEE2,stroke:#2F4BE0,stroke-width:1px,color:#26282C

class node_example,node_actor node
class node_actor accent
```
