"""Shared fixtures: build throwaway repositories with a README and run the gate on them."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from readme_quality.audit import audit_repo  # noqa: E402
from readme_quality.manifest import load_manifest  # noqa: E402
from readme_quality.registry import Author, Project, Registry  # noqa: E402

AUTHOR_BLOCK = """## Author

<table>
  <tr>
    <td>
      <strong>Rafael Braga-Kribitz</strong><br />
      Seiersberg-Pirka, Austria · Portfolio project, 2026<br />
      <a href="https://www.linkedin.com/in/rafaelbragakribitz/">LinkedIn</a>
      ·
      <a href="mailto:rafaelbragakribitz@gmail.com">rafaelbragakribitz@gmail.com</a>
    </td>
  </tr>
</table>
"""

MIT = (ROOT / "blocks" / "licenses" / "mit.txt").read_text(encoding="utf-8").replace("$year", "2026").replace("$holder", "Rafael Braga-Kribitz")


@pytest.fixture
def manifest():
    return load_manifest()


@pytest.fixture
def registry(tmp_path):
    return Registry(path=tmp_path / "portfolio.yaml", repos_root=tmp_path, author=Author(),
                    status_vocabulary=["Prototype", "Foundation", "In development", "Functional", "Complete", "Maintained", "Archived"], projects=[])


def make_repo(tmp_path: Path, name: str, readme: str | None, files: dict[str, str | bytes] | None = None, license_text: str | None = MIT) -> Path:
    repo = tmp_path / name
    repo.mkdir(parents=True, exist_ok=True)
    if readme is not None:
        (repo / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    if license_text:
        (repo / "LICENSE").write_text(license_text, encoding="utf-8")
    for rel, content in (files or {}).items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8", newline="\n")
    return repo


PNG_1x1 = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da6364f8cfc00000020001e221bc330000000049454e44ae426082")


def run(repo: Path, project: Project, manifest, registry):
    return audit_repo(repo, project, manifest, registry)


def statuses(report) -> dict[str, str]:
    return {f.id: f.status for f in report.findings}
