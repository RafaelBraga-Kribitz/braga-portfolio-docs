"""Loader for manifest/requirements.yaml (the machine-readable contract)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = HERE / "manifest" / "requirements.yaml"


@dataclass
class Requirement:
    id: str
    title: str
    applies_to: list[str]
    severity: str
    check: str
    evidence: str = ""
    remediation: str = "manual"
    human_escalation: str | None = None
    excellence: bool = False
    notes: str = ""
    retired: bool = False

    @property
    def required(self) -> bool:
        return self.severity == "required" and not self.excellence


@dataclass
class Manifest:
    version: str
    max_readme_lines: int
    project_types: dict[str, str]
    status_vocabulary: list[str]
    epistemic_tags: list[str]
    requirements: list[Requirement] = field(default_factory=list)
    path: Path | None = None

    def get(self, rid: str) -> Requirement | None:
        for r in self.requirements:
            if r.id == rid:
                return r
        return None


def load_manifest(path: Path | str | None = None) -> Manifest:
    path = Path(path) if path else DEFAULT_MANIFEST
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    reqs = []
    for raw in data.get("requirements", []):
        raw = dict(raw)
        for k in list(raw):
            if k not in Requirement.__dataclass_fields__:
                raw.pop(k)
        raw["applies_to"] = list(raw.get("applies_to") or ["all"])
        reqs.append(Requirement(**raw))
    ids = [r.id for r in reqs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"duplicate requirement ids in manifest: {sorted(dupes)}")
    return Manifest(
        version=str(data.get("version", "0")),
        max_readme_lines=int(data.get("max_readme_lines", 450)),
        project_types=dict(data.get("project_types") or {}),
        status_vocabulary=list(data.get("status_vocabulary") or []),
        epistemic_tags=list(data.get("epistemic_tags") or []),
        requirements=[r for r in reqs if not r.retired],
        path=path,
    )


def applies(req: Requirement, project) -> bool:
    """Does a requirement apply to a project, given its type and registry flags?"""
    for a in req.applies_to:
        if a == "all":
            return True
        if a == project.type:
            return True
        if a == "interactive" and getattr(project, "interactive", False):
            return True
        if a == "incomplete" and getattr(project, "incomplete", False):
            return True
    return False
