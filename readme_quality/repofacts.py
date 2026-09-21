"""Facts read from the repository itself (never from prose): license, CI, runtime, targets, tree."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md", "COPYING")
IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".dvc", ".cursor", ".idea", ".vscode", "dist", "build", ".tox", ".egg-info"}

LICENSE_SIGNATURES = [
    ("MIT", re.compile(r"MIT License|Permission is hereby granted, free of charge", re.I)),
    ("Apache-2.0", re.compile(r"Apache License,? Version 2\.0", re.I)),
    ("ISC", re.compile(r"ISC License|Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee", re.I)),
    ("BSD-3-Clause", re.compile(r"BSD 3-Clause|Neither the name of", re.I)),
    ("BSD-2-Clause", re.compile(r"BSD 2-Clause", re.I)),
    ("GPL-3.0", re.compile(r"GNU GENERAL PUBLIC LICENSE\s+Version 3", re.I)),
    ("AGPL-3.0", re.compile(r"GNU AFFERO GENERAL PUBLIC LICENSE", re.I)),
    ("MPL-2.0", re.compile(r"Mozilla Public License,? v(ersion)? 2\.0", re.I)),
    ("CC-BY-4.0", re.compile(r"Creative Commons Attribution 4\.0", re.I)),
    ("Unlicense", re.compile(r"This is free and unencumbered software released into the public domain", re.I)),
]


@dataclass
class RepoFacts:
    repo_dir: Path
    license_file: Path | None = None
    license_id: str = ""            # SPDX-like id detected from LICENSE text
    license_declared: str = ""      # from pyproject/package.json/setup.cfg metadata
    license_declared_source: str = ""
    workflows: list[str] = field(default_factory=list)   # workflow file names
    ci_workflow: str = ""           # ci.yml or the first workflow whose name contains "ci"
    python_requires: str = ""
    python_version_file: str = ""
    node_engine: str = ""
    make_targets: set[str] = field(default_factory=set)
    just_targets: set[str] = field(default_factory=set)
    top_level: list[tuple[str, bool, int]] = field(default_factory=list)  # (name, is_dir, file_count)
    first_commit_year: str = ""
    last_commit_date: str = ""
    default_branch: str = ""
    remote_url: str = ""
    has_pyproject: bool = False
    has_package_json: bool = False
    package_json_deps: set[str] = field(default_factory=set)
    pyproject_deps: set[str] = field(default_factory=set)
    python_deps: set[str] = field(default_factory=set)      # normalized, from pyproject + requirements*.txt
    python_dep_sources: list[str] = field(default_factory=list)  # files the names came from
    all_files: list[Path] = field(default_factory=list)

    def has_file(self, rel: str) -> bool:
        return (self.repo_dir / rel).exists()

    def declares_python_dep(self, name: str) -> bool:
        return normalize_dep(name) in self.python_deps

    def basename_index(self) -> dict[str, list[Path]]:
        idx: dict[str, list[Path]] = {}
        for p in self.all_files:
            idx.setdefault(p.name.lower(), []).append(p)
        return idx


def normalize_dep(name: str) -> str:
    """PEP 503 normalization, so `bk_viz`, `BK-VIZ` and `bk.viz` are one name."""
    return re.sub(r"[-_.]+", "-", str(name).strip()).lower()


def _dep_names_from_requirement(spec: str) -> str:
    """The distribution name out of one requirement line, including PEP 508 direct URLs."""
    s = spec.split("#", 1)[0].strip()
    if not s or s.startswith("-"):           # -r other.txt, -e ., --index-url …
        return ""
    s = s.split(";", 1)[0].strip()           # environment marker
    s = re.split(r"\s*@\s*", s, maxsplit=1)[0]   # name @ git+https://…
    m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?", s)
    return m.group(1) if m else ""


def _collect_python_deps(repo_dir: Path, f: RepoFacts) -> None:
    """Declared Python dependencies from pyproject.toml and every requirements*.txt."""
    py = repo_dir / "pyproject.toml"
    if py.is_file():
        txt = py.read_text(encoding="utf-8", errors="replace")
        names: set[str] = set()
        try:
            import tomllib
            data = tomllib.loads(txt)
            proj = data.get("project") or {}
            arrays = [proj.get("dependencies") or []]
            arrays += list((proj.get("optional-dependencies") or {}).values())
            arrays += list((data.get("dependency-groups") or {}).values())
            for arr in arrays:
                for spec in arr:
                    if isinstance(spec, str):
                        names.add(_dep_names_from_requirement(spec))
            tool = data.get("tool") or {}
            # uv/poetry/pdm source tables name the same distributions by key
            names |= set((tool.get("uv") or {}).get("sources") or {})
            names |= set(((tool.get("poetry") or {}).get("dependencies") or {}))
            names |= set(((tool.get("poetry") or {}).get("group") or {}).get("dev", {}).get("dependencies") or {})
        except Exception:  # unparsable or older runtime: fall back to the loose scan
            names |= {_dep_names_from_requirement(x) for x in re.findall(r"^\s*[\"']([^\"']+)[\"']", txt, re.M)}
            names |= set(re.findall(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*=\s*\{", txt, re.M))
        if names:
            f.python_dep_sources.append("pyproject.toml")
        f.python_deps |= {normalize_dep(n) for n in names if n}

    for req in sorted(repo_dir.glob("requirements*.txt")) + sorted(repo_dir.glob("requirements/*.txt")):
        try:
            lines = req.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        found = {normalize_dep(n) for n in (_dep_names_from_requirement(l) for l in lines) if n}
        if found:
            f.python_dep_sources.append(req.relative_to(repo_dir).as_posix())
        f.python_deps |= found


def _git(repo_dir: Path, *args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(repo_dir), *args], capture_output=True, text=True, timeout=30)
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def detect_license_id(text: str) -> str:
    for lid, rx in LICENSE_SIGNATURES:
        if rx.search(text):
            return lid
    return "UNKNOWN"


def _walk(repo_dir: Path, limit: int = 20000) -> list[Path]:
    out: list[Path] = []
    stack = [repo_dir]
    while stack and len(out) < limit:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name in IGNORED_DIRS or e.name.endswith(".egg-info"):
                    continue
                stack.append(e)
            else:
                out.append(e)
    return out


def collect(repo_dir: Path) -> RepoFacts:
    repo_dir = Path(repo_dir).resolve()
    f = RepoFacts(repo_dir=repo_dir)

    for name in LICENSE_FILES:
        p = repo_dir / name
        if p.is_file():
            f.license_file = p
            f.license_id = detect_license_id(p.read_text(encoding="utf-8", errors="replace"))
            break

    py = repo_dir / "pyproject.toml"
    if py.is_file():
        f.has_pyproject = True
        txt = py.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^license\s*=\s*(?:\{\s*text\s*=\s*)?[\"']([^\"']+)[\"']", txt, re.M)
        if m:
            f.license_declared, f.license_declared_source = m.group(1).strip(), "pyproject.toml"
        m = re.search(r"^requires-python\s*=\s*[\"']([^\"']+)[\"']", txt, re.M)
        if m:
            f.python_requires = m.group(1).strip()
        deps = re.findall(r"^\s*[\"']([A-Za-z0-9_.\-]+)", txt, re.M)
        f.pyproject_deps = {d.lower() for d in deps}
    pv = repo_dir / ".python-version"
    if pv.is_file():
        f.python_version_file = pv.read_text(encoding="utf-8", errors="replace").strip().splitlines()[0] if pv.read_text(encoding="utf-8", errors="replace").strip() else ""

    pj = repo_dir / "package.json"
    if pj.is_file():
        f.has_package_json = True
        try:
            data = json.loads(pj.read_text(encoding="utf-8", errors="replace"))
            if isinstance(data.get("license"), str) and not f.license_declared:
                f.license_declared, f.license_declared_source = data["license"], "package.json"
            eng = (data.get("engines") or {}).get("node")
            if eng:
                f.node_engine = str(eng)
            for key in ("dependencies", "devDependencies"):
                f.package_json_deps |= {k.lower() for k in (data.get(key) or {})}
        except (ValueError, AttributeError):
            pass

    if not f.license_declared:  # nested packages (depth <= 2), e.g. app/package.json or src/pkg/pyproject.toml
        for cand in sorted(list(repo_dir.glob("*/package.json")) + list(repo_dir.glob("*/*/package.json")) + list(repo_dir.glob("*/pyproject.toml"))):
            if any(part in IGNORED_DIRS for part in cand.relative_to(repo_dir).parts):
                continue
            try:
                txt = cand.read_text(encoding="utf-8", errors="replace")
                if cand.name == "package.json":
                    val = json.loads(txt).get("license")
                else:
                    m = re.search(r"^license\s*=\s*(?:\{\s*text\s*=\s*)?[\"']([^\"']+)[\"']", txt, re.M)
                    val = m.group(1) if m else None
                if isinstance(val, str) and val.strip():
                    f.license_declared, f.license_declared_source = val.strip(), cand.relative_to(repo_dir).as_posix()
                    break
            except (ValueError, OSError):
                continue

    wf_dir = repo_dir / ".github" / "workflows"
    if wf_dir.is_dir():
        f.workflows = sorted(p.name for p in wf_dir.iterdir() if p.suffix in (".yml", ".yaml"))
        for w in f.workflows:
            if w.lower() in ("ci.yml", "ci.yaml"):
                f.ci_workflow = w
                break
        if not f.ci_workflow:
            for w in f.workflows:
                if "ci" in w.lower().replace("citation", ""):
                    f.ci_workflow = w
                    break

    mk = repo_dir / "Makefile"
    if mk.is_file():
        for m in re.finditer(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)", mk.read_text(encoding="utf-8", errors="replace"), re.M):
            f.make_targets.add(m.group(1))
        # includes: Makefile.governance etc.
        for inc in re.findall(r"^-?include\s+(\S+)", mk.read_text(encoding="utf-8", errors="replace"), re.M):
            ip = repo_dir / inc
            if ip.is_file():
                for m in re.finditer(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)", ip.read_text(encoding="utf-8", errors="replace"), re.M):
                    f.make_targets.add(m.group(1))
    jf = repo_dir / "justfile"
    if jf.is_file():
        for m in re.finditer(r"^([A-Za-z0-9_\-]+)(?:\s+[^:\n]*)?:(?!=)", jf.read_text(encoding="utf-8", errors="replace"), re.M):
            f.just_targets.add(m.group(1))

    _collect_python_deps(repo_dir, f)

    f.all_files = _walk(repo_dir)
    try:
        for e in sorted(repo_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            if e.name in IGNORED_DIRS or e.name.startswith(".") and e.name not in (".github",):
                continue
            if e.is_dir():
                count = sum(1 for p in f.all_files if e in p.parents)
                f.top_level.append((e.name, True, count))
            else:
                f.top_level.append((e.name, False, 1))
    except OSError:
        pass

    f.first_commit_year = _git(repo_dir, "log", "--reverse", "--format=%ad", "--date=format:%Y")[:4]
    f.last_commit_date = _git(repo_dir, "log", "-1", "--format=%ad", "--date=short")
    f.default_branch = _git(repo_dir, "rev-parse", "--abbrev-ref", "HEAD")
    f.remote_url = _git(repo_dir, "remote", "get-url", "origin")
    return f


def github_slug_from_remote(remote_url: str) -> str:
    m = re.search(r"github\.com[:/]([^/]+/[^/.]+)", remote_url or "")
    return m.group(1) if m else ""
