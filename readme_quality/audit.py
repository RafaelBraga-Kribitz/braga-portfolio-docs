"""The gate: run every applicable requirement and produce a verdict."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from . import checks as C
from .manifest import Manifest, Requirement, applies, load_manifest
from .parse import Readme, find_readme, parse_file
from .registry import Project, Registry, load_registry, project_for_repo
from .repofacts import RepoFacts, collect

GATE_PASS = "PASS"
GATE_PASS_EXC = "PASS_WITH_EXCELLENCE"
GATE_FAIL = "FAIL"
GATE_BLOCKED = "BLOCKED_HUMAN"


@dataclass
class Finding:
    id: str
    title: str
    severity: str
    status: str
    message: str
    evidence: list[str]
    remediation: str
    auto_fixable: bool
    excellence: bool
    classification: str = ""


@dataclass
class Report:
    name: str
    repo_dir: str
    project_type: str
    readme: str | None
    gate: str
    findings: list[Finding] = field(default_factory=list)
    manifest_version: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def failures(self) -> list[Finding]:
        return [f for f in self.findings if f.status == C.FAIL and f.severity == "required" and not f.excellence]

    @property
    def blocked(self) -> list[Finding]:
        return [f for f in self.findings if f.status == C.BLOCKED]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.status == C.WARN]

    @property
    def auto_fixable(self) -> list[Finding]:
        return [f for f in self.failures + self.blocked if f.auto_fixable]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["failures"] = [f.id for f in self.failures]
        d["blocked"] = [f.id for f in self.blocked]
        d["warnings"] = [f.id for f in self.warnings]
        return d


def build_context(repo_dir: Path, project: Project, manifest: Manifest, registry: Registry | None, readme_path: Path | None = None):
    facts = collect(repo_dir)
    readme_path = readme_path or find_readme(repo_dir)
    rd = parse_file(readme_path) if readme_path else None
    author = registry.author if registry else __import__("readme_quality.registry", fromlist=["Author"]).Author()
    return C.CheckContext(readme=rd, project=project, facts=facts, manifest=manifest, author=author, repo_dir=Path(repo_dir)) if rd else (None, facts, author)


def audit_repo(repo_dir: Path | str, project: Project | None = None, manifest: Manifest | None = None,
               registry: Registry | None = None, readme_path: Path | None = None) -> Report:
    repo_dir = Path(repo_dir).resolve()
    manifest = manifest or load_manifest()
    if registry is None:
        try:
            registry = load_registry()
        except (SystemExit, FileNotFoundError):
            registry = None
    if project is None:
        from .detect import detect
        det = detect(repo_dir)
        project = project_for_repo(registry, repo_dir, det)
    readme_path = readme_path or find_readme(repo_dir)
    report = Report(name=project.name, repo_dir=str(repo_dir), project_type=project.type,
                    readme=str(readme_path) if readme_path else None, gate=GATE_FAIL, manifest_version=manifest.version)
    if getattr(project, "notes", "") and "synthesized" in project.notes:
        report.notes.append(f"project not in registry; type detected as {project.type}")
    if not readme_path:
        report.findings.append(Finding("readme.exists", "README.md exists", "required", C.FAIL,
                                       "no README at the repository root", [], "auto", True, False))
        report.gate = GATE_FAIL
        return report
    ctx = build_context(repo_dir, project, manifest, registry, readme_path)
    exc_pass = 0
    for req in manifest.requirements:
        if not applies(req, project):
            continue
        fn = C.CHECKS.get(req.check)
        if fn is None:
            report.findings.append(Finding(req.id, req.title, req.severity, C.FAIL, f"check {req.check!r} not implemented", [], req.remediation, False, req.excellence))
            continue
        try:
            res = fn(ctx)
        except Exception as exc:  # a broken check must never pass silently
            res = C.Result(C.FAIL, f"check crashed: {type(exc).__name__}: {exc}")
        status = res.status
        if status == C.FAIL and (req.severity == "recommended" or req.excellence):
            status = C.WARN
        if status == C.PASS_EXC:
            exc_pass += 1
        report.findings.append(Finding(req.id, req.title, req.severity, status, res.message, list(res.evidence),
                                       req.remediation, res.auto_fixable, req.excellence, res.classification))
    if report.failures:
        report.gate = GATE_FAIL
    elif report.blocked:
        report.gate = GATE_BLOCKED
    else:
        report.gate = GATE_PASS_EXC if exc_pass >= 2 else GATE_PASS
    return report


# ---------------------------------------------------------------- renderers
def render_text(report: Report, verbose: bool = False) -> str:
    out = [f"{report.name}  [{report.project_type}]  {report.gate}"]
    if report.readme is None:
        out.append("    FAIL  readme.exists  no README at the repository root")
        return "\n".join(out)
    for f in report.findings:
        if f.status in (C.PASS, C.NA, C.PASS_EXC) and not verbose:
            continue
        flag = " (auto-fixable)" if f.auto_fixable and f.status in (C.FAIL, C.BLOCKED) else ""
        out.append(f"    {f.status:<20} {f.id:<32} {f.message}{flag}")
        if f.evidence and (verbose or f.status in (C.FAIL, C.BLOCKED)):
            for e in f.evidence[:4]:
                out.append(f"    {'':<20} {'':<32} - {e}")
    for n in report.notes:
        out.append(f"    note: {n}")
    return "\n".join(out)


def render_markdown(report: Report) -> str:
    lines = [f"### {report.name} — `{report.gate}`", "", "| Requirement | Status | Detail |", "|---|---|---|"]
    for f in report.findings:
        lines.append(f"| `{f.id}` | {f.status} | {f.message.replace('|', '/')} |")
    return "\n".join(lines) + "\n"


def to_json(report: Report) -> str:
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
