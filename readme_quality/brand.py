"""Design-system compliance of a README's presentation: banner, badges, Mermaid (D-051, D-052, D-054).

Pure functions on text and files; the checks (checks.py) report with them and the fixer
(fix.py) applies them. Values come from tokens.json through `design`, never from literals.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import design
from .diagram import ACCENT, CLASSDEFS, CLUSTER, EDGE, INIT, INIT_RE, INK, NODE, SURFACE

DS_VERSION = design.tokens().get("version", "0")
BADGE_LABEL = design.color("light")["ink"].lstrip("#")       # D-054: label ink
BADGE_MESSAGE = design.color("light")["ink-2"].lstrip("#")   # message ink-2
ALLOWED_DIAGRAM_HEX = {c.upper() for c in (SURFACE, NODE, INK, EDGE, CLUSTER, ACCENT)}

MERMAID_FENCE_RE = re.compile(r"^```mermaid[^\n]*\n(.*?)^```", re.M | re.S)
STATIC_BADGE_RE = re.compile(r"(https?://img\.shields\.io/badge/)([^)\s\"'?]+?)-([0-9A-Za-z]+)(?:\.svg)?(\?[^)\s\"']*)?(?=[)\s\"']|$)")
DYNAMIC_SHIELD_RE = re.compile(r"(https?://img\.shields\.io/(?!badge/)[^)\s\"'?]+)(\?[^)\s\"']*)?")
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
CLASSDEF_LINE_RE = re.compile(r"^(\s*)classDef\s+(\S+)\s+(.*)$", re.M)
CLASS_ACCENT_RE = re.compile(r"^[ \t]*class[ \t]+([\w, \t]+?)[ \t]+accent[ \t]*$", re.M)


def _version_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) or (0,)


# ---------------------------------------------------------------- banner
def banner_layout(repo_dir: Path, banner: str) -> dict | None:
    p = (Path(repo_dir) / banner).with_suffix(".layout.json")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def banner_is_current(layout: dict | None) -> bool:
    """A generated banner records the design-system version it was drawn with."""
    if not layout:
        return False
    m = re.search(r"braga ([\d.]+)", str(layout.get("design_system", "")))
    return bool(m) and _version_tuple(m.group(1)) >= _version_tuple(DS_VERSION)


# ---------------------------------------------------------------- badges
def _neutral_query(query: str | None, colour: bool = True) -> str:
    params = [p for p in (query or "").lstrip("?").split("&") if p and not p.lower().startswith(("color=", "labelcolor="))]
    params += ([f"color={BADGE_MESSAGE}"] if colour else []) + [f"labelColor={BADGE_LABEL}"]
    return "?" + "&".join(params)


def recolour_badges(text: str) -> str:
    """Shields badges to the neutrals: label ink, message ink-2 (D-054). CI badge.svg is GitHub's, untouched."""
    text = STATIC_BADGE_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}-{BADGE_MESSAGE}{_neutral_query(m.group(4), colour=False)}", text)
    text = DYNAMIC_SHIELD_RE.sub(lambda m: f"{m.group(1)}{_neutral_query(m.group(2))}", text)
    return text


def badge_problems(text: str) -> list[str]:
    bad = []
    for m in STATIC_BADGE_RE.finditer(text):
        q = (m.group(4) or "").lower()
        if m.group(3).upper() != BADGE_MESSAGE.upper() or f"labelcolor={BADGE_LABEL.lower()}" not in q:
            bad.append(m.group(0))
    for m in DYNAMIC_SHIELD_RE.finditer(text):
        q = (m.group(2) or "").lower()
        if f"color={BADGE_MESSAGE.lower()}" not in q or f"labelcolor={BADGE_LABEL.lower()}" not in q:
            bad.append(m.group(0))
    return bad


# ---------------------------------------------------------------- mermaid
def _restyle_block(body: str) -> str:
    if INIT_RE.search(body):
        body = INIT_RE.sub(lambda _m: INIT, body, count=1)
    else:
        body = INIT + "\n" + body
    node_def, accent_def = CLASSDEFS.split("\n")

    def classdef(m):
        name = m.group(2)
        if name == "node":
            return m.group(1) + node_def
        if name == "accent":
            return m.group(1) + accent_def
        return m.group(0)
    return CLASSDEF_LINE_RE.sub(classdef, body)


def restyle_mermaid_blocks(text: str) -> str:
    """Every Mermaid block on the site's diagram theme; the graph itself is left alone."""
    return MERMAID_FENCE_RE.sub(lambda m: m.group(0).replace(m.group(1), _restyle_block(m.group(1)), 1), text)


def mermaid_problems(text: str) -> list[str]:
    out = []
    for i, m in enumerate(MERMAID_FENCE_RE.finditer(text), 1):
        body = m.group(1)
        init = INIT_RE.search(body)
        if not init or init.group(0).strip() != INIT.strip():
            out.append(f"diagram {i}: no design-system %%{{init}}%% directive (D-052)")
        stray = sorted({h.upper() for h in HEX_RE.findall(INIT_RE.sub("", body))} - ALLOWED_DIAGRAM_HEX)
        if stray:
            out.append(f"diagram {i}: colours outside the design system: {', '.join(stray[:6])}")
        accents = [n.strip() for mm in CLASS_ACCENT_RE.finditer(body) for n in mm.group(1).split(",") if n.strip()]
        if len(accents) > 1:
            out.append(f"diagram {i}: {len(accents)} accent nodes; one per figure (D-036)")
    return out
