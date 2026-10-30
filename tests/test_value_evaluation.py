"""honesty.value_evaluation (v1.6): the why-section near the top of the README and its evaluation file."""
from __future__ import annotations

from readme_quality.registry import Project
from tests import fixtures as F
from tests.conftest import make_repo, run
from tests.test_gate import COMMON_FILES

RID = "honesty.value_evaluation"
EVALUATION = "# Economic evaluation\n\nVerdict: fails financial hurdle at 1.9x central. Recommendation: smaller version.\n"
WHY = ("## Why this project exists\n\n"
       "A small bakery orders flour weekly and wastes about one sack in five when demand drops. The forecast is meant to "
       "let the owner cut that waste without running out on busy weeks. The evaluation expected a modest saving against "
       "a build of 24 hours and found that it fails the financial hurdle; the smaller spreadsheet version is enough. "
       "Observed result: not yet measured. See the [economic evaluation](docs/economic-evaluation.md).\n\n")


def _with_why(text: str = WHY, before: str = "## Decision summary") -> str:
    return F.ANALYTICAL.replace(before, text + before, 1)


def _finding(tmp_path, manifest, registry, readme, files):
    repo = make_repo(tmp_path, "study", readme, {**COMMON_FILES, **files})
    p = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated")
    return next(f for f in run(repo, p, manifest, registry).findings if f.id == RID)


def test_the_check_is_recommended_and_manual(manifest):
    r = manifest.get(RID)
    assert manifest.version == "1.6.0"
    assert r.severity == "recommended" and not r.excellence and r.remediation == "manual" and r.applies_to == ["all"]


def test_passes_with_file_verdict_and_section(tmp_path, manifest, registry):
    f = _finding(tmp_path, manifest, registry, _with_why(), {"docs/economic-evaluation.md": EVALUATION})
    assert f.status == "PASS" and "H2 number 1" in f.message


def test_warns_without_the_evaluation_file(tmp_path, manifest, registry):
    f = _finding(tmp_path, manifest, registry, _with_why(), {})
    assert f.status == "WARN" and "no docs/economic-evaluation.md" in f.message


def test_warns_when_the_evaluation_states_no_verdict(tmp_path, manifest, registry):
    f = _finding(tmp_path, manifest, registry, _with_why(), {"docs/economic-evaluation.md": "# Economic evaluation\n\nLooks good.\n"})
    assert f.status == "WARN" and "no hurdle verdict" in f.message


def test_warns_without_the_section(tmp_path, manifest, registry):
    f = _finding(tmp_path, manifest, registry, F.ANALYTICAL, {"docs/economic-evaluation.md": EVALUATION})
    assert f.status == "WARN" and "no '## Why this project exists'" in f.message


def test_warns_when_late_unlinked_or_off_length(tmp_path, manifest, registry):
    short = "## Why this project exists\n\nBecause flour is wasted.\n\n"
    f = _finding(tmp_path, manifest, registry, _with_why(short, before="## Limitations"), {"docs/economic-evaluation.md": EVALUATION})
    assert f.status == "WARN"
    assert "place it among the first three" in f.message
    assert "does not link docs/economic-evaluation.md" in f.message
    assert "has 4 words; the target is 60 to 100" in f.message


def test_registry_exemption_needs_a_reason(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.ANALYTICAL, COMMON_FILES)
    exempt = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated",
                     value_evaluation="none", value_evaluation_reason="not shown on the portfolio website")
    f = next(x for x in run(repo, exempt, manifest, registry).findings if x.id == RID)
    assert f.status == "NOT_APPLICABLE" and "not shown on the portfolio website" in f.message
    bare = Project(name="study", path=str(repo), type="analytical", status="Complete", banner="generated", value_evaluation="none")
    f = next(x for x in run(repo, bare, manifest, registry).findings if x.id == RID)
    assert f.status == "WARN" and "no value_evaluation_reason" in f.message
