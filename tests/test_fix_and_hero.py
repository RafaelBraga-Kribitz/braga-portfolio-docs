"""The remediator and the hero generator: safe fixes only, validated banners."""
from __future__ import annotations

import json

from PIL import Image

from readme_quality.fix import Fixer
from readme_quality.hero import HeroLayoutError, HeroSpec, MARGIN, W, H, generate
from readme_quality.registry import Project
from tests.conftest import PNG_1x1, make_repo, run, statuses
from tests import fixtures as F
from tests.test_gate import COMMON_FILES


def test_fixer_adds_license_author_status_badges_hero(tmp_path, manifest, registry):
    text = "# demo_lib\n\nReading ragged CSV files silently corrupts analyses; demo_lib refuses them with a line number.\n\n## What it does\n\n`read(path)` returns the rows of a CSV file keyed by header and raises `RaggedRow` with the line number on any row of the wrong width; it does nothing else.\n\n## Quick start\n\n```python\nimport demo_lib\n```\n\n## Explore this project\n\n| Path | Start here |\n|---|---|\n| Fast path | [Quick start](#quick-start) |\n| Deep path | [What it enforces](#what-it-enforces) |\n\n## What it enforces\n\n| Rule | Where |\n|---|---|\n| width | read() |\n| headers | read() |\n\n## API reference\n\n| Function | Purpose |\n|---|---|\n| `read(path)` | read |\n\n## Validation\n\n`pytest` runs 3 tests.\n\n## Limitations\n\n- one\n- two\n"
    repo = make_repo(tmp_path, "demo_lib", text, {"pyproject.toml": '[project]\nname = "demo_lib"\nlicense = { text = "MIT" }\nrequires-python = ">=3.11"\n', "tests/test_a.py": "", "demo_lib.py": ""}, license_text=None)
    p = Project(name="demo_lib", path=str(repo), type="library", status="Functional", title="demo-lib", descriptor="Refuses ragged CSV rows.", github="x/demo_lib")
    fixer = Fixer(repo, p, registry, manifest)
    rep, changes = fixer.run()
    joined = "\n".join(changes)
    assert "meta.license_file: created LICENSE (MIT" in joined and "declared in pyproject.toml" in joined
    assert (repo / "LICENSE").exists() and (repo / "docs" / "assets" / "hero.png").exists()
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert readme.startswith("# demo-lib\n") and "![" in readme.split("\n## ")[0]
    assert "**Status:** Functional" in readme and "## Status" in readme and "## License" in readme and "## Author" in readme
    assert "badge/status-Functional" in readme and "badge/python" in readme
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), [f.id for f in rep.failures]
    # idempotent
    rep2, changes2 = Fixer(repo, p, registry, manifest).run()
    assert not changes2 and rep2.gate == rep.gate


def test_fixer_never_changes_existing_license(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL.replace("MIT. See [`LICENSE`](LICENSE).", "MIT."), COMMON_FILES, license_text="Apache License, Version 2.0\n")
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    before = (repo / "LICENSE").read_text()
    rep, changes = Fixer(repo, p, registry, manifest).run()
    assert (repo / "LICENSE").read_text() == before
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert "Apache" in readme.split("## License")[1].split("## Author")[0]


def test_fixer_blocks_instead_of_guessing_license(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL.replace("MIT. See [`LICENSE`](LICENSE).", "No license file is present in this repository."), COMMON_FILES, license_text=None)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated", license_blocked_reason="bundled third-party material")
    rep, changes = Fixer(repo, p, registry, manifest).run()
    assert not (repo / "LICENSE").exists()
    assert any("BLOCKED_HUMAN" in c for c in changes)
    assert statuses(rep)["meta.license_file"] == "BLOCKED_HUMAN"


def test_fixer_repairs_moved_image_path(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("(docs/assets/hero.png)", "(img/hero.png)")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep, changes = Fixer(repo, p, registry, manifest).run()
    assert "docs/assets/hero.png" in (repo / "README.md").read_text(encoding="utf-8")
    assert statuses(rep)["links.images"] == "PASS"


def test_hero_layout_is_validated_and_inside_safe_area(tmp_path):
    out = tmp_path / "hero.png"
    rep = generate(HeroSpec(title="A Very Long Project Title That Must Wrap Onto Several Lines Without Overflowing",
                            descriptor="A descriptor with punctuation: colons; semicolons (and brackets) / slashes that the trial font lacks, so the fallback must fill them.",
                            kind="Analytical project", status="In development",
                            facts=[("License", "MIT"), ("Runtime", "Python 3.12"), ("CI", "GitHub Actions"), ("Repo", "github.com/x/y")]), out, report_path=tmp_path / "hero.json")
    assert rep["validated"] and out.exists()
    img = Image.open(out)
    assert img.size == (W, H)
    for name, b in rep["blocks"].items():
        x0, y0, x1, y1 = b["bbox"]
        assert x0 >= MARGIN - 2 and y0 >= MARGIN - 2 and x1 <= W - MARGIN + 2 and y1 <= H - MARGIN + 2, name
    assert len(rep["blocks"]["title"]["lines"]) <= 3
    data = json.loads((tmp_path / "hero.json").read_text(encoding="utf-8"))
    assert "pixel-scan" in data["guardrails"]


def test_hero_rejects_impossible_layout(tmp_path):
    try:
        generate(HeroSpec(title="Supercalifragilisticexpialidocious" * 6, descriptor=""), tmp_path / "h.png")
    except HeroLayoutError:
        return
    raise AssertionError("an unwrappable title must raise HeroLayoutError")


def test_hero_tagline_renders_as_its_own_block(tmp_path):
    out = tmp_path / "hero.png"
    rep = generate(HeroSpec(title="DSX", tagline="Declare. Substantiate. eXplain.",
                            descriptor="Data Science, eXamined: deterministic gates that block leakage.",
                            kind="Framework", status="Maintained",
                            facts=[("License", "MIT")]), out, report_path=tmp_path / "hero.json")
    blocks = rep["blocks"]
    assert blocks["tagline"]["lines"] == ["DECLARE. SUBSTANTIATE. EXPLAIN."]
    # order on the canvas: title, then tagline, then descriptor
    assert blocks["title"]["bbox"][3] <= blocks["tagline"]["bbox"][1]
    assert blocks["tagline"]["bbox"][3] <= blocks["descriptor"]["bbox"][1]
    assert out.exists()


def test_hero_keeps_a_long_tagline_on_one_line(tmp_path):
    """The guardrail shrinks the type until the motto fits; it never wraps to two lines."""
    long_motto = "Declare the analysis before the data is touched and substantiate every claim with code"
    rep = generate(HeroSpec(title="DSX", tagline=long_motto, descriptor="x"), tmp_path / "h.png")
    assert len(rep["blocks"]["tagline"]["lines"]) == 1


def test_hero_rejects_an_unwrappable_tagline(tmp_path):
    try:
        generate(HeroSpec(title="DSX", tagline="Substantiate" * 20, descriptor="x"), tmp_path / "h2.png")
    except HeroLayoutError:
        return
    raise AssertionError("a tagline that cannot fit on one line must raise HeroLayoutError")
