#!/usr/bin/env python3
"""BRAGA Portfolio README Standard v1.0 — structural checker.

Checks slots, not prose quality. Project type comes from portfolio.yaml;
this script never infers type from the README.

Usage:
  python tools/readme_audit.py --all
  python tools/readme_audit.py --repo /path/to/checkout
  python tools/readme_audit.py --name warehouse_humanoid_tco
  python tools/readme_audit.py --all --report docs/readme-audit.md
  BRAGA_REPOS_ROOT=~/code python tools/readme_audit.py --all
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "portfolio.yaml"
DEFAULT_REPOS_ROOT = Path(os.environ.get("BRAGA_REPOS_ROOT", Path.home() / "code"))

BANNED_OPENINGS = (
    r"^this is a python\b",
    r"^this repository contains\b",
    r"^this repo (contains|is)\b",
    r"^this package is a python\b",
)

EXECUTIVE_ALIASES = {
    "decision summary",
    "decision",
    "what it does",
    "the idea",
    "project status",
    "what's inside",
}

SEE_RUNNING_ALIASES = {
    "see it running",
    "quick start",
    "demo",
    "live demo",
    "how to run",
}

AUDIENCE_ALIASES = {
    "explore this project",
    "which path applies to you",
    "start here",
    "audience",
}

REPRODUCE_ALIASES = {
    "reproduce",
    "reproduction",
    "quick start",
    "install",
    "installation",
    "how to run",
    "how to reproduce",
    "how to reproduce (once m1+ lands)",
}

ARCHITECTURE_ALIASES = {
    "architecture",
    "repository structure",
    "folder structure",
    "what's inside",
    "modules",
    "repo structure",
    "how this was built",
}

LIMITATIONS_ALIASES = {
    "limitations",
    "known limits",
    "known limitations",
    "scope",
    "non-goals",
    "what this does not",
    "caveats",
}

LICENSE_ALIASES = {"license", "license & author", "licence"}

AUTHOR_ALIASES = {"author", "authors", "credits", "license & author"}

RESULTS_ALIASES = {"results", "decision summary", "decision"}

METHOD_ALIASES = {
    "method",
    "methodology",
    "how this was built",
    "three-step workflow",
    "the contract",
    "workflow",
}

DATA_ALIASES = {"data", "data sources", "data provenance", "what is real vs. modeled"}

VALIDATION_ALIASES = {
    "validation",
    "proof on known truth",
    "diagnostics",
    "acceptance test",
    "what the gates actually catch",
    "verified anchors",
    "skills evidence",
}

PRODUCTION_ALIASES = {
    "what i would do differently with production data",
    "what i would do with production data",
    "production version",
    "production-data",
    "with production data",
}

STATUS_SECTION_ALIASES = {"status", "project status", "current status"}

EPISTEMIC_TAGS = ("VERIFIED", "CALIBRATED", "SIMULATED", "ILLUSTRATIVE")

IMG_RE = re.compile(
    r"!\[.*?\]\([^)]+\)|<img\b",
    re.IGNORECASE | re.DOTALL,
)
BADGE_RE = re.compile(
    r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)|img\.shields\.io|badge\.svg",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"```[\s\S]*?```")
MERMAID_RE = re.compile(r"```mermaid\b", re.IGNORECASE)
QUANT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*%|"
    r"\b(?:mape|rmse|mae|npv|pp|ci|crps)\b|"
    r"€\s*\d|\b\d+\.\d+\s*pp\b",
    re.IGNORECASE,
)
NO_RESULTS_RE = re.compile(
    r"no results exist yet|results do not yet exist|the answer lands here|"
    r"none are quoted yet|not yet implemented|no results yet",
    re.IGNORECASE,
)
GIF_RE = re.compile(r"\.gif\b|image/gif", re.IGNORECASE)
DEMO_RE = re.compile(
    r"streamlit\.app|huggingface\.co|tableau\.com|github\.io|"
    r"live demo|dashboard",
    re.IGNORECASE,
)


def load_registry(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("PyYAML is required: pip install pyyaml") from exc
    text = path.read_text(encoding="utf-8")
    # Allow ${BRAGA_REPOS_ROOT} / ${VAR} expansion in the registry.
    text = re.sub(
        r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}",
        lambda m: os.environ.get(m.group(1), ""),
        text,
    )
    data = yaml.safe_load(text)
    if not isinstance(data, dict) or "projects" not in data:
        raise SystemExit(f"invalid registry: {path}")
    return data


def normalize_heading(text: str) -> str:
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^a-z0-9\s'+.-]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def parse_readme(text: str) -> dict:
    headings = []
    for m in HEADING_RE.finditer(text):
        level = len(m.group(1))
        title = m.group(2).strip()
        headings.append(
            {
                "level": level,
                "title": title,
                "norm": normalize_heading(title),
                "start": m.start(),
                "end": m.end(),
            }
        )
    first_h2 = next((h for h in headings if h["level"] >= 2), None)
    identity_end = first_h2["start"] if first_h2 else min(len(text), 1800)
    identity = text[:identity_end]
    return {"text": text, "headings": headings, "identity": identity, "identity_end": identity_end}


def has_heading(parsed: dict, aliases: set[str]) -> bool:
    return any(h["norm"] in aliases or any(a in h["norm"] for a in aliases) for h in parsed["headings"])


def identity_prose(identity: str) -> str:
    lines = []
    for line in identity.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("<") and "linkedin" not in s.lower():
            continue
        if IMG_RE.search(s) and not re.search(r"[A-Za-z]{8,}", IMG_RE.sub("", s)):
            continue
        if BADGE_RE.search(s) and len(re.sub(r"\[!?\[.*?\]\(.*?\)\]\(.*?\)", "", s).strip()) < 20:
            continue
        if s in {"---", "***", "***"}:
            continue
        lines.append(s)
    return "\n".join(lines)


def check_h1(parsed: dict) -> list[str]:
    h1s = [h for h in parsed["headings"] if h["level"] == 1]
    if not h1s:
        return ["missing: H1 title"]
    if h1s[0]["start"] > 80:
        return ["missing: H1 title at top of file"]
    return []


def check_hero(parsed: dict) -> list[str]:
    identity = parsed["identity"]
    if IMG_RE.search(identity):
        return []
    if MERMAID_RE.search(identity):
        return []
    return ["missing: hero visual in identity zone"]


def check_problem(parsed: dict) -> list[str]:
    prose = identity_prose(parsed["identity"])
    # Strip markdown images and badges from prose
    cleaned = IMG_RE.sub("", prose)
    cleaned = BADGE_RE.sub("", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) < 40:
        return ["missing: one-line problem / purpose"]
    first = cleaned[:180].lower()
    for pat in BANNED_OPENINGS:
        if re.search(pat, first):
            return ["problem opens with banned repository-description phrasing"]
    return []


def check_status(parsed: dict, vocabulary: list[str]) -> list[str]:
    vocab = [v.lower() for v in vocabulary]
    text = parsed["text"]
    # **Status:** Foundation  or Status: Foundation
    labeled = re.findall(
        r"\**status\**:\**\s*[*`]*([A-Za-z][A-Za-z ]+)",
        text,
        flags=re.IGNORECASE,
    )
    for hit in labeled:
        token = hit.strip().lower()
        if any(v == token or v in token for v in vocab):
            return []
    # Vocabulary word near a status heading
    if has_heading(parsed, STATUS_SECTION_ALIASES):
        lower = text.lower()
        if any(re.search(rf"\b{re.escape(v)}\b", lower) for v in vocab):
            return []
    # Foundation stage / in development in identity
    ident = parsed["identity"].lower()
    if any(re.search(rf"\b{re.escape(v)}\b", ident) for v in vocab):
        return []
    return ["missing: status (controlled vocabulary)"]


def check_executive(parsed: dict, project: dict) -> list[str]:
    if has_heading(parsed, EXECUTIVE_ALIASES):
        return []
    # Incomplete projects may use project status as the only H2 after identity
    if project.get("incomplete") and has_heading(parsed, {"project status", "status"}):
        return []
    return ["missing: executive answer (Decision / What it does / The idea / Project status)"]


def check_primary_evidence(parsed: dict, project: dict) -> list[str]:
    ptype = project.get("type")
    text = parsed["text"]
    identity = parsed["identity"]
    if ptype == "analytical":
        if IMG_RE.search(identity) or IMG_RE.search(text[:4000]):
            return []
        if project.get("incomplete") and (
            has_heading(parsed, ARCHITECTURE_ALIASES) and has_heading(parsed, STATUS_SECTION_ALIASES | {"project status"})
        ):
            return []
        return ["missing: primary evidence (result chart or architecture+status for incomplete)"]
    if ptype == "library":
        if FENCE_RE.search(text) or IMG_RE.search(text):
            return []
        return ["missing: primary evidence (working example)"]
    if ptype == "framework":
        if MERMAID_RE.search(text) or has_heading(parsed, ARCHITECTURE_ALIASES) or IMG_RE.search(text):
            return []
        return ["missing: primary evidence (architecture / workflow)"]
    # application
    if IMG_RE.search(text) or has_heading(parsed, ARCHITECTURE_ALIASES):
        return []
    if project.get("incomplete") and has_heading(parsed, STATUS_SECTION_ALIASES | EXECUTIVE_ALIASES):
        return []
    return ["missing: primary evidence"]


def check_reproduce(parsed: dict) -> list[str]:
    if has_heading(parsed, REPRODUCE_ALIASES):
        return []
    if re.search(r"```(?:bash|shell|zsh|sh|python)\b", parsed["text"], re.IGNORECASE):
        return []
    return ["missing: reproduce / install / quick-start"]


def check_architecture(parsed: dict) -> list[str]:
    if has_heading(parsed, ARCHITECTURE_ALIASES):
        return []
    if MERMAID_RE.search(parsed["text"]):
        return []
    return ["missing: architecture or repository structure"]


def check_limitations(parsed: dict) -> list[str]:
    if has_heading(parsed, LIMITATIONS_ALIASES):
        return []
    if re.search(r"\blimitation|\bscope\b|\bcaveat", parsed["text"], re.IGNORECASE):
        # require a heading-level treatment, not a stray word
        return ["missing: limitations / scope heading"]
    return ["missing: limitations / scope"]


def check_license(parsed: dict) -> list[str]:
    if has_heading(parsed, LICENSE_ALIASES):
        return []
    if re.search(r"\b(mit|apache|bsd|gpl|license)\b", parsed["text"], re.IGNORECASE):
        return []
    return ["missing: license"]


def check_author(parsed: dict, author: dict) -> list[str]:
    text = parsed["text"]
    missing = []
    name = author.get("name", "Rafael Braga-Kribitz")
    if name not in text:
        missing.append("missing: author name")
    if author.get("location", "Austria") not in text:
        missing.append("missing: author location (Austria)")
    if str(author.get("year", "2026")) not in text:
        missing.append("missing: author year (2026)")
    linkedin = author.get("linkedin", "")
    if linkedin and linkedin not in text:
        missing.append("missing: author LinkedIn URL")
    return missing


def check_audience(parsed: dict) -> list[str]:
    if has_heading(parsed, AUDIENCE_ALIASES):
        return []
    # Two-depth table
    if re.search(r"recruiter|hiring manager|technical reviewer|auditor", parsed["text"], re.IGNORECASE):
        return []
    if re.search(r"fast path|deep path|start here|2-minute", parsed["text"], re.IGNORECASE):
        return []
    # Two of: quick start + architecture/method already present counts if an explore table is missing
    return ["missing: audience path (at least two depths)"]


def check_analytical(parsed: dict, project: dict) -> list[str]:
    issues = []
    text = parsed["text"]
    if not has_heading(parsed, DATA_ALIASES) and not re.search(
        r"synthetic|public data|epistemic|data source", text, re.IGNORECASE
    ):
        issues.append("missing: data provenance")
    if not any(tag in text for tag in EPISTEMIC_TAGS):
        issues.append("missing: epistemic tags (VERIFIED / CALIBRATED / SIMULATED / ILLUSTRATIVE)")
    if not has_heading(parsed, METHOD_ALIASES):
        issues.append("missing: method")
    if not has_heading(parsed, VALIDATION_ALIASES) and not re.search(
        r"\b(holdout|known.?truth|baseline|validation|backtest)\b", text, re.IGNORECASE
    ):
        issues.append("missing: validation")
    if project.get("incomplete"):
        if not NO_RESULTS_RE.search(text) and not has_heading(parsed, {"project status"}):
            issues.append("missing: explicit no-results / foundation status")
    else:
        if not has_heading(parsed, RESULTS_ALIASES) and not QUANT_RE.search(text[:6000]):
            issues.append("missing: results (quantitative)")
        elif not QUANT_RE.search(text) and not NO_RESULTS_RE.search(text):
            issues.append("missing: quantitative result")
    if project.get("production_data_section") and not has_heading(parsed, PRODUCTION_ALIASES):
        if not re.search(r"production data", text, re.IGNORECASE):
            issues.append("missing: production-data implications")
    return issues


def check_interactive(parsed: dict) -> list[str]:
    text = parsed["text"]
    if GIF_RE.search(text) or DEMO_RE.search(text):
        return []
    if IMG_RE.search(text) and has_heading(parsed, SEE_RUNNING_ALIASES | {"see it running"}):
        return []
    if IMG_RE.search(text):
        # screenshot present somewhere — accept for incomplete apps
        return []
    return ["missing: see-it-running (screenshot, GIF, or demo)"]


def audit_project(project: dict, repos_root: Path, author: dict, vocabulary: list[str]) -> dict:
    rel = project["path"]
    repo_dir = Path(rel) if Path(rel).is_absolute() else repos_root / rel
    readme = None
    for cand in ("README.md", "readme.md", "README.rst"):
        p = repo_dir / cand
        if p.is_file():
            readme = p
            break
    result = {
        "name": project["name"],
        "path": str(repo_dir),
        "type": project.get("type"),
        "ok": False,
        "issues": [],
    }
    if not repo_dir.is_dir():
        result["issues"] = [f"missing: checkout at {repo_dir}"]
        return result
    if readme is None:
        result["issues"] = ["missing: README"]
        return result
    parsed = parse_readme(readme.read_text(encoding="utf-8", errors="replace"))
    issues: list[str] = []
    issues += check_h1(parsed)
    issues += check_hero(parsed)
    issues += check_problem(parsed)
    issues += check_status(parsed, vocabulary)
    issues += check_executive(parsed, project)
    issues += check_primary_evidence(parsed, project)
    issues += check_reproduce(parsed)
    issues += check_architecture(parsed)
    issues += check_limitations(parsed)
    issues += check_license(parsed)
    issues += check_author(parsed, author)
    issues += check_audience(parsed)
    if project.get("type") == "analytical":
        issues += check_analytical(parsed, project)
    if project.get("interactive"):
        issues += check_interactive(parsed)
    if project.get("type") in {"library", "framework", "application"}:
        if not has_heading(parsed, SEE_RUNNING_ALIASES | REPRODUCE_ALIASES):
            if "missing: reproduce / install / quick-start" not in issues:
                issues.append("missing: see-it-running / quick-start")
    result["issues"] = issues
    result["ok"] = not issues
    return result


def render_report(results: list[dict], title: str) -> str:
    lines = [f"# {title}", "", f"Checked {len(results)} public portfolio projects.", ""]
    passed = sum(1 for r in results if r["ok"])
    lines.append(f"**{passed}/{len(results)} PASS**",)
    lines.append("")
    lines.append("```text")
    width = max(len(r["name"]) for r in results)
    for r in results:
        status = "PASS" if r["ok"] else "FAIL"
        lines.append(f"{r['name']:<{width}}  {status}")
        if not r["ok"]:
            for issue in r["issues"]:
                lines.append(f"    {issue}")
    lines.append("```")
    lines.append("")
    return "\n".join(lines) + "\n"


def select_projects(registry: dict, name: str | None, repo: str | None, repos_root: Path | None = None) -> list[dict]:
    projects = registry["projects"]
    if name:
        needle = name.lower()
        picked = [p for p in projects if p["name"].lower() == needle or p["path"].lower() == needle]
        if not picked:
            raise SystemExit(f"unknown project {name!r}")
        return picked
    if repo:
        repo_path = Path(repo).resolve()
        root = repos_root
        if root is None:
            configured = registry.get("repos_root") or ""
            root = Path(str(configured)).expanduser() if configured else DEFAULT_REPOS_ROOT
        for p in projects:
            cand = Path(p["path"])
            if not cand.is_absolute():
                cand = root / p["path"]
            try:
                if cand.resolve() == repo_path:
                    return [p]
            except FileNotFoundError:
                continue
        return [
            {
                "name": repo_path.name,
                "path": str(repo_path),
                "type": "library",
                "interactive": False,
                "incomplete": False,
                "production_data_section": False,
            }
        ]
    return projects


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BRAGA README Standard v1.0 checker")
    parser.add_argument("--all", action="store_true", help="audit every registry project")
    parser.add_argument("--name", help="audit one registry project by name")
    parser.add_argument("--repo", help="audit a checkout path")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument(
        "--repos-root",
        help="directory that contains sibling portfolio checkouts "
        "(default: $BRAGA_REPOS_ROOT or ~/code)",
    )
    parser.add_argument("--report", help="write a markdown report to this path")
    parser.add_argument("--title", default="README audit")
    args = parser.parse_args(argv)
    if not (args.all or args.name or args.repo):
        parser.error("pass --all, --name, or --repo")

    registry = load_registry(Path(args.registry))
    configured = registry.get("repos_root") or ""
    if args.repos_root:
        repos_root = Path(args.repos_root).expanduser()
    elif configured:
        repos_root = Path(str(configured)).expanduser()
    else:
        repos_root = DEFAULT_REPOS_ROOT
    author = registry.get("author", {})
    vocabulary = registry.get("status_vocabulary", [])
    projects = select_projects(registry, args.name, args.repo, repos_root)
    results = [audit_project(p, repos_root, author, vocabulary) for p in projects]
    report = render_report(results, args.title)
    sys.stdout.write(report)
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
