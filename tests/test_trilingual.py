from pathlib import Path

from readme_quality.registry import Project
from readme_quality.trilingual import audit_changed_files, audit_readmes
from tests.conftest import make_repo, run


def make_trilingual_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "project"
    repo.mkdir()
    switcher = (
        "[🇧🇷 PT-BR](README.pt-BR.md) · "
        "[🇬🇧 EN-UK](README.md) · "
        "[🇦🇹 DE-AT](README.de-AT.md)"
    )
    for filename in ("README.md", "README.pt-BR.md", "README.de-AT.md"):
        (repo / filename).write_text(f"# Project\n\n{switcher}\n", encoding="utf-8")
    return repo


def test_legacy_readme_is_not_required_to_be_trilingual(tmp_path):
    repo = tmp_path / "project"
    repo.mkdir()
    (repo / "README.md").write_text("# Project\n", encoding="utf-8")

    assert audit_readmes(repo)[0] == "NOT_APPLICABLE"


def test_trilingual_readmes_need_all_three_files_and_switch_links(tmp_path):
    repo = make_trilingual_repo(tmp_path)

    assert audit_readmes(repo) == (
        "PASS",
        "all three locale files exist and each links to PT-BR, EN-UK and DE-AT",
        [],
    )


def test_missing_locale_file_fails(tmp_path):
    repo = make_trilingual_repo(tmp_path)
    (repo / "README.de-AT.md").unlink()

    status, _, evidence = audit_readmes(repo)

    assert status == "FAIL"
    assert any("README.de-AT.md" in item for item in evidence)


def test_each_locale_page_needs_three_correct_switch_links(tmp_path):
    repo = make_trilingual_repo(tmp_path)
    (repo / "README.pt-BR.md").write_text(
        "# Projeto\n\n[PT-BR](README.pt-BR.md) · [EN-UK](README.md) · [DE-AT](wrong.md)\n",
        encoding="utf-8",
    )

    status, _, evidence = audit_readmes(repo)

    assert status == "FAIL"
    assert any("README.pt-BR.md: missing a DE-AT switch link" in item for item in evidence)


def test_trilingual_change_requires_all_locale_files(tmp_path):
    repo = make_trilingual_repo(tmp_path)

    status, _, evidence = audit_changed_files(repo, ["README.md", "README.pt-BR.md"])

    assert status == "FAIL"
    assert any("README.de-AT.md" in item for item in evidence)


def test_trilingual_change_passes_when_all_locale_files_are_included(tmp_path):
    repo = make_trilingual_repo(tmp_path)

    status, message, _ = audit_changed_files(
        repo, ["README.md", "README.pt-BR.md", "README.de-AT.md"]
    )

    assert status == "PASS"
    assert "all three" in message


def test_non_readme_change_does_not_require_locale_update(tmp_path):
    repo = make_trilingual_repo(tmp_path)

    status, _, _ = audit_changed_files(repo, ["src/model.py"])

    assert status == "PASS"


def test_portfolio_audit_includes_trilingual_requirement(tmp_path, manifest, registry):
    switcher = "[PT-BR](README.pt-BR.md) [EN-UK](README.md) [DE-AT](README.de-AT.md)"
    repo = make_repo(tmp_path, "trilingual", "# Project\n\n" + switcher + "\n")
    for filename in ("README.pt-BR.md", "README.de-AT.md"):
        (repo / filename).write_text("# Project\n\n" + switcher + "\n", encoding="utf-8")
    project = Project(name="trilingual", path=str(repo), type="analytical", status="Complete")

    report = run(repo, project, manifest, registry)
    requirement = next(item for item in report.findings if item.id == "communication.trilingual_readmes")

    assert requirement.status == "PASS"


def test_translation_must_preserve_the_heading_outline(tmp_path):
    repo = make_trilingual_repo(tmp_path)
    switcher = "[PT-BR](README.pt-BR.md) [EN-UK](README.md) [DE-AT](README.de-AT.md)"
    (repo / "README.md").write_text(
        "# Project\n\n## Scope\n\nA complete source description with enough words.\n\n" + switcher + "\n",
        encoding="utf-8",
    )
    (repo / "README.pt-BR.md").write_text(
        "# Projeto\n\nA descrição completa da origem contém palavras suficientes.\n\n" + switcher + "\n",
        encoding="utf-8",
    )

    status, _, evidence = audit_readmes(repo)

    assert status == "FAIL"
    assert any("heading outline differs" in item for item in evidence)


def test_materially_shortened_translation_is_flagged(tmp_path):
    repo = make_trilingual_repo(tmp_path)
    switcher = "[PT-BR](README.pt-BR.md) [EN-UK](README.md) [DE-AT](README.de-AT.md)"
    source = " ".join(["source"] * 100)
    shortened = " ".join(["translated"] * 30)
    (repo / "README.md").write_text("# Project\n\n" + source + "\n\n" + switcher + "\n", encoding="utf-8")
    (repo / "README.pt-BR.md").write_text("# Projeto\n\n" + shortened + "\n\n" + switcher + "\n", encoding="utf-8")

    status, _, evidence = audit_readmes(repo)

    assert status == "FAIL"
    assert any("review for omitted or added content" in item for item in evidence)


def test_translation_must_preserve_fenced_code_labels_and_order(tmp_path):
    repo = make_trilingual_repo(tmp_path)
    switcher = "[PT-BR](README.pt-BR.md) [EN-UK](README.md) [DE-AT](README.de-AT.md)"
    fence = chr(96) * 3
    source = "# Project\n\nOne section describes the expected procedure clearly.\n\n" + fence + "bash\nrun-tool\n" + fence + "\n\n" + switcher + "\n"
    translated = "# Projeto\n\nUma seção descreve claramente o procedimento esperado.\n\n" + fence + "text\nrun-tool\n" + fence + "\n\n" + switcher + "\n"
    (repo / "README.md").write_text(source, encoding="utf-8")
    (repo / "README.pt-BR.md").write_text(translated, encoding="utf-8")

    status, _, evidence = audit_readmes(repo)

    assert status == "FAIL"
    assert any("fenced code-block labels or order differ" in item for item in evidence)
