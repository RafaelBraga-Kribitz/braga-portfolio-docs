"""Verify the verifier: the gate must pass honest READMEs of every type and fail the right things."""
from __future__ import annotations

import re
from pathlib import Path

from readme_quality import checks as C
from readme_quality.registry import Project
from tests.conftest import PNG_1x1, make_repo, run, statuses
from tests import fixtures as F

COMMON_FILES = {"docs/assets/hero.png": PNG_1x1, "docs/assets/example.png": PNG_1x1, "docs/assets/Author_MDS_Rafael_Braga-Kribitz_kroped.png": PNG_1x1, "run.py": "print('x')\n",
                "requirements.txt": "pandas\n", "data/.keep": "", "reports/.keep": "", "tests/test_x.py": "def test_x(): pass\n",
                "ingest.py": "", "docs/SPEC.md": "# spec\n", "tinycsv.py": ""}


def required_failures(report):
    return [f.id for f in report.failures]


# ---------------------------------------------------------------- happy paths
def test_no_readme_fails(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "empty", None)
    rep = run(repo, Project(name="empty", path=str(repo), type="library", status="Functional"), manifest, registry)
    assert rep.gate == "FAIL" and rep.findings[0].id == "readme.exists"


def test_minimal_readme_fails_on_many_required(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "min", F.MINIMAL, license_text=None)
    rep = run(repo, Project(name="min", path=str(repo), type="library", status="Functional"), manifest, registry)
    ids = required_failures(rep)
    for expected in ("identity.hero", "identity.badges", "identity.problem", "identity.status_line", "meta.license_file", "meta.author", "honesty.limitations"):
        assert expected in ids, expected
    assert "identity.h1" in ids  # underscore slug


def test_analytical_readme_passes(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated", public_data=True)
    rep = run(repo, p, manifest, registry)
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)
    st = statuses(rep)
    assert st["analytical.quantitative"] == "PASS" and st["analytical.uncertainty"] == "PASS" and st["analytical.epistemic"] == "PASS"
    assert st["excellence.audience_personas"] == "PASS_WITH_EXCELLENCE"


def test_library_readme_passes_and_analytical_checks_not_applied(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "tinycsv", F.LIBRARY, COMMON_FILES)
    p = Project(name="tinycsv", path=str(repo), type="library", status="Functional", banner="docs/assets/example.png")
    rep = run(repo, p, manifest, registry)
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)
    ids = {f.id for f in rep.findings}
    assert "analytical.results" not in ids and "technical.architecture" not in ids  # not applicable to libraries -> not even listed


def test_framework_readme_passes(tmp_path, manifest, registry):
    text = F.LIBRARY.replace("# tinycsv", "# tinykit").replace("## What it does", "## The idea")
    repo = make_repo(tmp_path, "tinykit", text, COMMON_FILES)
    p = Project(name="tinykit", path=str(repo), type="framework", status="Functional", banner="docs/assets/example.png")
    rep = run(repo, p, manifest, registry)
    # frameworks need an inline architecture diagram; the library fixture has none
    assert "technical.architecture" in required_failures(rep)
    text2 = text.replace("## Validation", "## Architecture\n\n```mermaid\nflowchart LR\n  A --> B\n```\n\n## Validation")
    (repo / "README.md").write_text(text2, encoding="utf-8")
    rep = run(repo, p, manifest, registry)
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)


def test_interactive_readme_needs_see_it_running(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "app", F.ANALYTICAL, COMMON_FILES)
    p = Project(name="app", path=str(repo), type="analytical", status="Complete", interactive=True, banner="generated", demo="static", demo_reason="static charts are the interface")
    rep = run(repo, p, manifest, registry)
    assert "evidence.see_it_running" in required_failures(rep)
    text = F.ANALYTICAL.replace("## Explore this project", "## See it running\n\n![screenshot](docs/assets/example.png)\n\nNo hosted demo.\n\n## Explore this project")
    (repo / "README.md").write_text(text, encoding="utf-8")
    rep = run(repo, p, manifest, registry)
    st = statuses(rep)
    assert st["evidence.see_it_running"] == "PASS" and st["evidence.demo_motion"] == "NOT_APPLICABLE" and st["evidence.live_demo"] == "PASS"
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)


def test_foundation_readme_passes_without_results(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "tide", F.FOUNDATION, COMMON_FILES)
    p = Project(name="tide", path=str(repo), type="analytical", status="Foundation", incomplete=True, banner="generated")
    rep = run(repo, p, manifest, registry)
    st = statuses(rep)
    assert st["analytical.quantitative"] == "NOT_APPLICABLE" and st["analytical.uncertainty"] == "NOT_APPLICABLE"
    assert st["honesty.no_results_statement"] == "PASS" and st["analytical.results"] == "PASS"
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)


# ---------------------------------------------------------------- excellence preserved
def test_project_specific_sections_are_never_failures(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("## Limitations", "## Weekday residual plots\n\nA custom residual plot per weekday, useful for the owner.\n\n## Limitations")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    st = statuses(rep)
    assert st["excellence.project_specific"] == "PASS_WITH_EXCELLENCE"
    assert "Weekday residual plots" in next(f.message for f in rep.findings if f.id == "excellence.project_specific")
    assert rep.gate == "PASS_WITH_EXCELLENCE"


# ---------------------------------------------------------------- honesty
def test_broken_image_and_link_fail(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("docs/assets/hero.png", "docs/assets/missing.png").replace("[Results](#results)", "[Results](#resultz)")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    ids = required_failures(rep)
    assert "links.images" in ids and "links.internal" in ids and "identity.hero" in ids


def test_hype_and_placeholders_fail(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("## What I would do with production data\n\n- Use per-product counts instead of totals.",
                                "## What I would do with production data\n\n- TBD\n\nThe model is production-ready and state-of-the-art.")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    ids = required_failures(rep)
    assert "honesty.placeholders" in ids and "honesty.hype" in ids


def test_license_section_must_match_file(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL.replace("MIT. See [`LICENSE`](LICENSE).", "Apache-2.0. See [`LICENSE`](LICENSE)."), COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    assert "meta.license_section" in required_failures(rep)


def test_missing_license_is_fail_or_blocked(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL.replace("MIT. See [`LICENSE`](LICENSE).", "No license file is present in this repository."), COMMON_FILES, license_text=None)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    assert "meta.license_file" in required_failures(rep)
    p.license_blocked_reason = "third-party material bundled"
    rep = run(repo, p, manifest, registry)
    assert statuses(rep)["meta.license_file"] == "BLOCKED_HUMAN" and rep.gate == "BLOCKED_HUMAN" or "identity.badges" in required_failures(rep)


def test_status_mismatch_with_registry_fails(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Maintained", banner="generated")
    rep = run(repo, p, manifest, registry)
    ids = required_failures(rep)
    assert "identity.status_line" in ids and "honesty.status_section" in ids


def test_reproduce_commands_must_reference_real_targets(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("python run.py", "make everything")
    repo = make_repo(tmp_path, "study", text, {**COMMON_FILES, "Makefile": "test:\n\tpytest\n"})
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    assert "technical.reproduce" in required_failures(rep)


def test_length_limit(tmp_path, manifest, registry):
    text = F.ANALYTICAL + "\n" + "\n".join(f"filler line {i}" for i in range(500))
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    assert "meta.length" in required_failures(rep)
    p.max_lines = 1000
    p.max_lines_reason = "test"
    assert "meta.length" not in required_failures(run(repo, p, manifest, registry))


def test_manifest_ids_are_stable_and_checks_exist(manifest):
    ids = [r.id for r in manifest.requirements]
    assert len(ids) == len(set(ids))
    for r in manifest.requirements:
        assert r.check in C.CHECKS, r.check
        assert re.match(r"^[a-z]+\.[a-z0-9_]+$", r.id), r.id


def test_registry_matches_ci_checkout_by_remote(tmp_path, manifest):
    import subprocess
    from readme_quality.registry import Author, Registry, project_for_repo
    repo = make_repo(tmp_path, "repo", F.ANALYTICAL, COMMON_FILES)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/Someone/real-name.git"], cwd=repo, check=True)
    reg = Registry(path=tmp_path / "p.yaml", repos_root=tmp_path, author=Author(), status_vocabulary=["Complete"],
                   projects=[Project(name="real-name", path="real-name", github="Someone/real-name", type="analytical", status="Complete", license_blocked_reason="x")])
    p = project_for_repo(reg, repo, {"type": "library"})
    assert p.name == "real-name" and p.license_blocked_reason == "x"
