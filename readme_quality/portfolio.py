"""Portfolio mode: run the gate (and optionally the fixer) across every registered repository."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from . import checks as C
from .audit import Report, audit_repo, render_text
from .manifest import load_manifest
from .registry import load_registry


@dataclass
class PortfolioRun:
    reports: list[Report] = field(default_factory=list)
    changes: dict[str, list[str]] = field(default_factory=dict)

    @property
    def all_pass(self) -> bool:
        return all(r.gate in ("PASS", "PASS_WITH_EXCELLENCE") for r in self.reports)

    def summary_table(self) -> str:
        w = max(len(r.name) for r in self.reports) if self.reports else 10
        lines = [f"{'Repository':<{w}}  {'Type':<12} {'Status':<22} Open items", "-" * (w + 60)]
        for r in self.reports:
            fails = [f.id for f in r.failures]
            blocked = [f.id for f in r.blocked]
            warns = len(r.warnings)
            detail = ""
            if fails:
                detail = "FAIL: " + ", ".join(fails[:5]) + (" …" if len(fails) > 5 else "")
            elif blocked:
                detail = "BLOCKED: " + ", ".join(blocked)
            if warns:
                detail += (" · " if detail else "") + f"{warns} warning(s)"
            lines.append(f"{r.name:<{w}}  {r.project_type:<12} {r.gate:<22} {detail}")
        passed = sum(1 for r in self.reports if r.gate.startswith("PASS"))
        lines.append("-" * (w + 60))
        lines.append(f"{passed}/{len(self.reports)} PASS")
        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps({"reports": [r.to_dict() for r in self.reports], "changes": self.changes}, indent=2, ensure_ascii=False)


def run_portfolio(registry_path=None, repos_root=None, fix: bool = False, names: list[str] | None = None, dry_run: bool = False, fonts_dir=None, verbose: bool = False) -> PortfolioRun:
    registry = load_registry(registry_path, repos_root)
    manifest = load_manifest()
    run = PortfolioRun()
    for p in registry.projects:
        if names and p.name.lower() not in {n.lower() for n in names}:
            continue
        repo_dir = registry.resolve_path(p)
        if not repo_dir.is_dir():
            rep = Report(name=p.name, repo_dir=str(repo_dir), project_type=p.type, readme=None, gate="FAIL", manifest_version=manifest.version)
            rep.notes.append(f"checkout not found at {repo_dir}")
            run.reports.append(rep)
            continue
        if fix:
            from .fix import Fixer
            fixer = Fixer(repo_dir, p, registry, manifest, dry_run=dry_run, fonts_dir=fonts_dir)
            rep, changes = fixer.run()
            run.changes[p.name] = changes
        else:
            rep = audit_repo(repo_dir, p, manifest, registry)
        run.reports.append(rep)
    return run
