"""Project-type detection from repository contents (used only when a repo is not in the registry).

Returns a dict with type, interactive, incomplete, title, and the evidence lines
that led to the call. The registry always wins over detection.
"""
from __future__ import annotations

import re
from pathlib import Path

from .repofacts import collect

ANALYTICAL_DEPS = {"pymc", "statsmodels", "scikit-learn", "sklearn", "xgboost", "lightgbm", "prophet", "arviz", "nutpie", "pulp", "ortools", "duckdb", "dbt-core", "dbt-duckdb", "pandas", "polars"}
UI_DEPS_PY = {"streamlit", "fastapi", "dash", "gradio", "flask", "django", "panel", "voila"}
UI_DEPS_JS = {"react", "next", "vite", "vue", "svelte", "express", "@react-flow/core", "reactflow"}
FRAMEWORK_MARKERS = ("SKILL.md", "templates", "BOOTSTRAP_PROMPT.md", "install.mjs", "capabilities", "skills", "agents", "rules")


def detect(repo_dir: Path | str) -> dict:
    repo_dir = Path(repo_dir)
    facts = collect(repo_dir)
    ev: list[str] = []
    names = {p.name for p in facts.all_files}
    rel = {str(p.relative_to(facts.repo_dir)).replace("\\", "/") for p in facts.all_files}
    top = {n for n, _, _ in facts.top_level}

    scores = {"analytical": 0, "application": 0, "library": 0, "framework": 0, "docs": 0}
    interactive = False
    incomplete = False

    if facts.has_pyproject and (repo_dir / "src").is_dir() and not any(d in top for d in ("reports", "notebooks", "data")):
        scores["library"] += 2; ev.append("pyproject + src/ without reports/notebooks/data -> library")
    if any(d in top for d in ("reports", "notebooks", "data", "dbt")):
        scores["analytical"] += 2; ev.append("reports/ notebooks/ data/ or dbt/ present -> analytical")
    if facts.pyproject_deps & ANALYTICAL_DEPS:
        scores["analytical"] += 1; ev.append(f"analytical deps: {sorted(facts.pyproject_deps & ANALYTICAL_DEPS)[:4]}")
    if facts.pyproject_deps & UI_DEPS_PY:
        interactive = True; scores["application"] += 1; ev.append(f"UI deps: {sorted(facts.pyproject_deps & UI_DEPS_PY)}")
    if facts.package_json_deps & UI_DEPS_JS:
        interactive = True; scores["application"] += 2; ev.append(f"JS UI deps: {sorted(facts.package_json_deps & UI_DEPS_JS)[:3]}")
    if any(m in top or m in names for m in FRAMEWORK_MARKERS):
        scores["framework"] += 2; ev.append("skill / template / capability markers -> framework")
    if any(n.lower().endswith((".ipynb",)) for n in names):
        scores["analytical"] += 1; ev.append("notebooks present")
    if (repo_dir / ".planning").is_dir() or "PROJECT_CHARTER.md" in top:
        ev.append("planning artifacts present (charter / .planning)")
    charter = repo_dir / "PROJECT_CHARTER.md"
    if charter.is_file():
        txt = charter.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\b(foundation|phase 1|M0|not yet implemented|pending)\b", txt, re.I):
            incomplete = True; ev.append("charter mentions foundation / phase 1 / pending -> incomplete hint")
    code_files = [p for p in facts.all_files if p.suffix in (".py", ".ts", ".tsx", ".js", ".R", ".sql")]
    if len(code_files) < 3 and len([p for p in facts.all_files if p.suffix == ".md"]) > 5:
        scores["docs"] += 3; ev.append("mostly markdown, little code -> docs")
    if not code_files and not facts.all_files:
        scores["docs"] += 5; ev.append("empty repository")

    ptype = max(scores, key=lambda k: (scores[k], k == "library"))
    if scores[ptype] == 0:
        ptype = "library"; ev.append("no signals; defaulting to library")
    title = re.sub(r"[-_]+", " ", repo_dir.name).strip().title()
    return {"type": ptype, "interactive": interactive, "incomplete": incomplete, "title": title, "scores": scores, "evidence": ev}
