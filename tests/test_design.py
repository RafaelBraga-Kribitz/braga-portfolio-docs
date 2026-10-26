"""Design system v2.1 (braga-portfolio-v2 design-system/DECISIONS.md §3): banner, badges, diagrams."""
import json
import re
from pathlib import Path

import pytest
from PIL import Image

from readme_quality import brand, design
from readme_quality.hero import HeroSpec, STATUS_STATE, generate, palette

ROOT = Path(__file__).resolve().parent.parent


def test_vendored_tokens_match_the_design_system_checkout():
    """The snapshot may not drift from tokens.json when a braga-portfolio-v2 checkout is at hand."""
    root = design.ds_root()
    if root is None:
        pytest.skip("no braga-portfolio-v2 checkout next to this one (set BRAGA_DS to check)")
    live = json.loads((root / "design-system" / "tokens.json").read_text(encoding="utf-8"))
    vendored = json.loads(design.VENDORED_TOKENS.read_text(encoding="utf-8"))
    assert vendored == live, "run `make design-sync`"


def test_no_v1_palette_or_typeface_left_in_the_code():
    for f in (ROOT / "readme_quality").glob("*.py"):
        text = f.read_text(encoding="utf-8")
        for v1 in ("#FA6400", "#E6E6E6", "#282828", "#5B7FFF", "Sohne-Fett"):
            assert v1 not in text, f"{f.name} still carries {v1}"


def test_banner_carries_no_accent_and_records_its_system(tmp_path):
    out = tmp_path / "hero.png"
    rep = generate(HeroSpec(title="Fictional Demand Study", descriptor="Weekly demand forecast for a fictional retailer.",
                            kind="Analytical project", status="Complete", facts=[("License", "MIT")]),
                   out, report_path=out.with_suffix(".layout.json"))
    assert rep["status_state"] == "complete"
    assert brand.banner_is_current(rep)
    accent = tuple(int(palette("light")["accent"][i:i + 2], 16) for i in (1, 3, 5))
    colours = {c for _, c in Image.open(out).convert("RGB").getcolors(1 << 20)}
    assert accent not in colours
    assert tuple(int(palette("light")["surface"][i:i + 2], 16) for i in (1, 3, 5)) in colours


def test_banner_from_an_older_system_is_not_current():
    assert not brand.banner_is_current({"fonts": "Söhne from /x"})
    assert not brand.banner_is_current({"design_system": "braga 2.0.0 (D-051)"})
    assert not brand.banner_is_current(None)


def test_every_readme_status_maps_to_a_square():
    vocabulary = ["Prototype", "Foundation", "In development", "Functional", "Complete", "Maintained", "Archived"]
    assert all(s.lower() in STATUS_STATE for s in vocabulary)
    assert {STATUS_STATE[s.lower()] for s in vocabulary} <= {"complete", "functional", "under-revision", "in-build", "archived"}


def test_badges_take_the_neutrals_and_the_fix_is_idempotent():
    text = ("[![Status](https://img.shields.io/badge/status-Foundation-orange)](#status) "
            "[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) "
            "[![CI](https://github.com/o/r/actions/workflows/ci.yml/badge.svg)](x)")
    assert len(brand.badge_problems(text)) == 2
    fixed = brand.recolour_badges(text)
    assert brand.badge_problems(fixed) == []
    assert brand.recolour_badges(fixed) == fixed
    assert "actions/workflows/ci.yml/badge.svg" in fixed          # GitHub's badge is not ours to recolour
    assert "-orange" not in fixed and "-yellow" not in fixed


def test_mermaid_blocks_take_the_site_theme_and_keep_the_graph():
    text = "# T\n\n```mermaid\nflowchart TD\n  a[A] --> b[B]\nclassDef accent fill:#E6E6E6,stroke:#FA6400\nclass a accent\n```\n"
    assert brand.mermaid_problems(text)
    fixed = brand.restyle_mermaid_blocks(text)
    assert brand.mermaid_problems(fixed) == []
    assert "a[A] --> b[B]" in fixed and "class a accent" in fixed
    assert brand.restyle_mermaid_blocks(fixed) == fixed


def test_two_accent_nodes_are_reported():
    from readme_quality.diagram import CLASSDEFS, INIT
    text = f"```mermaid\n{INIT}\nflowchart TD\n  a --> b\n{CLASSDEFS}\nclass a,b accent\n```\n"
    assert any("2 accent nodes" in p for p in brand.mermaid_problems(text))
