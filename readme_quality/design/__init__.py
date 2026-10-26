"""The Braga design system as this package sees it: tokens.json and the BKribitz faces.

The source of truth is `design-system/tokens.json` in braga-portfolio-v2 (DECISIONS.md §3).
This folder vendors a snapshot of it and the four faces the banner uses (SIL OFL 1.1, licence
and notice alongside), so the gate runs offline and in CI. Resolution order:

  1. $BRAGA_DS            a braga-portfolio-v2 checkout (or its design-system/ folder)
  2. ../braga-portfolio-v2 next to this checkout
  3. the vendored snapshot

`make design-sync` refreshes the snapshot; tests/test_design.py fails when a sibling checkout
is present and the snapshot has drifted from it.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDORED_TOKENS = HERE / "tokens.json"
VENDORED_FONTS = HERE / "fonts"

FACES = {  # role -> file stem (public/fonts in braga-portfolio-v2)
    "wordmark": "BKribitz-800",
    "display": "BKribitz-700",
    "body": "BKribitz-400",
    "mono": "BKribitzMono-400",
}


def ds_root() -> Path | None:
    """A braga-portfolio-v2 checkout, when one can be found."""
    cands = [os.environ.get("BRAGA_DS"), HERE.parents[2] / "braga-portfolio-v2", HERE.parents[3] / "braga-portfolio-v2"]
    for c in cands:
        if not c:
            continue
        p = Path(c)
        if p.name == "design-system":
            p = p.parent
        if (p / "design-system" / "tokens.json").is_file():
            return p
    return None


@lru_cache(maxsize=1)
def tokens() -> dict:
    root = ds_root()
    path = root / "design-system" / "tokens.json" if root else VENDORED_TOKENS
    return json.loads(path.read_text(encoding="utf-8"))


def color(mode: str = "light") -> dict:
    return tokens()["color"][mode]


def font_path(role: str, fonts_dir: str | Path | None = None) -> str | None:
    """The face for a role: an explicit folder first, then the checkout, then the vendored copy."""
    stem = FACES[role]
    root = ds_root()
    for d in (fonts_dir, os.environ.get("BK_FONTS"), root / "public" / "fonts" if root else None, VENDORED_FONTS):
        if not d:
            continue
        for ext in (".woff2", ".ttf", ".otf"):
            p = Path(d) / f"{stem}{ext}"
            if p.is_file():
                return str(p)
    return None
