"""Command-line interface.

  python -m readme_quality audit    --repo PATH | --name NAME | --all   [--json] [--verbose]
  python -m readme_quality fix      --repo PATH | --name NAME | --all   [--dry-run]
  python -m readme_quality hero     --repo PATH | --name NAME [--out PATH] [--fonts DIR]
  python -m readme_quality detect   PATH
  python -m readme_quality explain  REQUIREMENT_ID
  python -m readme_quality portfolio [--fix] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .audit import audit_repo, render_text, to_json
from .manifest import load_manifest
from .registry import load_registry, project_for_repo


def _registry(args):
    try:
        return load_registry(getattr(args, "registry", None), getattr(args, "repos_root", None))
    except (SystemExit, FileNotFoundError):
        return None


def _targets(args, registry):
    """Yield (repo_dir, project) for the selection flags."""
    if getattr(args, "all", False):
        if registry is None:
            raise SystemExit("--all needs a registry")
        for p in registry.projects:
            yield registry.resolve_path(p), p
        return
    if getattr(args, "name", None):
        if registry is None:
            raise SystemExit("--name needs a registry")
        p = registry.by_name(args.name)
        if p is None:
            raise SystemExit(f"unknown project {args.name!r}; registered: {[x.name for x in registry.projects]}")
        yield registry.resolve_path(p), p
        return
    repo = Path(getattr(args, "repo", None) or ".").resolve()
    from .detect import detect
    p = project_for_repo(registry, repo, detect(repo))
    yield repo, p


def cmd_audit(args) -> int:
    registry = _registry(args)
    manifest = load_manifest()
    worst = 0
    reports = []
    for repo_dir, p in _targets(args, registry):
        rep = audit_repo(repo_dir, p, manifest, registry)
        reports.append(rep)
        if not args.json:
            print(render_text(rep, verbose=args.verbose))
            print()
        if rep.gate == "FAIL":
            worst = max(worst, 1)
        elif rep.gate == "BLOCKED_HUMAN":
            worst = max(worst, 2)
    if args.json:
        print(json.dumps([r.to_dict() for r in reports], indent=2, ensure_ascii=False))
    return worst


def cmd_fix(args) -> int:
    from .fix import Fixer
    registry = _registry(args)
    manifest = load_manifest()
    worst = 0
    for repo_dir, p in _targets(args, registry):
        fixer = Fixer(repo_dir, p, registry, manifest, dry_run=args.dry_run, fonts_dir=args.fonts)
        rep, changes = fixer.run()
        print(f"== {p.name} ({'dry run' if args.dry_run else 'applied'})")
        for c in changes:
            print(f"   + {c}")
        if not changes:
            print("   (nothing to fix automatically)")
        print(render_text(rep, verbose=args.verbose))
        print()
        worst = max(worst, {"PASS": 0, "PASS_WITH_EXCELLENCE": 0, "FAIL": 1, "BLOCKED_HUMAN": 2}[rep.gate])
    return worst


def cmd_hero(args) -> int:
    from .hero import generate, spec_from_project
    from .repofacts import collect
    registry = _registry(args)
    for repo_dir, p in _targets(args, registry):
        facts = collect(repo_dir)
        spec = spec_from_project(p, facts)
        if args.mode:
            spec.mode = args.mode
        out = Path(args.out) if args.out else repo_dir / (p.hero_path or "docs/assets/hero.png")
        rep = generate(spec, out, fonts_dir=args.fonts, report_path=out.with_suffix(".layout.json"))
        print(f"{p.name}: wrote {out} ({rep['fonts']}; title {rep['title_size']}px; {rep['attempts']} attempt(s); validated)")
    return 0


def cmd_detect(args) -> int:
    from .detect import detect
    d = detect(Path(args.path))
    print(json.dumps(d, indent=2))
    return 0


def cmd_explain(args) -> int:
    m = load_manifest()
    r = m.get(args.id)
    if not r:
        ids = ", ".join(x.id for x in m.requirements)
        raise SystemExit(f"unknown requirement {args.id!r}. Known: {ids}")
    print(f"{r.id} — {r.title}")
    print(f"  applies_to : {', '.join(r.applies_to)}")
    print(f"  severity   : {r.severity}{' (excellence only)' if r.excellence else ''}")
    print(f"  check      : {r.check}")
    print(f"  evidence   : {r.evidence}")
    print(f"  remediation: {r.remediation}")
    print(f"  escalation : {r.human_escalation or 'never'}")
    if r.notes:
        print(f"  notes      : {r.notes}")
    return 0


def cmd_portfolio(args) -> int:
    from .portfolio import run_portfolio
    run = run_portfolio(args.registry, args.repos_root, fix=args.fix, names=args.only, dry_run=args.dry_run, fonts_dir=args.fonts)
    if args.json:
        print(run.to_json())
    else:
        for rep in run.reports:
            if args.fix and run.changes.get(rep.name):
                print(f"== {rep.name}")
                for c in run.changes[rep.name]:
                    print(f"   + {c}")
            if rep.gate not in ("PASS", "PASS_WITH_EXCELLENCE") or args.verbose:
                print(render_text(rep, verbose=args.verbose))
                print()
        print(run.summary_table())
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text("# README Quality Gate — portfolio run\n\n```text\n" + run.summary_table() + "\n```\n", encoding="utf-8")
    return 0 if run.all_pass else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="readme_quality", description=f"BRAGA README Quality Gate v{__version__}")
    ap.add_argument("--registry", help="path to manifest/portfolio.yaml")
    ap.add_argument("--repos-root", help="folder containing the portfolio checkouts (default: $BRAGA_REPOS_ROOT or the registry's parent folder)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def sel(p):
        g = p.add_mutually_exclusive_group()
        g.add_argument("--repo", help="checkout path (default: current directory)")
        g.add_argument("--name", help="registry project name")
        g.add_argument("--all", action="store_true", help="every registry project")

    a = sub.add_parser("audit", help="run the gate"); sel(a)
    a.add_argument("--json", action="store_true"); a.add_argument("--verbose", "-v", action="store_true")
    a.set_defaults(fn=cmd_audit)

    f = sub.add_parser("fix", help="apply safe automatic remediation, then re-run the gate"); sel(f)
    f.add_argument("--dry-run", action="store_true"); f.add_argument("--fonts", help="Söhne font directory")
    f.add_argument("--verbose", "-v", action="store_true")
    f.set_defaults(fn=cmd_fix)

    h = sub.add_parser("hero", help="generate the design-system hero banner"); sel(h)
    h.add_argument("--out"); h.add_argument("--fonts"); h.add_argument("--mode", choices=["light", "dark"])
    h.set_defaults(fn=cmd_hero)

    d = sub.add_parser("detect", help="detect project type from repository contents")
    d.add_argument("path"); d.set_defaults(fn=cmd_detect)

    e = sub.add_parser("explain", help="explain a requirement id")
    e.add_argument("id"); e.set_defaults(fn=cmd_explain)

    pf = sub.add_parser("portfolio", help="audit (or fix) every registered repository")
    pf.add_argument("--fix", action="store_true"); pf.add_argument("--dry-run", action="store_true")
    pf.add_argument("--only", nargs="*"); pf.add_argument("--json", action="store_true")
    pf.add_argument("--report", help="write a markdown summary here"); pf.add_argument("--fonts")
    pf.add_argument("--verbose", "-v", action="store_true")
    pf.set_defaults(fn=cmd_portfolio)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
