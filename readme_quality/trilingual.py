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
    language: re.compile(rf"\b{language[:2]}[-_–]{language[3:]}\b", re.IGNORECASE)
    for language in README_FILES
}
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})[ \t]+", re.MULTILINE)
BACKTICK = chr(96)
FENCE_OPEN = re.compile(r"^(" + BACKTICK + r"{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^(" + BACKTICK + r"{3,}|~{3,})[ \t]*$")
MIN_WORD_RATIO = 0.70
MAX_WORD_RATIO = 1.50


def is_trilingual(repo_dir: Path) -> bool:
    """Auto-detect an intentional trilingual README set without affecting legacy READMEs."""
    if any((repo_dir / name).is_file() for name in ("README.pt-BR.md", "README.de-AT.md")):
        return True
    readme = repo_dir / "README.md"
    if not readme.is_file():
        return False
    text = readme.read_text(encoding="utf-8", errors="replace")
    return all(name in text for name in README_FILES.values())


def _fence_languages(text: str) -> list[str]:
    """Return the language label of each fenced block, ignoring translated block contents."""
    lines = text.splitlines()
    languages: list[str] = []
    index = 0
    while index < len(lines):
        opening = FENCE_OPEN.match(lines[index])
        if not opening:
            index += 1
            continue
        fence, info = opening.groups()
        languages.append(info.strip().split(maxsplit=1)[0].lower() if info.strip() else "")
        index += 1
        while index < len(lines):
            closing = FENCE_CLOSE.match(lines[index])
            if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence):
                break
            index += 1
        index += 1
    return languages


def _word_count(text: str) -> int:
    """Count visible words while excluding code and Markdown link destinations."""
    code_fence = re.compile(
        r"(?ms)^(" + BACKTICK + r"{3,}|~{3,})[^\n]*\n.*?^(?:" + BACKTICK + r"{3,}|~{3,})[ \t]*$"
    )
    text = code_fence.sub(" ", text)
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(BACKTICK + r"([^" + BACKTICK + r"]+)" + BACKTICK, r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"(?u)\b[\w]+(?:[’'][\w]+)?\b", text))


def _translation_parity_errors(source: str, translated: str, filename: str) -> list[str]:
    """Catch structural omissions; these checks cannot certify semantic translation quality."""
    errors: list[str] = []
    source_outline = [len(match.group(1)) for match in HEADING.finditer(source)]
    translated_outline = [len(match.group(1)) for match in HEADING.finditer(translated)]
    if translated_outline != source_outline:
        errors.append(
            f"{filename}: heading outline differs from README.md "
            f"({len(translated_outline)} vs {len(source_outline)} headings)"
        )

    source_fences = _fence_languages(source)
    translated_fences = _fence_languages(translated)
    if translated_fences != source_fences:
        errors.append(
            f"{filename}: fenced code-block labels or order differ from README.md "
            f"({len(translated_fences)} vs {len(source_fences)} blocks)"
        )

    source_words = _word_count(source)
    translated_words = _word_count(translated)
    if source_words == 0:
        errors.append("README.md: no visible words to compare with its translations")
    else:
        ratio = translated_words / source_words
        if ratio < MIN_WORD_RATIO or ratio > MAX_WORD_RATIO:
            errors.append(
                f"{filename}: visible word count is {translated_words} vs {source_words} "
                f"in README.md (ratio {ratio:.2f}; expected {MIN_WORD_RATIO:.2f}–{MAX_WORD_RATIO:.2f}); "
                "review for omitted or added content"
            )
    return errors


def audit_readmes(repo_dir: Path) -> tuple[str, str, list[str]]:
    """Return status, message and evidence for the trilingual README requirement."""
    if not is_trilingual(repo_dir):
        return "NOT_APPLICABLE", "no trilingual README set detected", []

    errors: list[str] = []
    missing = [name for name in README_FILES.values() if not (repo_dir / name).is_file()]
    if missing:
        errors.append("missing locale file(s): " + ", ".join(missing))

    source_path = repo_dir / README_FILES["EN-UK"]
    source = source_path.read_text(encoding="utf-8", errors="replace") if source_path.is_file() else ""
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
                errors.append(f"{filename}: missing a {language} switch link to {target_filename}")
        if locale != "EN-UK" and source_path.is_file():
            errors.extend(_translation_parity_errors(source, text, filename))

    if errors:
        return "FAIL", f"{len(errors)} trilingual README issue(s)", errors
    return (
        "PASS",
        "all locale files and switch links are present; translated heading, code-block and length structure aligns",
        [],
    )


def audit_changed_files(repo_dir: Path, changed_files: list[str]) -> tuple[str, str, list[str]]:
    """Require the complete three-file set whenever any locale README changes in a change set."""
    if not is_trilingual(repo_dir):
        return "PASS", "repository has no trilingual README set; change-set pairing is not applicable", []

    required = set(README_FILES.values())
    changed = {Path(path.replace("\\", "/")).as_posix() for path in changed_files}
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
