"""Verify the verifier: the gate must pass honest READMEs of every type and fail the right things."""
from __future__ import annotations

import re
from pathlib import Path

from readme_quality import checks as C
from readme_quality.parse import parse
from readme_quality.registry import Project
from tests.conftest import PNG_1x1, make_repo, run, statuses
from tests import fixtures as F

COMMON_FILES = {"docs/assets/hero.png": PNG_1x1, "docs/assets/example.png": PNG_1x1, "docs/assets/Author_MDS_Rafael_Braga-Kribitz_kroped.png": PNG_1x1, "run.py": "print('x')\n",
                "requirements.txt": "pandas\n", "data/.keep": "", "reports/.keep": "", "tests/test_x.py": "def test_x(): pass\n",
                "ingest.py": "", "docs/SPEC.md": "# spec\n", "tinycsv.py": ""}

# For the communication.* family: bk-viz declared, three figures shown in the README and
# twelve on disk, so `min(3, floor(0.25 * 12))` is exactly three.
PYPROJECT_WITH_THEME = '[project]\nname = "study"\ndependencies = [\n    "pandas>=2.2",\n    "bk-viz",\n]\n\n[tool.uv.sources]\nbk-viz = { git = "https://github.com/RafaelBraga-Kribitz/bk-viz" }\n'
COMM_FILES = {**COMMON_FILES, "pyproject.toml": PYPROJECT_WITH_THEME,
              **{f"reports/f{i:02d}_chart.png": PNG_1x1 for i in range(1, 13)},
              "reports/f01_holdout_error.png": PNG_1x1, "reports/f02_waste_band.png": PNG_1x1, "reports/f03_residuals.png": PNG_1x1}


def comm_project(repo, **kw):
    kw.setdefault("descriptor", "Weekly order forecasting for a small bakery, validated on a 12-week holdout.")
    return Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated", **kw)


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


# ---------------------------------------------------------------- v1.3: rendered length
def test_length_counts_rendered_lines_not_file_lines(tmp_path, manifest, registry):
    """A Mermaid block renders as one figure and a claim comment renders as nothing."""
    mermaid = "```mermaid\nflowchart TD\n" + "\n".join(f"  n{i} --> n{i + 1}" for i in range(80)) + "\n```"
    comment = "<!-- claim: " + "reports/ssot.json::row[0].value [eur]; " * 20 + "-->"
    text = F.ANALYTICAL.replace("## Limitations", f"## Appendix\n\n{mermaid}\n\n{comment}\n\n## Limitations")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)

    base = parse(F.ANALYTICAL)
    grown = parse(text)
    assert len(grown.lines) > len(base.lines) + 80          # the file really did grow by the diagram
    assert grown.rendered_line_count == base.rendered_line_count + 1   # only the `## Appendix` heading renders
    assert "meta.length" not in required_failures(rep)
    assert statuses(rep)["meta.length"] == "PASS"


def test_length_excludes_badge_only_lines_and_counts_content(manifest):
    rd = parse(
        "# T\n"
        "\n"
        "[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)\n"
        "[![Status](https://img.shields.io/badge/status-Complete-green)](#status)\n"
        "\n"
        "Real prose that a reader reads.\n"
        "\n"
        "| a | b |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
    )
    assert rd.rendered_line_count == 5   # H1, prose, three table lines; the two badge lines do not count


def test_length_and_length_total_are_separate_ceilings(tmp_path, manifest, registry):
    text = F.ANALYTICAL + "\n" + "\n".join(f"<!-- filler {i} -->" for i in range(1200))
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    st = statuses(run(repo, p, manifest, registry))
    assert st["meta.length"] == "PASS"          # comments render as nothing
    assert st["meta.length_total"] == "WARN"    # but the file is 1200 lines longer


def test_length_override_without_a_reason_is_ignored(tmp_path, manifest, registry):
    text = F.ANALYTICAL + "\n" + "\n".join(f"filler line {i}" for i in range(500))
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated", max_lines=1000)
    rep = run(repo, p, manifest, registry)
    assert "meta.length" in required_failures(rep)
    assert "no max_lines_reason" in next(f.message for f in rep.findings if f.id == "meta.length")
    p.max_lines_reason = "the appendix is the artifact"
    assert "meta.length" not in required_failures(run(repo, p, manifest, registry))


def test_length_total_not_applicable_never_happens_but_override_works(tmp_path, manifest, registry):
    text = F.ANALYTICAL + "\n" + "\n".join(f"<!-- filler {i} -->" for i in range(1200))
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated",
                max_lines_total=2000, max_lines_total_reason="the claim comments are the audit trail")
    assert statuses(run(repo, p, manifest, registry))["meta.length_total"] == "PASS"


# ---------------------------------------------------------------- v1.3: architecture links
def arch_project(repo):
    return Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated",
                   github="RafaelBraga-Kribitz/study")


def test_architecture_links_pass_and_report_owner_case(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, COMM_FILES)
    rep = run(repo, arch_project(repo), manifest, registry)
    f = next(x for x in rep.findings if x.id == "technical.architecture_links")
    assert f.status == "PASS", f.message
    assert "case mismatch" in f.message   # gitdiagram lowercases the owner; reported, not failed


def test_architecture_links_fail_on_a_path_that_does_not_exist(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace("/blob/main/run.py", "/blob/main/src/moved_away.py")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    rep = run(repo, arch_project(repo), manifest, registry)
    f = next(x for x in rep.findings if x.id == "technical.architecture_links")
    assert f.status == "WARN" and "do not exist" in f.message      # recommended in v1.3
    assert "technical.architecture_links" not in required_failures(rep)


def test_architecture_links_fail_when_the_link_points_at_another_repository(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace("github.com/rafaelbraga-kribitz/study/blob", "github.com/someone-else/other/blob")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    rep = run(repo, arch_project(repo), manifest, registry)
    assert "another repository" in next(x.message for x in rep.findings if x.id == "technical.architecture_links")


def test_architecture_links_accept_line_anchors_and_external_targets(tmp_path, manifest, registry):
    """`…/run.py#L92` is a normal GitHub link, and a non-GitHub target is reported, not failed."""
    text = F.COMMUNICATION.replace(
        'click node_ingest "https://github.com/rafaelbraga-kribitz/study/blob/main/run.py"',
        'click node_ingest "https://github.com/rafaelbraga-kribitz/study/blob/main/run.py#L12"\n'
        '  click node_analyst "https://huggingface.co/unitreerobotics"')
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    f = next(x for x in run(repo, arch_project(repo), manifest, registry).findings
             if x.id == "technical.architecture_links")
    assert f.status == "PASS", f.message
    assert "1 non-GitHub link(s) not checked" in f.message


def test_architecture_links_not_applicable_without_click_lines(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)   # plain mermaid, no click lines
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    assert statuses(run(repo, p, manifest, registry))["technical.architecture_links"] == "NOT_APPLICABLE"


def test_architecture_none_needs_a_reason(tmp_path, manifest, registry):
    text = F.ANALYTICAL.replace("## Architecture\n\n```mermaid\nflowchart LR\n    A[POS export] --> B[features] --> C[seasonal model] --> D[holdout scoring] --> E[decision]\n```\n\n", "")
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated",
                architecture_diagram="none")
    rep = run(repo, p, manifest, registry)
    assert "technical.architecture" in required_failures(rep)
    p.architecture_diagram_reason = "the pipeline is four sequential scripts; the Reproduce block is the diagram"
    assert statuses(run(repo, p, manifest, registry))["technical.architecture"] == "NOT_APPLICABLE"


# ---------------------------------------------------------------- v1.3: communication family
def test_communication_family_passes_on_a_well_communicated_readme(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, COMM_FILES)
    rep = run(repo, comm_project(repo), manifest, registry)
    st = statuses(rep)
    for rid in ("communication.alt_text", "communication.alt_distinct", "communication.chart_theme",
                "communication.figure_coverage", "communication.chart_caption", "communication.message_heading"):
        assert st[rid] == "PASS", (rid, next(f.message for f in rep.findings if f.id == rid))
    assert rep.gate in ("PASS", "PASS_WITH_EXCELLENCE"), required_failures(rep)


def test_alt_text_fails_on_an_empty_alt_and_ignores_badges(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace("![Residuals by weekday, showing the Saturday over-forecast the model does not remove]", "![]")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    rep = run(repo, comm_project(repo), manifest, registry)
    f = next(x for x in rep.findings if x.id == "communication.alt_text")
    assert f.status == "WARN" and "1 of 3" in f.message         # the two badge shields are not counted
    assert "communication.alt_text" not in required_failures(rep)


def test_alt_text_not_applicable_without_figures(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)   # banner only
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    assert statuses(run(repo, p, manifest, registry))["communication.alt_text"] == "NOT_APPLICABLE"


def test_alt_distinct_catches_the_descriptor_and_the_banner_copy(tmp_path, manifest, registry):
    descriptor = "Weekly order forecasting for a small bakery, validated on a 12-week holdout."
    text = F.COMMUNICATION.replace(
        "![Weekly mean absolute percentage error of both models over the 12-week holdout, seasonal model lower in 10 of 12 weeks]",
        f"![{descriptor}]")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    assert "registry descriptor" in next(x.message for x in run(repo, comm_project(repo), manifest, registry).findings
                                         if x.id == "communication.alt_distinct")

    text = F.COMMUNICATION.replace(
        "![Weekly mean absolute percentage error of both models over the 12-week holdout, seasonal model lower in 10 of 12 weeks]",
        "![Generated banner for the Fictional Demand Study]")
    repo2 = make_repo(tmp_path, "study2", text, COMM_FILES)
    assert "copied from the banner" in next(x.message for x in run(repo2, comm_project(repo2), manifest, registry).findings
                                            if x.id == "communication.alt_distinct")


def test_alt_distinct_catches_two_figures_with_the_same_alt(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace(
        "![Residuals by weekday, showing the Saturday over-forecast the model does not remove]",
        "![Flour waste per month under each model, with the 10th to 90th percentile band]")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    rep = run(repo, comm_project(repo), manifest, registry)
    f = next(x for x in rep.findings if x.id == "communication.alt_distinct")
    assert f.status == "WARN" and "identical to the figure" in f.message


def test_chart_theme_fails_without_bk_viz_and_is_na_for_bk_viz_itself(tmp_path, manifest, registry):
    files = {**COMM_FILES, "pyproject.toml": '[project]\nname = "study"\ndependencies = ["matplotlib>=3.8"]\n'}
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, files)
    rep = run(repo, comm_project(repo), manifest, registry)
    assert statuses(rep)["communication.chart_theme"] == "WARN"
    assert "communication.chart_theme" not in required_failures(rep)

    theme = Project(name="bk-viz", path=str(repo), type="library", status="Functional", banner="generated")
    assert statuses(run(repo, theme, manifest, registry))["communication.chart_theme"] == "NOT_APPLICABLE"


def test_chart_theme_accepts_the_git_dependency_form(tmp_path, manifest, registry):
    """austrian-mmm-budget-optimizer declares bk-viz through [tool.uv.sources]; that must count."""
    files = {**COMM_FILES, "pyproject.toml": '[project]\nname = "study"\ndependencies = ["matplotlib>=3.8"]\n\n'
                                             '[tool.uv.sources]\nbk-viz = { git = "https://github.com/RafaelBraga-Kribitz/bk-viz" }\n'}
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, files)
    assert statuses(run(repo, comm_project(repo), manifest, registry))["communication.chart_theme"] == "PASS"


def test_figure_coverage_reports_the_ratio(tmp_path, manifest, registry):
    text = F.COMMUNICATION
    for alt, path in (("Flour waste per month under each model, with the 10th to 90th percentile band", "reports/f02_waste_band.png"),
                      ("Residuals by weekday, showing the Saturday over-forecast the model does not remove", "reports/f03_residuals.png")):
        text = text.replace(f"![{alt}]({path})\n", "")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    f = next(x for x in run(repo, comm_project(repo), manifest, registry).findings if x.id == "communication.figure_coverage")
    assert f.status == "WARN" and "1 of 15 figures in reports/ shown in the README (need 3)" in f.message


def test_figure_coverage_not_applicable_without_figures_on_disk(tmp_path, manifest, registry):
    files = {k: v for k, v in COMM_FILES.items() if not k.startswith(("reports/f", "docs/assets/"))}
    files["docs/assets/Author_MDS_Rafael_Braga-Kribitz_kroped.png"] = PNG_1x1
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, files)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    assert statuses(run(repo, p, manifest, registry))["communication.figure_coverage"] == "NOT_APPLICABLE"


def test_chart_caption_fails_when_missing_or_when_it_repeats_the_alt(tmp_path, manifest, registry):
    caption = "*The seasonal model is below the naive baseline in ten of the twelve holdout weeks; the two crossings are both in the Christmas fortnight.*"
    repo = make_repo(tmp_path, "study", F.COMMUNICATION.replace(caption + "\n\n", ""), COMM_FILES)
    f = next(x for x in run(repo, comm_project(repo), manifest, registry).findings if x.id == "communication.chart_caption")
    assert f.status == "WARN" and "no caption within two lines" in f.message

    alt = "Weekly mean absolute percentage error of both models over the 12-week holdout, seasonal model lower in 10 of 12 weeks"
    repo2 = make_repo(tmp_path, "study2", F.COMMUNICATION.replace(caption, f"*{alt}*"), COMM_FILES)
    assert "repeats its alt text" in next(x.message for x in run(repo2, comm_project(repo2), manifest, registry).findings
                                          if x.id == "communication.chart_caption")


def test_chart_caption_not_applicable_without_a_chart(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    assert statuses(run(repo, p, manifest, registry))["communication.chart_caption"] == "NOT_APPLICABLE"


def test_message_heading_needs_a_numeral_and_is_na_for_incomplete(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace("### The seasonal model halves forecast error, 18.0 to 9.5 percent", "### Model comparison")
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    f = next(x for x in run(repo, comm_project(repo), manifest, registry).findings if x.id == "communication.message_heading")
    assert f.status == "WARN" and "carries a number" in f.message

    repo2 = make_repo(tmp_path, "tide", F.FOUNDATION, COMMON_FILES)
    p = Project(name="tide", path=str(repo2), type="analytical", status="Foundation", incomplete=True, banner="generated")
    assert statuses(run(repo2, p, manifest, registry))["communication.message_heading"] == "NOT_APPLICABLE"


# ---------------------------------------------------------------- v1.3: the comparator
def test_quantitative_needs_a_comparator_not_just_two_numbers(tmp_path, manifest, registry):
    """Before v1.3 this passed on two bare numbers: '€45k' written twice satisfied it."""
    # every section the check reads (Decision summary and Results are both RESULTS_ALIASES)
    summary = ("## Decision summary\n\nThe seasonal model is the one to run; the decision rule is stated "
               "in the results section and should be revisited when the next season closes.\n")
    bare = ("## Results\n\nThe five-year total cost is €45k. Capital expenditure is €12k and "
            "operating expenditure is €33k over the period.\n\nUncertainty: 90 percent interval.\n")
    text = re.sub(r"## Decision summary\n.*?\n## Explore", summary + "\n## Explore", F.ANALYTICAL, flags=re.S)
    text = re.sub(r"## Results\n.*?\n## Method", bare + "\n## Method", text, flags=re.S)
    repo = make_repo(tmp_path, "study", text, COMMON_FILES)
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    rep = run(repo, p, manifest, registry)
    assert "analytical.quantitative" in required_failures(rep)
    assert "no comparator" in next(f.message for f in rep.findings if f.id == "analytical.quantitative")

    (repo / "README.md").write_text(
        text.replace("The five-year total cost is €45k.", "The five-year total cost is €45k, against €61k for the baseline."),
        encoding="utf-8")
    assert "analytical.quantitative" not in required_failures(run(repo, p, manifest, registry))


def test_quantitative_accepts_every_comparator_form_the_standard_lists(manifest):
    for phrase in ("9.5 percent vs 18.0 percent", "9.5 percent versus 18.0", "compared to the 18.0 percent baseline",
                   "measured against the naive model", "relative to 2024", "Δ of 8.5 points", "a delta of 8.5 points",
                   "+3.7 pp on the margin", "-28 % against 2020", "Styria is above its 2020 level",
                   "below the breakeven ROAS", "2x lower than the baseline", "the lowest cost scenario",
                   "the highest coverage", "the human-only comparator", "against the benchmark",
                   "cut error from 18.0 percent to 9.5 percent"):
        assert C.COMPARATOR_RE.search(phrase), phrase
    for phrase in ("the five-year total cost is €45k", "coverage was 91 percent", "n = 720 postings"):
        assert not C.COMPARATOR_RE.search(phrase), phrase


# ---------------------------------------------------------------- v1.3: the diagram restyler
RAW_GITDIAGRAM = """flowchart TD

subgraph group_data["Data Preparation"]
  node_ingest["Order ingest<br/>[run.py]"]
  node_features["Feature build<br/>[run.py]"]
end

node_analyst(("Analyst"))

node_analyst -->|"runs the pipeline"| node_ingest
node_ingest -->|"builds features"| node_features

click node_ingest "https://github.com/rafaelbraga-kribitz/study/blob/main/run.py"
click node_features "https://github.com/rafaelbraga-kribitz/study/blob/main/run.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
class node_ingest,node_features toneBlue
class node_analyst toneAmber
"""


def _graph_content(text):
    """The graph itself, with the directive, classDef and class lines removed."""
    from readme_quality.diagram import CLASS_RE, CLASSDEF_RE, FLOWCHART_RE, INIT_RE
    t = INIT_RE.sub("", text)
    t = CLASSDEF_RE.sub("", t)
    t = CLASS_RE.sub("", t)
    t = FLOWCHART_RE.sub("", t)
    return [l.strip() for l in t.split("\n") if l.strip()]


def test_restyle_changes_presentation_and_nothing_else():
    from readme_quality.diagram import restyle
    out = restyle(RAW_GITDIAGRAM, "node_analyst")
    assert _graph_content(out) == _graph_content(RAW_GITDIAGRAM)   # every subgraph, node, edge, click kept
    assert "tone" not in out                                       # the seven pastel tones are gone
    assert out.count("classDef ") == 2                             # one neutral class, one accent
    assert "class node_ingest,node_features node" in out
    assert out.rstrip().endswith("class node_analyst accent")
    assert "#FA6400" in out and "#E6E6E6" in out and "#A0A0A0" in out


def test_restyle_puts_the_orange_on_exactly_one_node():
    from readme_quality.diagram import restyle
    out = restyle(RAW_GITDIAGRAM, "node_features")
    accent_lines = [l for l in out.split("\n") if re.match(r"^class .* accent$", l)]
    assert len(accent_lines) == 1
    assert accent_lines[0].split()[1] == "node_features"           # no commas: a single node


def test_restyle_direction_override_moves_no_graph_content():
    """Direction decides whether the graph fits GitHub's 783px README column; it is layout only."""
    from readme_quality.diagram import restyle
    td = restyle(RAW_GITDIAGRAM, "node_analyst")
    lr = restyle(RAW_GITDIAGRAM, "node_analyst", direction="LR")
    assert "flowchart TD" in td and "flowchart LR" in lr
    assert _graph_content(td) == _graph_content(lr) == _graph_content(RAW_GITDIAGRAM)
    assert restyle(RAW_GITDIAGRAM, "node_analyst", direction="lr") == lr   # case-insensitive


def test_init_directive_sets_fontFamily_at_the_top_level():
    """Mermaid 11 ignores fontFamily under themeVariables — verified by rendering both."""
    import json
    from readme_quality.diagram import INIT, MONO, restyle
    cfg = json.loads(re.search(r"%%\{init:\s*(\{.*\})\s*\}%%", INIT, re.S).group(1))
    assert cfg.get("fontFamily") == MONO, "fontFamily must be top-level or the labels fall back"
    assert cfg["themeVariables"].get("fontFamily") == MONO
    assert MONO in restyle(RAW_GITDIAGRAM, "node_analyst")


def test_shipped_mermaid_blocks_all_set_fontFamily_at_the_top_level():
    """The block, the templates and this repository's own README must not regress."""
    import json
    root = Path(__file__).resolve().parent.parent
    files = [root / "blocks" / "architecture-mermaid.md", root / "README.md"]
    files += [root / "templates" / f"{n}.md" for n in ("analytical", "framework", "interactive", "foundation")]
    checked = 0
    for f in files:
        for m in re.finditer(r"%%\{init:\s*(\{.*?\})\s*\}%%", f.read_text(encoding="utf-8"), re.S):
            cfg = json.loads(m.group(1))          # also asserts the directive is valid JSON
            assert "fontFamily" in cfg, f"{f.name}: fontFamily is not top-level"
            checked += 1
    assert checked >= 6


def test_restyle_refuses_an_unknown_direction():
    import pytest
    from readme_quality.diagram import restyle
    with pytest.raises(ValueError, match="not one of"):
        restyle(RAW_GITDIAGRAM, "node_analyst", direction="sideways")


def test_restyle_refuses_an_accent_node_that_is_not_in_the_graph():
    import pytest
    from readme_quality.diagram import restyle
    with pytest.raises(ValueError, match="not in the graph"):
        restyle(RAW_GITDIAGRAM, "node_invented")


def test_parse_graph_finds_entry_points_outputs_and_unclicked_nodes():
    from readme_quality.diagram import parse_graph
    g = parse_graph(RAW_GITDIAGRAM)
    assert g.direction == "TD"
    assert set(g.nodes) == {"node_ingest", "node_features", "node_analyst"}
    assert g.entry_points == ["node_analyst"]
    assert g.outputs == ["node_features"]
    assert g.unclicked == ["node_analyst"]     # an actor has no file to link to


def test_restyled_graph_still_passes_the_link_check(tmp_path, manifest, registry):
    """The restyler's output must satisfy technical.architecture_links, not just look right."""
    from readme_quality.diagram import restyle
    block = "```mermaid\n" + restyle(RAW_GITDIAGRAM, "node_analyst") + "```"
    text = F.COMMUNICATION.replace(F.ARCH_MERMAID.split("```\n\n*Generated")[0] + "```", block)
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    rep = run(repo, arch_project(repo), manifest, registry)
    f = next(x for x in rep.findings if x.id == "technical.architecture_links")
    assert f.status == "PASS", f.message


def test_verify_clicks_matches_the_gate_check(tmp_path, manifest, registry):
    from readme_quality.diagram import parse_graph, verify_clicks
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, COMM_FILES)
    v = verify_clicks(parse_graph(RAW_GITDIAGRAM), repo, "RafaelBraga-Kribitz/study")
    assert v["total"] == 2 and v["files"] == 2 and not v["missing"] and not v["wrong_repo"]
    assert v["case_only"] == ["rafaelbraga-kribitz/study"] * 2     # reported, never a failure

    broken = RAW_GITDIAGRAM.replace("/blob/main/run.py", "/blob/main/gone.py")
    v2 = verify_clicks(parse_graph(broken), repo, "RafaelBraga-Kribitz/study")
    assert len(v2["missing"]) == 2


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
