"""Restyle a gitdiagram Mermaid graph into the Braga-Kribitz design system.

The transformation blocks/architecture-mermaid.md describes as instructions for an agent,
done as code instead, because it is fully deterministic and because an agent doing it by
hand is an agent that can silently change the graph. The graph is evidence about the
repository; only the presentation is ours to change.

Kept byte-for-byte: every `subgraph`, node, edge, edge label and `click` line.
Replaced: the `%%{init}%%` directive, `classDef tone*`, and the `class … tone*` lines.

    python -m readme_quality diagram --repo ../some-project --input raw.mmd --accent node_cli
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .parse import GITHUB_BLOB_RE, MERMAID_CLICK_RE, is_external

# Design-system tokens (readme_quality/hero.py): surface, ink, hairline, the one accent.
SURFACE = "#E6E6E6"
INK = "#282828"
HAIRLINE = "#A0A0A0"
ACCENT = "#FA6400"
MONO = "Söhne Mono, ui-monospace, SFMono-Regular, Menlo, monospace"

# `fontFamily` must sit at the TOP LEVEL of the init config. Mermaid 11 ignores it under
# `themeVariables` — verified by rendering both: themeVariables-only falls back to the page's
# font, top-level applies. It is set in both places here because the two cover different
# surfaces (node labels vs cluster titles) and neither placement is harmful.
INIT = f"""%%{{init: {{
  "theme": "base",
  "fontFamily": "{MONO}",
  "themeVariables": {{
    "background": "{SURFACE}",
    "primaryColor": "{SURFACE}",
    "primaryTextColor": "{INK}",
    "primaryBorderColor": "{HAIRLINE}",
    "secondaryColor": "{SURFACE}",
    "secondaryTextColor": "{INK}",
    "secondaryBorderColor": "{HAIRLINE}",
    "tertiaryColor": "{SURFACE}",
    "tertiaryTextColor": "{INK}",
    "tertiaryBorderColor": "{HAIRLINE}",
    "lineColor": "{HAIRLINE}",
    "textColor": "{INK}",
    "mainBkg": "{SURFACE}",
    "nodeBorder": "{HAIRLINE}",
    "clusterBkg": "{SURFACE}",
    "clusterBorder": "{HAIRLINE}",
    "edgeLabelBackground": "{SURFACE}",
    "titleColor": "{INK}",
    "fontFamily": "{MONO}",
    "fontSize": "13px"
  }},
  "flowchart": {{ "curve": "linear", "htmlLabels": true, "padding": 8 }}
}}}}%%"""

CLASSDEFS = (f"classDef node fill:{SURFACE},stroke:{HAIRLINE},stroke-width:1px,color:{INK}\n"
             f"classDef accent fill:{SURFACE},stroke:{ACCENT},stroke-width:1px,color:{INK}")

FLOWCHART_RE = re.compile(r"^\s*(flowchart|graph)\s+(TD|TB|LR|RL|BT)\s*$", re.M)
CLASSDEF_RE = re.compile(r"^\s*classDef\s+\S+.*$", re.M)
CLASS_RE = re.compile(r"^\s*class\s+([\w,\s]+?)\s+(\w+)\s*$", re.M)
INIT_RE = re.compile(r"^\s*%%\{init:.*?\}%%\s*$", re.M | re.S)
NODE_DECL_RE = re.compile(r"^\s*(\w+)\s*(?:\[\(|\(\(|\{\{|\[|\(|>|\{)", re.M)
EDGE_RE = re.compile(r"^\s*(\w+)\s*(?:-\.?-+>|==+>|-{2,}|\.-+>)(?:\|[^|]*\|)?\s*(\w+)", re.M)


@dataclass
class Graph:
    raw: str
    direction: str = "TD"
    nodes: list[str] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)
    clicks: list[tuple[str, str]] = field(default_factory=list)
    body: str = ""            # everything except init / classDef / class lines

    @property
    def entry_points(self) -> list[str]:
        targets = {b for _, b in self.edges}
        return [n for n in self.nodes if n not in targets]

    @property
    def outputs(self) -> list[str]:
        sources = {a for a, _ in self.edges}
        return [n for n in self.nodes if n not in sources]

    @property
    def unclicked(self) -> list[str]:
        clicked = {n for n, _ in self.clicks}
        return [n for n in self.nodes if n not in clicked]


def parse_graph(raw: str) -> Graph:
    raw = raw.replace("\r\n", "\n").strip("\n")
    if raw.lstrip().startswith("```"):                 # a fenced block was pasted
        raw = re.sub(r"^\s*```\w*\n|\n\s*```\s*$", "", raw)
    g = Graph(raw=raw)
    m = FLOWCHART_RE.search(raw)
    g.direction = m.group(2) if m else "TD"

    body = INIT_RE.sub("", raw)
    body = CLASSDEF_RE.sub("", body)
    body = CLASS_RE.sub("", body)
    body = FLOWCHART_RE.sub("", body, count=1)
    g.body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")

    seen: set[str] = set()
    for line in g.body.split("\n"):
        s = line.strip()
        if s.startswith(("subgraph", "end", "click", "%%")) or not s:
            continue
        for mm in NODE_DECL_RE.finditer(line):
            if mm.group(1) not in seen and mm.group(1) not in ("subgraph", "end"):
                seen.add(mm.group(1))
                g.nodes.append(mm.group(1))
    for mm in EDGE_RE.finditer(g.body):
        g.edges.append((mm.group(1), mm.group(2)))
        for n in (mm.group(1), mm.group(2)):
            if n not in seen:
                seen.add(n)
                g.nodes.append(n)
    for mm in MERMAID_CLICK_RE.finditer(g.body):
        g.clicks.append((mm.group(1), mm.group(2)))
    return g


DIRECTIONS = ("TD", "TB", "LR", "RL", "BT")


def restyle(raw: str, accent: str, direction: str = "") -> str:
    """The raw graph with the design-system directive and exactly one accent node.

    `direction` overrides the generator's `flowchart TD`. It changes layout only — no node,
    edge or click line moves — and it is the one knob that decides whether the graph is legible
    in GitHub's README column, which is 783 px wide at a 1240 px viewport and 838 px at its
    widest. Which direction is narrower depends on the graph's shape, not on a rule of thumb:
    TD stacks the flow vertically but lays sibling subgraphs out side by side, so a graph with
    four parallel subgraphs is *wider* in TD than in LR. Render it and measure.
    """
    g = parse_graph(raw)
    if accent not in g.nodes:
        raise ValueError(f"accent node {accent!r} is not in the graph; nodes: {', '.join(g.nodes)}")
    if direction and direction.upper() not in DIRECTIONS:
        raise ValueError(f"direction {direction!r} is not one of {', '.join(DIRECTIONS)}")
    others = [n for n in g.nodes if n != accent]
    lines = [INIT, f"flowchart {(direction or g.direction).upper()}", "", g.body, "", CLASSDEFS]
    if others:
        lines.append("class " + ",".join(others) + " node")
    lines.append(f"class {accent} accent")
    return "\n".join(lines) + "\n"


def verify_clicks(g: Graph, repo_dir: Path, github: str = "") -> dict:
    """Same rule as the technical.architecture_links check, usable before anything is committed."""
    repo_dir = Path(repo_dir)
    out = {"total": len(g.clicks), "missing": [], "wrong_repo": [], "case_only": [], "external": [], "empty_on_github": [], "files": 0, "dirs": 0}
    for node, target in g.clicks:
        m = GITHUB_BLOB_RE.match(target.strip())
        if not m:
            # same rule as the technical.architecture_links check: an off-GitHub target is
            # reported, not failed. The gate cannot reach the network; a human verifies it.
            if is_external(target):
                out["external"].append(f"{node} -> {target}")
            else:
                out["missing"].append(f"{node} -> unresolvable: {target}")
            continue
        slug = f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
        path = m.group(3).split("#", 1)[0].split("?", 1)[0]   # strip a `#L92` line anchor
        if github and slug.lower() != github.lower():
            out["wrong_repo"].append(f"{node} -> {slug}")
            continue
        if github and slug != github:
            out["case_only"].append(slug)
        p = repo_dir / path
        if not p.exists():
            out["missing"].append(f"{node} -> {path}")
        elif p.is_dir():
            out["dirs"] += 1
            if _tracked_files(repo_dir, path) <= 1 and _only_placeholder(repo_dir, path):
                out["empty_on_github"].append(f"{node} -> {path}")
        else:
            out["files"] += 1
    return out


def _tracked_files(repo_dir: Path, path: str) -> int:
    """How many files git tracks under a directory (0 when git is unavailable)."""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", str(repo_dir), "ls-files", "--", path],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return 1        # cannot tell; do not warn
    return len([l for l in r.stdout.splitlines() if l.strip()]) if r.returncode == 0 else 1


def _only_placeholder(repo_dir: Path, path: str) -> bool:
    """True when the only tracked file is a .gitkeep-style placeholder.

    A directory whose contents are DVC-tracked or gitignored resolves on disk and the GitHub
    link works, but a reader who clicks it lands on an empty folder. The gate cannot see this
    (it tests the working tree); the author can, before the diagram is committed.
    """
    import subprocess
    try:
        r = subprocess.run(["git", "-C", str(repo_dir), "ls-files", "--", path],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return False
    names = [Path(l).name.lower() for l in r.stdout.splitlines() if l.strip()]
    return bool(names) and all(n in (".gitkeep", ".keep", ".gitignore", "readme.md") for n in names)
