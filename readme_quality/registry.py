"""Portfolio registry (manifest/portfolio.yaml): declared, human-owned project facts.

The registry is the only place where project *type*, *status*, and hero/demo
intent are declared. The gate never infers these from prose. Everything else the
gate needs, it reads from the repository itself.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = HERE / "manifest" / "portfolio.yaml"

VALID_TYPES = {"analytical", "application", "library", "framework", "docs"}


@dataclass
class Author:
    name: str = "Rafael Braga-Kribitz"
    location: str = "Austria"
    place: str = "Seiersberg-Pirka, Austria"
    year: str = "2026"
    linkedin: str = "https://www.linkedin.com/in/rafaelbragakribitz/"
    email: str = "rafaelbragakribitz@gmail.com"
    github: str = "RafaelBraga-Kribitz"
    photo: str = "Author_MDS_Rafael_Braga-Kribitz_kroped.png"   # basename; canonical copy in blocks/assets/, vendored to docs/assets/


@dataclass
class Project:
    name: str
    path: str
    type: str = "library"
    github: str = ""
    title: str = ""                 # human-readable title used by the hero generator
    descriptor: str = ""            # one line, factual, used by the hero generator
    status: str = ""                # controlled vocabulary; empty = BLOCKED_HUMAN on status checks
    interactive: bool = False
    incomplete: bool = False
    public_data: bool = True        # analytical: production-data section required when True
    estimation: str = "yes"         # analytical: "none" => uncertainty check NOT_APPLICABLE
    banner: str = "generated"       # vanity hero shown FIRST: "generated" (design-system banner) or a repo-relative path
    banner_path: str = "docs/assets/hero.png"   # where the generated banner is written
    primary_chart: str = ""         # optional repo-relative path of the main result chart (shown below badges)
    hero: str = ""                  # deprecated alias: "generated" -> banner; a path -> primary_chart
    hero_path: str = ""             # deprecated alias of banner_path
    demo: str = "motion"            # interactive: "motion" | "static" (static needs demo_reason)
    demo_reason: str = ""
    hosted_urls: list[str] = field(default_factory=list)
    license: str = ""               # override for the policy (e.g. "MIT"); empty = derive per policy
    license_blocked_reason: str = ""  # only for contract/employer work or conflicting declarations (docs/LICENSE_POLICY.md §2)
    license_notice: str = ""        # text for a NOTICE file (Apache-2.0 repos that bundle third-party material)
    max_lines: int = 0              # 0 = manifest default
    max_lines_reason: str = ""
    runtime: str = ""               # optional, e.g. "Python 3.12" — shown on the hero if set
    notes: str = ""

    @property
    def is_analytical(self) -> bool:
        return self.type == "analytical"


@dataclass
class Registry:
    path: Path
    repos_root: Path
    author: Author
    status_vocabulary: list[str]
    projects: list[Project]

    def by_name(self, name: str) -> Project | None:
        n = name.lower()
        for p in self.projects:
            if p.name.lower() == n or Path(p.path).name.lower() == n:
                return p
        return None

    def by_path(self, path: Path) -> Project | None:
        target = Path(path).resolve()
        for p in self.projects:
            cand = self.resolve_path(p)
            try:
                if cand.resolve() == target:
                    return p
            except OSError:
                continue
        return None

    def by_remote(self, repo_dir: Path) -> Project | None:
        """Match by the checkout's origin URL (CI checkouts live in folders like `repo/`)."""
        from .repofacts import _git, github_slug_from_remote
        slug = github_slug_from_remote(_git(Path(repo_dir), "remote", "get-url", "origin")).lower()
        if not slug:
            return None
        for p in self.projects:
            if p.github.lower() == slug:
                return p
        return None

    def resolve_path(self, p: Project) -> Path:
        pp = Path(p.path).expanduser()
        return pp if pp.is_absolute() else self.repos_root / pp


def _expand_env(text: str) -> str:
    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", lambda m: os.environ.get(m.group(1), ""), text)


def load_registry(path: Path | str | None = None, repos_root: str | Path | None = None) -> Registry:
    path = Path(path) if path else DEFAULT_REGISTRY
    data = yaml.safe_load(_expand_env(path.read_text(encoding="utf-8"))) or {}
    if "projects" not in data:
        raise SystemExit(f"invalid registry (no projects key): {path}")
    root = repos_root or os.environ.get("BRAGA_REPOS_ROOT") or data.get("repos_root") or (path.parent.parent.parent)
    root = Path(str(root)).expanduser()
    a = data.get("author", {}) or {}
    author = Author(**{k: str(v) for k, v in a.items() if k in Author.__dataclass_fields__})
    vocab = list(data.get("status_vocabulary") or ["Prototype", "Foundation", "In development", "Functional", "Complete", "Maintained", "Archived"])
    projects = []
    for raw in data["projects"]:
        raw = dict(raw)
        for k in list(raw):
            if k not in Project.__dataclass_fields__:
                raw.pop(k)
        p = Project(**raw)
        if p.hero and not raw.get("banner"):  # legacy field
            if p.hero == "generated":
                p.banner = "generated"
            else:
                p.primary_chart = p.hero
        if p.hero_path and not raw.get("banner_path"):
            p.banner_path = p.hero_path
        if p.type not in VALID_TYPES:
            raise SystemExit(f"project {p.name}: unknown type {p.type!r} (valid: {sorted(VALID_TYPES)})")
        if p.status and p.status not in vocab:
            raise SystemExit(f"project {p.name}: status {p.status!r} not in vocabulary {vocab}")
        projects.append(p)
    return Registry(path=path, repos_root=root, author=author, status_vocabulary=vocab, projects=projects)


def project_for_repo(registry: Registry | None, repo_dir: Path, detected: dict | None = None) -> Project:
    """Return the registry project for a checkout, or a synthesized one from detection."""
    if registry:
        p = registry.by_path(repo_dir) or registry.by_name(Path(repo_dir).name) or registry.by_remote(repo_dir)
        if p:
            return p
    d = detected or {}
    return Project(
        name=Path(repo_dir).name,
        path=str(Path(repo_dir).resolve()),
        type=d.get("type", "library"),
        interactive=bool(d.get("interactive", False)),
        incomplete=bool(d.get("incomplete", False)),
        title=d.get("title", ""),
        descriptor="",
        status="",
        notes="synthesized from detection; not in registry",
    )
