"""Structural and change-set checks for three-language README sets."""
from __future__ import annotations

import re
from pathlib import Path

README_FILES = {
    "PT-BR": "README.pt-BR.md",
    "EN-UK": "README.md",
    "DE-AT": "README.de-AT.md",
}
LANGUAGE_PATTERNS = {
    language: re.compile(rf"\\b{language[:2]}[-_–]{language[3:]}\\b", re.IGNORECASE)
    for language in README_FILES
}
MARKDOWN_LINK = re.compile(r"\\[([^\\]]+)\\]\\(([^)]+)\\)")


def is_trilingual(repo_dir: Path) -> bool:
    """Auto-detect an intentional trilingual README set without affecting legacy READMEs."""
    if any((repo_dir / name).is_file() for name in ("README.pt-BR.md", "README.de-AT.md")):
        return True
    readme = repo_dir / "README.md"
    if not readme.is_file():
        return False
    text = readme.read_text(encoding="utf-8", errors="replace")
    return all(name in text for name in README_FILES.values())


def audit_readmes(repo_dir: Path) -> tuple[str, str, list[str]]:
    """Return status, message and evidence for the trilingual README requirement."""
    if not is_trilingual(repo_dir):
        return "NOT_APPLICABLE", "no trilingual README set detected", []

    errors: list[str] = []
    missing = [name for name in README_FILES.values() if not (repo_dir / name).is_file()]
    if missing:
        errors.append("missing locale file(s): " + ", ".join(missing))

    for locale, filename in README_FILES.items():
        path = repo_dir / filename
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        links = [(label.strip(), target.strip().strip("<>")) for label, target in MARKDOWN_LINK.findall(text)]
        for language, target_filename in README_FILES.items():
            matching = [
                target for label, target in links
                if LANGUAGE_PATTERNS[language].search(label)
                and Path(target.split("#", 1)[0]).as_posix() == target_filename
            ]
            if not matching:
                errors.append(
                    f"{filename}: missing a {language} switch link to {target_filename}"
                )

    if errors:
        return "FAIL", f"{len(errors)} trilingual README issue(s)", errors
    return "PASS", "all three locale files exist and each links to PT-BR, EN-UK and DE-AT", []


def audit_changed_files(repo_dir: Path, changed_files: list[str]) -> tuple[str, str, list[str]]:
    """Require the complete three-file set whenever any locale README changes in a change set."""
    if not is_trilingual(repo_dir):
        return "PASS", "repository has no trilingual README set; change-set pairing is not applicable", []

    required = set(README_FILES.values())
    changed = {Path(path.replace("\\\\", "/")).as_posix() for path in changed_files}
    changed_locale_files = changed & required
    if not changed_locale_files:
        return "PASS", "no README locale file changed", []

    missing_updates = sorted(required - changed_locale_files)
    if missing_updates:
        evidence = [
            "changed locale file(s): " + ", ".join(sorted(changed_locale_files)),
            "also update and review: " + ", ".join(missing_updates),
        ]
        return "FAIL", "a trilingual README change must update all three locale files in the same pull request", evidence
    return "PASS", "all three locale README files are included in the change set", []
