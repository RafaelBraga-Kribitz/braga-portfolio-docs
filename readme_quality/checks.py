"""Check functions for every requirement in manifest/requirements.yaml.

Each check receives a CheckContext and returns a Result. Checks are structural
and evidence-based: they read the README and the repository, never a network.
A check must never invent content; it only reports what is and is not there.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .parse import Readme, Section, is_external, resolve_relative, github_slug
from .repofacts import RepoFacts

PASS = "PASS"
PASS_EXC = "PASS_WITH_EXCELLENCE"
NA = "NOT_APPLICABLE"
FAIL = "FAIL"
BLOCKED = "BLOCKED_HUMAN"
WARN = "WARN"


@dataclass
class Result:
    status: str
    message: str = ""
    evidence: list[str] = field(default_factory=list)
    auto_fixable: bool = False
    classification: str = ""  # standard | conditional_standard | project_specific_excellence


@dataclass
class CheckContext:
    readme: Readme
    project: object
    facts: RepoFacts
    manifest: object
    author: object
    repo_dir: Path


# ---------------------------------------------------------------- vocabularies
EXEC_ALIASES = {"decision summary", "decision", "what it does", "the idea", "project status", "what this is", "key findings", "decision and result", "what it is"}
SEE_RUNNING_ALIASES = {"see it running", "demo", "live demo", "screenshots", "what it looks like"}
AUDIENCE_ALIASES = {"explore this project", "start here", "which path applies to you", "audience", "explore", "where to start", "how to read this"}
RESULTS_ALIASES = {"results", "key findings", "decision summary", "decision", "findings", "verified anchors", "coverage and quality", "outcome"}
METHOD_ALIASES = {"method", "methodology", "how it works", "how this was built", "pipeline", "approach", "the workflow", "workflow"}
DATA_ALIASES = {"data", "data sources", "sources", "data provenance", "sources and collection period", "what is real vs. modeled", "what is real vs modeled", "inputs"}
VALIDATION_ALIASES = {"validation", "proof on known truth", "acceptance test", "what the gates actually catch", "tests", "testing", "verification", "diagnostics", "coverage and quality"}
ARCH_ALIASES = {"architecture", "system design", "design", "how it fits together"}
STRUCTURE_ALIASES = {"repository structure", "repository map", "folder structure", "what's inside", "modules", "package map", "structure", "repo structure", "project layout", "layout"}
REPRO_ALIASES = {"reproduce", "reproduction", "quick start", "quickstart", "install", "installation", "usage", "how to run", "getting started", "how to reproduce", "setup", "run it"}
LIMIT_ALIASES = {"limitations", "known limits", "known limitations", "scope", "caveats", "what this does not", "what it does not", "non-goals", "limits"}
PRODUCTION_ALIASES = {"production data", "do differently", "production version", "maintenance", "roadmap", "next steps", "with a real client", "what i would do"}
STATUS_ALIASES = {"status", "project status", "current status"}
LICENSE_ALIASES = {"license", "licence", "license and citation", "licence and citation", "license & author"}
AUTHOR_ALIASES = {"author", "authors", "about the author"}
STACK_ALIASES = {"stack", "technical stack", "tech stack", "technology", "technologies", "built with"}
EXAMPLE_ALIASES = {"quick start", "quickstart", "minimal example", "minimum viable chart", "usage", "example", "the contract", "minimal working example", "getting started", "install"}
CONTRACT_ALIASES = {"what it enforces", "acceptance test", "the contract", "what the gates", "guarantees", "behavioural contract", "behavioral contract", "semantics", "gate behaviour", "gate behavior", "what it adds to the loop", "validation", "what gets gated"}
API_ALIASES = {"api reference", "api", "reference", "commands", "cli reference", "public api", "functions"}
WHY_ALIASES = {"why this project", "what surprised me", "why", "motivation"}
GOVERNANCE_ALIASES = {"governance", "how this was built"}

STANDARD_HEADINGS = (EXEC_ALIASES | SEE_RUNNING_ALIASES | AUDIENCE_ALIASES | RESULTS_ALIASES | METHOD_ALIASES
                     | DATA_ALIASES | VALIDATION_ALIASES | ARCH_ALIASES | STRUCTURE_ALIASES | REPRO_ALIASES
                     | LIMIT_ALIASES | PRODUCTION_ALIASES | STATUS_ALIASES | LICENSE_ALIASES | AUTHOR_ALIASES
                     | STACK_ALIASES | EXAMPLE_ALIASES | CONTRACT_ALIASES | API_ALIASES | WHY_ALIASES | GOVERNANCE_ALIASES
                     | {"what i would do differently with production data", "what i would do with production data", "releases", "development", "configuration", "contributing", "credits", "citation", "modes"})

BANNED_OPENINGS = re.compile(
    r"^(this (is|repo|repository|package|project|library)\b|a (python|reusable|simple|small|lightweight) \b|python port of\b|an? \w+ (package|library|tool|kit) (for|that)\b)",
    re.I,
)
DECISION_WORDS = re.compile(r"\?|\bdecision\b|\bcost\b|\brisk\b|\bwhich\b|\bwhat\b|\bhow much\b|\bwhether\b|\bshould\b", re.I)
QUANT_RE = re.compile(r"\d+(?:[.,]\d+)?\s?(%|percent|pp\b|€|EUR\b|USD\b|\$|MAPE|RMSE|MAE|k\b|M€|×|x\b|s\b|ms\b|weeks?\b|episodes?\b|rows?\b|postings?\b|tests?\b)|\bn\s?=\s?\d|€\s?\d|\$\s?\d", re.I)
UNCERTAINTY_RE = re.compile(r"\binterval\b|credible|confidence|\bp5\b|\bp95\b|\bp10\b|\bp90\b|percentile|±|1σ|\bsigma\b|probability of|std\b|standard deviation|\bHDI\b|\bCI\b|coverage", re.I)
NO_RESULTS_RE = re.compile(r"no results (exist )?yet|results do not (yet )?exist|none are quoted|not yet implemented|does not exist yet|no results are quoted|not yet (built|shipped)|no published|lands here at|what does not exist|nothing here answers", re.I)
VALIDATION_RE = re.compile(r"hold-?out|known[- ]truth|baseline|backtest|cross-?valid|leave-one|precision (audit|of)|acceptance test|self-?test|pytest|vitest|unittest|npm test|make test|make verify|golden|\btests? pass|integration test|unit test|recovery", re.I)
PRODUCTION_RE = re.compile(r"production data|do differently|with a real client|swap-?in|highest-value additions|real[- ]data|client data", re.I)
FALSIFY_RE = re.compile(r"reconsider(ed)?( (this|the|any) [a-z-]+)? if|revisited if|would (change|falsify|retire|break)|revisit (under|if|when)|falsif|what would change|is broken if|contract is broken", re.I)
PLACEHOLDER_RE = re.compile(r"\bTBD\b|\bTODO\b|\bFIXME\b|coming soon|lorem ipsum|\{\{[^}]*\}\}|<!--\s*TEMPLATE|<placeholder>|\[placeholder\]|\bXXX\b|YYYY-MM-DD|<Project Name|<one-line|<the |\[link\]\(\)", re.I)
HYPE_RE = re.compile(r"state[- ]of[- ]the[- ]art|production[- ]ready|blazing(ly)?|seamless(ly)?|cutting[- ]edge|revolutionary|best[- ]in[- ]class|world[- ]class|highly accurate|extremely fast|enterprise[- ]grade|next[- ]generation|game[- ]changing|effortless(ly)?|robust and scalable|industry[- ]leading", re.I)
STATUS_LINE_RE = re.compile(r"^\s*\**status\**\s*:\**\s*[*`]*([A-Za-z][A-Za-z ]+?)[*`]*\s*(?:[·|(—-].*)?$", re.I | re.M)
DATE_RE = re.compile(r"\b(19|20)\d{2}-\d{2}(-\d{2})?\b|\b(19|20)\d{2}\b|\bM\d\b|\bPhase \d|\bv\d+\.\d+|milestone", re.I)
MOTION_RE = re.compile(r"\.gif\b|\.mp4\b|\.webm\b|\.mov\b|youtu\.?be|loom\.com|vimeo\.com|asciinema", re.I)
HOSTED_RE = re.compile(r"github\.io|tableau\.com|streamlit\.app|huggingface\.co|render\.com|run\.app|vercel\.app|netlify\.app|herokuapp|fly\.dev|onrender", re.I)
NO_HOSTED_RE = re.compile(r"no (hosted|live) demo|not hosted|no live url|not deployed|runs? locally only|no interactive ui", re.I)
BOX_RE = re.compile(r"[─│┌└┐┘├┤┬┴┼▼▶►◄▲]|-{2,}>|--->|==>|-> ")
DIAGRAM_LANGS = {"mermaid", "text", "", "ascii", "txt"}


def _sections(ctx: CheckContext, aliases, level=None, contains=True) -> list[Section]:
    return ctx.readme.find_sections(aliases, level=level, contains=contains)


def _vocab_match(value: str, vocab: list[str]) -> str:
    v = value.strip().lower()
    for term in vocab:
        if v == term.lower() or v.startswith(term.lower()):
            return term
    return ""


def _first_prose_paragraph(rd: Readme) -> str:
    """First paragraph of prose in the identity zone after the H1 (skips images, badges, status, html)."""
    paras: list[str] = []
    cur: list[str] = []
    first_h2 = rd.first_h2_line
    ident = "\n".join(rd.masked_lines[:first_h2])  # masked: fenced code is blank
    ident = re.sub(r"<(img|picture|source|p|a|table|tr|td|br|div|span)\b[^>]*?/?>", " ", ident, flags=re.I | re.S)
    ident = re.sub(r"</(picture|p|a|table|tr|td|div|span)>", " ", ident, flags=re.I)
    ident = re.sub(r"<!--.*?-->", " ", ident, flags=re.S)
    h1_line = rd.h1.line if rd.h1 else -1
    for i, line in enumerate(ident.split("\n")):
        if i == h1_line:
            continue
        s = line.strip()
        if not s:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if s.startswith("#") or s.startswith("!["):
            continue
        if s.startswith("<") or s.startswith("[!["):
            continue
        if STATUS_LINE_RE.match(s):
            continue
        if s.startswith("---"):
            continue
        cur.append(s.lstrip("> ").strip())
    if cur:
        paras.append(" ".join(cur))
    for p in paras:
        raw = p.strip()
        if len(raw) > 2 and raw.startswith(("*", "_")) and raw.endswith(("*", "_")) and not raw.startswith("**"):
            continue  # italic caption under the hero, not the problem statement
        cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        cleaned = re.sub(r"[*_`]", "", cleaned)
        if len(cleaned.split()) >= 8:
            return cleaned.strip()
    return ""


def _resolves(ctx: CheckContext, target: str) -> bool:
    p = resolve_relative(ctx.repo_dir, ctx.readme.path or (ctx.repo_dir / "README.md"), target)
    if p is None:
        return True  # external or anchor: not checked here
    return p.exists()


def _hero_images(ctx: CheckContext):
    rd = ctx.readme
    return [im for im in rd.images if im.line < rd.first_h2_line]


def _license_name(lid: str) -> str:
    return {"MIT": "MIT", "Apache-2.0": "Apache", "ISC": "ISC", "BSD-3-Clause": "BSD", "BSD-2-Clause": "BSD",
            "GPL-3.0": "GPL", "AGPL-3.0": "AGPL", "MPL-2.0": "MPL", "CC-BY-4.0": "CC BY", "Unlicense": "Unlicense"}.get(lid, lid)


# ============================================================ identity
def h1_title(ctx: CheckContext) -> Result:
    rd = ctx.readme
    h1 = rd.h1
    if not h1:
        return Result(FAIL, "no H1 title", auto_fixable=True)
    nonblank_before = [l for l in rd.lines[:h1.line] if l.strip()]
    if len(nonblank_before) > 3:
        return Result(FAIL, f"H1 appears at line {h1.line + 1}; must be at the top", auto_fixable=False)
    if "_" in h1.title:
        return Result(FAIL, f"H1 '{h1.title}' is a repository slug (underscores); use a human-readable title", auto_fixable=True)
    return Result(PASS, f"H1: {h1.title}")


def hero_visual(ctx: CheckContext) -> Result:
    imgs = _hero_images(ctx)
    if not imgs:
        return Result(FAIL, "no image before the first H2 (hero slot empty)", auto_fixable=True)
    bad = [im.target for im in imgs if not is_external(im.target) and not _resolves(ctx, im.target)]
    if bad:
        return Result(FAIL, f"hero image does not resolve: {bad[0]}", evidence=bad, auto_fixable=True)
    return Result(PASS, f"hero: {imgs[0].target}")


def badge_row(ctx: CheckContext) -> Result:
    rd, facts = ctx.readme, ctx.facts
    ident = rd.identity
    lines = rd.badge_lines()
    problems = []
    if not lines:
        return Result(FAIL, "no badge row in the identity zone", auto_fixable=True)
    if facts.ci_workflow and "actions/workflows" not in ident:
        problems.append(f"CI workflow {facts.ci_workflow} exists but no CI badge")
    if facts.license_file:
        if not re.search(r"license|licence", ident, re.I):
            problems.append("no license badge although a LICENSE file exists")
        else:
            name = _license_name(facts.license_id)
            if name and name != "UNKNOWN" and not re.search(re.escape(name), ident, re.I):
                problems.append(f"license badge does not name {name} (LICENSE file is {facts.license_id})")
    else:
        m = re.search(r"badge/licen[sc]e-([A-Za-z0-9.]+)", ident, re.I)
        if m:
            problems.append(f"license badge claims {m.group(1)} but no LICENSE file exists")
    if not re.search(r"badge/status-|Status-", ident):
        problems.append("no status badge")
    if problems:
        return Result(FAIL, "; ".join(problems), evidence=problems, auto_fixable=True)
    return Result(PASS, f"{len(lines)} badge line(s)")


def problem_statement(ctx: CheckContext) -> Result:
    rd = ctx.readme
    para = _first_prose_paragraph(rd)
    if not para:
        return Result(FAIL, "no prose paragraph in the identity zone")
    words = len(para.split())
    if words < 12:
        return Result(FAIL, f"first paragraph has {words} words; state the problem in 1-2 sentences", evidence=[para])
    if words > 110:
        return Result(FAIL, f"first paragraph has {words} words; the problem statement must be readable in one breath (max ~2 sentences, <= 110 words)", evidence=[para[:160] + "..."])
    if BANNED_OPENINGS.search(para):
        return Result(FAIL, "opens with a repository description instead of the problem", evidence=[para[:120]])
    if getattr(ctx.project, "is_analytical", False) and not DECISION_WORDS.search(para):
        return Result(FAIL, "analytical project: the opening paragraph names neither a question nor a decision", evidence=[para[:160]])
    return Result(PASS, para[:100] + ("..." if len(para) > 100 else ""))


def status_line(ctx: CheckContext) -> Result:
    rd, vocab = ctx.readme, ctx.manifest.status_vocabulary
    declared = getattr(ctx.project, "status", "")
    m = STATUS_LINE_RE.search(rd.identity)
    if not m:
        if not declared:
            return Result(BLOCKED, "no status line and the registry declares no status for this project; add `status:` to manifest/portfolio.yaml")
        return Result(FAIL, "no `**Status:** <vocabulary>` line before the first H2", auto_fixable=True)
    term = _vocab_match(m.group(1), vocab)
    if not term:
        return Result(FAIL, f"status line value {m.group(1)!r} is not in the vocabulary {vocab}", auto_fixable=bool(declared))
    if declared and term != declared:
        return Result(FAIL, f"status line says {term!r}; registry declares {declared!r}", auto_fixable=True)
    return Result(PASS, f"Status: {term}")


# ============================================================ executive
def executive_summary(ctx: CheckContext) -> Result:
    rd = ctx.readme
    h2s = rd.h2_sections
    if not h2s:
        return Result(FAIL, "no H2 sections")
    first = h2s[0]
    ok = first.norm in EXEC_ALIASES or any(a in first.norm for a in ("decision", "what it does", "the idea", "project status", "key findings", "what this is"))
    if not ok:
        return Result(FAIL, f"first H2 is '{first.heading.title}'; expected an executive answer (Decision summary / What it does / The idea / Project status)", evidence=[first.heading.title])
    prose = " ".join(l for l in first.body_lines if l.strip() and not l.strip().startswith(("|", "```", "!", "<", "#")))
    prose = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", prose)
    if len(prose.split()) < 20:
        return Result(FAIL, f"'{first.heading.title}' has fewer than 20 words of prose; answer the question in a paragraph")
    return Result(PASS, f"first H2: {first.heading.title}")


# ============================================================ evidence
def _non_hero_images(ctx: CheckContext):
    hero_path = getattr(ctx.project, "hero_path", "") or ""
    return [im for im in ctx.readme.images if not im.target.replace("./", "").endswith(hero_path.replace("./", "")) or not hero_path]


def primary_evidence(ctx: CheckContext) -> Result:
    rd, p = ctx.readme, ctx.project
    ptype = p.type
    incomplete = getattr(p, "incomplete", False)
    hero_generated = getattr(p, "hero", "generated") == "generated"
    imgs = [im for im in rd.images if not (hero_generated and im.target.replace("./", "").endswith((getattr(p, "hero_path", "") or "docs/assets/hero.png").replace("./", "")))]
    resolving = [im for im in imgs if is_external(im.target) or _resolves(ctx, im.target)]
    early_limit = 150
    diagram = any(f.lang == "mermaid" or (f.lang in DIAGRAM_LANGS and BOX_RE.search(f.body)) for f in rd.fences)
    has_status = rd.has_section(STATUS_ALIASES | {"project status"})
    tables = rd.tables_in(0, min(len(rd.lines), early_limit))
    if incomplete:
        if diagram and has_status:
            return Result(PASS, "incomplete project: architecture diagram + status section")
        return Result(FAIL, "incomplete project needs an architecture diagram and an explicit status section")
    if ptype == "analytical":
        early_imgs = [im for im in resolving if im.line < early_limit]
        if early_imgs:
            return Result(PASS, f"result visual: {early_imgs[0].target}")
        if any(rows >= 2 for _, rows in tables):
            return Result(PASS, "result table within the first 150 lines")
        return Result(FAIL, "analytical project: no result chart or result table in the first 150 lines")
    if ptype == "library":
        if any(f.lang in ("python", "py", "r", "js", "ts", "typescript", "javascript") for f in rd.fences):
            return Result(PASS, "code example present")
        if resolving:
            return Result(PASS, "rendered output present")
        return Result(FAIL, "library: no runnable code example")
    if ptype == "framework":
        if diagram or rd.has_section(ARCH_ALIASES) or resolving:
            return Result(PASS, "architecture / workflow evidence present")
        return Result(FAIL, "framework: no architecture or workflow diagram")
    if ptype == "application":
        if resolving:
            return Result(PASS, f"screenshot: {resolving[0].target}")
        return Result(FAIL, "application: no screenshot", auto_fixable=False)
    if ptype == "docs":
        return Result(PASS, "docs repository") if rd.h2_sections else Result(FAIL, "no sections")
    return Result(FAIL, f"unknown project type {ptype}")


def see_it_running(ctx: CheckContext) -> Result:
    rd = ctx.readme
    if getattr(ctx.project, "incomplete", False) and not rd.images:
        secs = _sections(ctx, SEE_RUNNING_ALIASES, level=2)
        if secs and (secs[0].body.strip()):
            return Result(PASS, "incomplete interactive project: 'See it running' states the current runnable surface")
    secs = _sections(ctx, SEE_RUNNING_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no 'See it running' section")
    sec = secs[0]
    repro = _sections(ctx, REPRO_ALIASES, level=2)
    body_imgs = rd.images_in(sec.start, sec.end)
    body_fences = rd.fences_in(sec.start, sec.end)
    has_link = bool(re.search(r"https?://", sec.body))
    if not (body_imgs or body_fences or has_link):
        return Result(FAIL, "'See it running' has no screenshot, capture, or link")
    if repro and repro[0].start < sec.start and not (rd.images and rd.images[0].line < repro[0].start):
        return Result(FAIL, "'See it running' appears after the install / reproduce section; show the interface first")
    return Result(PASS, "interface shown before installation")


def demo_motion(ctx: CheckContext) -> Result:
    p = ctx.project
    if getattr(p, "demo", "motion") == "static":
        reason = getattr(p, "demo_reason", "")
        if reason:
            return Result(NA, f"static evidence declared: {reason}")
        return Result(FAIL, "registry says demo: static but gives no demo_reason")
    if MOTION_RE.search(ctx.readme.masked_text):
        return Result(PASS, "GIF / video present")
    return Result(FAIL, "no GIF or video for an interactive interface (set demo: static with a reason if motion adds nothing)")


def live_demo(ctx: CheckContext) -> Result:
    urls = list(getattr(ctx.project, "hosted_urls", []) or [])
    text = ctx.readme.masked_text
    if urls:
        missing = [u for u in urls if u not in text]
        if missing:
            return Result(FAIL, f"declared hosted URL not in README: {missing[0]}", evidence=missing)
        return Result(PASS, f"{len(urls)} hosted URL(s) present")
    if HOSTED_RE.search(text):
        return Result(PASS, "hosted link present")
    if NO_HOSTED_RE.search(text):
        return Result(PASS, "README states that no hosted demo exists")
    return Result(FAIL, "neither a hosted demo link nor a statement that none exists")


# ============================================================ navigation
def audience_paths(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, AUDIENCE_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no 'Explore this project' / 'Start here' section", auto_fixable=False)
    sec = secs[0]
    tables = rd.tables_in(sec.start, sec.end)
    rows = [l for l in sec.body_lines if l.strip().startswith("|")]
    body_rows = [r for r in rows[2:]] if tables else []
    if not tables:
        bullets = [l for l in sec.body_lines if re.match(r"^\s*[-*]\s", l)]
        if len(bullets) < 2:
            return Result(FAIL, "audience section needs a table or list with at least two depth levels")
        body_rows = bullets
    if len(body_rows) < 2:
        return Result(FAIL, "audience table has fewer than two rows")
    unlinked = [r for r in body_rows if not re.search(r"\]\(|`[^`]+`|#[a-z]", r)]
    if unlinked:
        return Result(FAIL, f"{len(unlinked)} audience row(s) do not link anywhere", evidence=[u.strip()[:100] for u in unlinked], auto_fixable=True)
    return Result(PASS, f"{len(body_rows)} audience paths")


# ============================================================ analytical
def decision_stated(ctx: CheckContext) -> Result:
    rd = ctx.readme
    if rd.has_section({"decision", "decision summary", "key findings", "research question", "verified anchors", "results"}):
        return Result(PASS, "decision / findings section present")
    if "?" in rd.identity:
        return Result(PASS, "question posed in the identity zone")
    return Result(FAIL, "no decision, findings, or question stated")


def results_section(ctx: CheckContext) -> Result:
    rd = ctx.readme
    if getattr(ctx.project, "incomplete", False):
        if NO_RESULTS_RE.search(rd.prose_text):
            return Result(PASS, "incomplete: explicit no-results statement")
        return Result(FAIL, "incomplete project must say explicitly that results do not exist yet")
    if rd.has_section(RESULTS_ALIASES, level=2):
        return Result(PASS, "results section present")
    return Result(FAIL, "no Results / Key findings / Decision section")


def _results_text(ctx: CheckContext) -> str:
    secs = _sections(ctx, RESULTS_ALIASES, level=2)
    return "\n".join(s.body for s in secs) if secs else ctx.readme.prose_text


def quantitative_results(ctx: CheckContext) -> Result:
    if getattr(ctx.project, "incomplete", False):
        return Result(NA, "incomplete project")
    text = _results_text(ctx)
    hits = QUANT_RE.findall(text)
    if len(hits) >= 2:
        return Result(PASS, f"{len(hits)} quantitative expressions in the results")
    return Result(FAIL, "results are not quantitative (need numbers with units and a comparator)")


def uncertainty_reported(ctx: CheckContext) -> Result:
    if getattr(ctx.project, "incomplete", False):
        return Result(NA, "incomplete project")
    if getattr(ctx.project, "estimation", "yes") == "none":
        return Result(NA, "registry: no estimated quantities")
    if UNCERTAINTY_RE.search(ctx.readme.prose_text):
        return Result(PASS, "uncertainty wording present")
    return Result(FAIL, "no interval / percentile / probability reported next to the estimates")


def data_provenance(ctx: CheckContext) -> Result:
    secs = _sections(ctx, DATA_ALIASES, level=None, contains=False) or _sections(ctx, {"data", "sources"}, level=None)
    secs = [s for s in secs if s.level in (2, 3)]
    if not secs:
        return Result(FAIL, "no Data / Sources section (H2 or H3)")
    body = " ".join(s.body for s in secs)
    if not re.search(r"\b(19|20)\d{2}\b|weekly|daily|hourly|monthly|quarterly|snapshot|period|window|grain|per (week|day|hour)|episodes|rows|postings", body, re.I):
        return Result(FAIL, "Data section names no period, grain, or size")
    return Result(PASS, f"Data section: {secs[0].heading.title}")


def epistemic_tags(ctx: CheckContext) -> Result:
    tags = ctx.manifest.epistemic_tags
    text = ctx.readme.prose_text
    used = [t for t in tags if re.search(rf"\b{t}\b", text)]
    if not used:
        return Result(FAIL, "no epistemic tags (VERIFIED / CALIBRATED / SIMULATED / ILLUSTRATIVE) applied to any artifact", auto_fixable=False)
    legend = re.search(r"\|\s*`?(VERIFIED|CALIBRATED|SIMULATED|ILLUSTRATIVE)`?\s*\|", text) or re.search(r"epistemic_boundaries|epistemic tags?:|Tag \| Meaning", text, re.I)
    if not legend:
        return Result(FAIL, f"tags used ({', '.join(used)}) but no legend table explaining them", auto_fixable=True)
    return Result(PASS, f"tags used: {', '.join(used)}")


def method_section(ctx: CheckContext) -> Result:
    if ctx.readme.has_section(METHOD_ALIASES, level=2):
        return Result(PASS, "method section present")
    return Result(FAIL, "no Method / Methodology / How it works section")


def validation_section(ctx: CheckContext) -> Result:
    rd = ctx.readme
    if rd.has_section(VALIDATION_ALIASES, level=2):
        return Result(PASS, "validation section present")
    if VALIDATION_RE.search(rd.prose_text) or any(VALIDATION_RE.search(f.body) for f in rd.fences):
        return Result(PASS, "validation mechanism named in the text")
    return Result(FAIL, "no validation mechanism (holdout, known truth, baseline, tests, acceptance test)")


def production_data(ctx: CheckContext) -> Result:
    if not getattr(ctx.project, "public_data", True):
        return Result(NA, "project uses the client's production data")
    if getattr(ctx.project, "incomplete", False):
        return Result(NA, "incomplete project: no results to carry to production yet")
    rd = ctx.readme
    if rd.has_section(PRODUCTION_ALIASES, level=2) or PRODUCTION_RE.search(rd.prose_text):
        return Result(PASS, "production-data implications present")
    return Result(FAIL, "no 'What I would do with production data' / maintenance roadmap")


# ============================================================ technical
def architecture_inline(ctx: CheckContext) -> Result:
    rd = ctx.readme
    for f in rd.fences:
        if f.lang == "mermaid":
            return Result(PASS, "mermaid diagram")
        if f.lang in DIAGRAM_LANGS and BOX_RE.search(f.body) and len(f.body.splitlines()) >= 3:
            return Result(PASS, "ASCII diagram")
    secs = _sections(ctx, ARCH_ALIASES, level=2)
    for s in secs:
        if rd.images_in(s.start, s.end):
            return Result(PASS, "architecture image")
    return Result(FAIL, "no inline architecture diagram (mermaid, ASCII, or image under Architecture)")


def repo_structure(ctx: CheckContext) -> Result:
    rd, facts = ctx.readme, ctx.facts
    secs = _sections(ctx, STRUCTURE_ALIASES, level=None)
    if not secs:
        return Result(FAIL, "no Repository structure / Modules section", auto_fixable=True)
    body = "\n".join(s.body for s in secs) + "\n" + "\n".join(f.body for s in secs for f in rd.fences_in(s.start, s.end))
    tokens = set(re.findall(r"[`|\s├└─]([A-Za-z0-9_.\-]+)/", body)) | set(x for x in re.findall(r"`([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*)/?`", body) if "/" in x or "." in x)  # file-like tokens only
    tokens |= set(re.findall(r"^\s*([A-Za-z0-9_.\-]+)/\s", body, re.M))
    tokens |= set(re.findall(r"^[├└]──\s+([A-Za-z0-9_.\-]+)", body, re.M))  # top-level tree entries (files too)
    tokens |= set(re.findall(r"^\s*([A-Za-z0-9_\-]+\.[A-Za-z0-9]{1,6})(?:\s{2,}|\s*$)", body, re.M))  # "run.py    entry point"
    existing = 0
    checked = 0
    missing = []
    repo_name = facts.repo_dir.name.lower()
    idx = facts.basename_index()
    dir_names = {p.parent.name.lower() for p in facts.all_files}
    for t in tokens:
        first = t.split("/")[0]
        if first in (".", "..", "") or first.lower() == repo_name or not re.match(r"[A-Za-z._]", first):
            continue
        checked += 1
        last = t.rstrip("/").split("/")[-1].lower()
        if (facts.repo_dir / first).exists() or (facts.repo_dir / t).exists() or last in idx or last in dir_names:
            existing += 1
        else:
            missing.append(t)
    if existing < 3:
        return Result(FAIL, f"structure section names only {existing} existing top-level path(s); need >= 3 real paths", auto_fixable=True)
    if checked and existing / checked < 0.6:
        return Result(FAIL, f"{checked - existing} of {checked} paths in the structure section do not exist on disk", evidence=missing[:6])
    return Result(PASS, f"{existing} real paths listed" + (f"; not on disk: {missing[:3]}" if missing else ""))


def reproduce_section(ctx: CheckContext) -> Result:
    rd, facts = ctx.readme, ctx.facts
    secs = _sections(ctx, REPRO_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no Reproduce / Quick start / Install section")
    fences = [f for s in secs for f in rd.fences_in(s.start, s.end) if f.lang in ("bash", "sh", "shell", "console", "zsh", "python", "powershell", "", "text", "toml")]
    if not fences:
        return Result(FAIL, "reproduce section has no command block")
    problems = []
    for f in fences:
        for m in re.finditer(r"\bmake\s+([A-Za-z0-9_.\-]+)", f.body):
            t = m.group(1)
            if facts.make_targets and t not in facts.make_targets and t not in ("-j", "all"):
                problems.append(f"make {t}: no such target in Makefile")
            if facts.make_targets and t == "all" and "all" not in facts.make_targets:
                problems.append("make all: no such target in Makefile")
        for m in re.finditer(r"\bjust\s+([a-z][A-Za-z0-9_\-]*)", f.body):
            t = m.group(1)
            if facts.just_targets and t not in facts.just_targets:
                problems.append(f"just {t}: no such recipe in justfile")
        for m in re.finditer(r"\bpython3?\s+(?:-m\s+)?([A-Za-z0-9_./\-]+\.py)\b", f.body):
            rel = m.group(1)
            if not (facts.repo_dir / rel).exists() and not (facts.repo_dir / "src" / rel).exists():
                problems.append(f"python {rel}: file not found")
    if problems:
        return Result(FAIL, "commands reference targets/files that do not exist: " + "; ".join(sorted(set(problems))[:4]), evidence=sorted(set(problems)))
    return Result(PASS, f"{len(fences)} command block(s); referenced targets exist")


def stack_table(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, STACK_ALIASES, level=None)
    for s in secs:
        if rd.tables_in(s.start, s.end):
            return Result(PASS, f"stack table under '{s.heading.title}'")
    for hl, rows in rd.tables_in(0, len(rd.lines)):
        header = rd.lines[hl].lower()
        if ("technology" in header or "piece" in header or "layer" in header) and ("role" in header or "why" in header or "technology" in header):
            return Result(PASS, "stack table present")
    return Result(FAIL, "no stack table")


# ============================================================ library / framework
def minimal_example(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, EXAMPLE_ALIASES, level=None)
    for s in secs:
        if any(f.lang in ("python", "py", "yaml", "yml", "bash", "sh", "js", "ts", "typescript", "javascript", "r") for f in rd.fences_in(s.start, s.end)):
            return Result(PASS, f"example under '{s.heading.title}'")
    if any(f.lang in ("python", "py", "yaml") for f in rd.fences):
        return Result(PASS, "code example present")
    return Result(FAIL, "no minimal working example code block")


def behavioural_contract(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, CONTRACT_ALIASES, level=None)
    for s in secs:
        if rd.tables_in(s.start, s.end) or len([l for l in s.body_lines if re.match(r"^\s*[-*]\s", l)]) >= 2 or len(s.body.split()) >= 40:
            return Result(PASS, f"contract under '{s.heading.title}'")
    for hl, rows in rd.tables_in(0, len(rd.lines)):
        header = rd.lines[hl].lower()
        if rows >= 2 and re.search(r"\bgate\b|\brule\b|enforce|guarantee|\bcode\b.*\bmeaning\b|\bexit\b", header):
            return Result(PASS, f"contract table at line {hl + 1}")
    return Result(FAIL, "no behavioural contract / acceptance test / gate table")


def api_reference(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, API_ALIASES, level=None)
    for s in secs:
        if rd.tables_in(s.start, s.end) or any(h.level == 3 and "(" in h.title for h in rd.headings if s.start < h.line < s.end):
            return Result(PASS, f"API reference under '{s.heading.title}'")
    sigs = [h for h in rd.headings if h.level == 3 and re.search(r"\w+\(.*\)", h.title)]
    if len(sigs) >= 2:
        return Result(PASS, f"{len(sigs)} function signatures documented")
    return Result(FAIL, "no API / command reference")


def install_pin(ctx: CheckContext) -> Result:
    rd = ctx.readme
    text = rd.text
    if re.search(r"@v?\d+\.\d+|==\d+\.\d+|>=\s?\d+\.\d+|\bv\d+\.\d+\.\d+\b", text) or rd.has_section({"releases", "release model", "versioning"}):
        return Result(PASS, "version pin or release model stated")
    return Result(FAIL, "no version pin in the install line and no Releases section")


# ============================================================ honesty
def limitations_section(ctx: CheckContext) -> Result:
    rd = ctx.readme
    secs = _sections(ctx, LIMIT_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no Limitations / Known limits / Scope section")
    s = secs[0]
    bullets = [l for l in s.body_lines if re.match(r"^\s*[-*]\s|^\s*\d+\.\s", l)]
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(l for l in s.body_lines if l.strip() and not l.strip().startswith("#")))
    if len(bullets) >= 2 or len([x for x in sentences if len(x.split()) > 4]) >= 2:
        return Result(PASS, f"{max(len(bullets), 2)}+ limitations stated")
    return Result(FAIL, "limitations section has fewer than two limitations")


def falsification_condition(ctx: CheckContext) -> Result:
    if FALSIFY_RE.search(ctx.readme.prose_text):
        return Result(PASS, "falsification condition stated")
    return Result(FAIL, "no 'reconsider if …' / 'would change this conclusion' condition")


def no_placeholders(ctx: CheckContext) -> Result:
    text = re.sub(r"<!--.*?-->", "", ctx.readme.masked_text, flags=re.S)
    hits = [(i + 1, l.strip()[:80]) for i, l in enumerate(text.split("\n")) if PLACEHOLDER_RE.search(l)]
    if hits:
        return Result(FAIL, f"placeholder / template residue at line {hits[0][0]}: {hits[0][1]}", evidence=[f"L{n}: {t}" for n, t in hits[:6]])
    return Result(PASS, "no placeholders")


def no_hype(ctx: CheckContext) -> Result:
    text = ctx.readme.prose_text
    bad = []
    for sent in re.split(r"(?<=[.!?])\s+|\n", text):
        if HYPE_RE.search(sent) and not re.search(r"\d", sent):
            bad.append(sent.strip()[:120])
    if bad:
        return Result(FAIL, f"unsupported superlative: {bad[0]}", evidence=bad[:5])
    return Result(PASS, "no unsupported superlatives")


def status_section(ctx: CheckContext) -> Result:
    rd, vocab = ctx.readme, ctx.manifest.status_vocabulary
    declared = getattr(ctx.project, "status", "")
    secs = _sections(ctx, STATUS_ALIASES, level=2, contains=False)
    if not secs:
        if not declared:
            return Result(BLOCKED, "no Status section and no registry status; declare `status:` in manifest/portfolio.yaml")
        return Result(FAIL, "no `## Status` section", auto_fixable=True)
    s = secs[-1]
    m = STATUS_LINE_RE.search(s.body)
    if not m:
        return Result(FAIL, "Status section has no `**Status:** <vocabulary>` line", auto_fixable=bool(declared))
    term = _vocab_match(m.group(1), vocab)
    if not term:
        return Result(FAIL, f"Status section value {m.group(1)!r} not in vocabulary", auto_fixable=bool(declared))
    if declared and term != declared:
        return Result(FAIL, f"Status section says {term!r}; registry declares {declared!r}", auto_fixable=True)
    if not DATE_RE.search(s.body):
        return Result(FAIL, "Status section gives no date, version, or milestone", auto_fixable=True)
    return Result(PASS, f"Status: {term}")


def no_results_statement(ctx: CheckContext) -> Result:
    if NO_RESULTS_RE.search(ctx.readme.prose_text):
        return Result(PASS, "explicit no-results statement")
    return Result(FAIL, "incomplete project: say explicitly what does not exist yet (e.g. 'no results exist yet')")


# ============================================================ links
def images_resolve(ctx: CheckContext) -> Result:
    bad = []
    for im in ctx.readme.images:
        if is_external(im.target):
            continue
        if not _resolves(ctx, im.target):
            bad.append(f"L{im.line + 1}: {im.target}")
    if bad:
        return Result(FAIL, f"{len(bad)} image reference(s) do not resolve", evidence=bad, auto_fixable=True)
    return Result(PASS, f"{len(ctx.readme.images)} image(s) resolve")


def links_resolve(ctx: CheckContext) -> Result:
    rd = ctx.readme
    slugs = {h.slug for h in rd.headings}
    bad = []
    for ln in rd.links:
        t = ln.target.strip()
        if is_external(t) or not t:
            continue
        if t.startswith("#"):
            if t[1:].lower() not in slugs:
                bad.append(f"L{ln.line + 1}: anchor {t} matches no heading")
            continue
        if not _resolves(ctx, t):
            bad.append(f"L{ln.line + 1}: {t}")
    if bad:
        return Result(FAIL, f"{len(bad)} relative link(s) do not resolve", evidence=bad[:10], auto_fixable=True)
    return Result(PASS, "all relative links resolve")


# ============================================================ meta
def license_file(ctx: CheckContext) -> Result:
    facts, p = ctx.facts, ctx.project
    if facts.license_file:
        return Result(PASS, f"{facts.license_file.name}: {facts.license_id}")
    reason = getattr(p, "license_blocked_reason", "")
    if reason:
        return Result(BLOCKED, f"no LICENSE file; human decision required: {reason}")
    return Result(FAIL, "no LICENSE file (auto remediation follows docs/LICENSE_POLICY.md)", auto_fixable=True)


def license_section(ctx: CheckContext) -> Result:
    rd, facts = ctx.readme, ctx.facts
    secs = _sections(ctx, LICENSE_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no `## License` section", auto_fixable=True)
    body = " ".join(s.body for s in secs)
    if facts.license_file:
        name = _license_name(facts.license_id)
        if facts.license_id == "UNKNOWN":
            return Result(PASS, "License section present (LICENSE text not recognised; not compared)")
        if not re.search(re.escape(name), body, re.I):
            return Result(FAIL, f"License section does not name {name} (LICENSE file is {facts.license_id})", auto_fixable=True)
        return Result(PASS, f"License section names {name}")
    if re.search(r"no license|not licensed|unlicensed|source-available|pending an explicit licen|no `?LICENSE`? file", body, re.I):
        return Result(PASS, "License section truthfully states that no license file exists")
    if re.search(r"\b(MIT|Apache|BSD|GPL|ISC)\b", body):
        return Result(FAIL, "License section names a license but the repository has no LICENSE file", auto_fixable=True)
    return Result(FAIL, "License section must name the license or state that none exists", auto_fixable=True)


def author_block(ctx: CheckContext) -> Result:
    rd, a = ctx.readme, ctx.author
    secs = _sections(ctx, AUTHOR_ALIASES, level=2)
    if not secs:
        return Result(FAIL, "no `## Author` section", auto_fixable=True)
    body = secs[-1].body
    missing = [x for x in (a.name, a.location, str(a.year), a.linkedin) if x not in body]
    if missing:
        return Result(FAIL, f"author block missing: {missing}", auto_fixable=True)
    return Result(PASS, "canonical author block")


def readme_length(ctx: CheckContext) -> Result:
    n = len(ctx.readme.lines)
    limit = getattr(ctx.project, "max_lines", 0) or ctx.manifest.max_readme_lines
    if n <= limit:
        return Result(PASS, f"{n} lines (limit {limit})")
    reason = getattr(ctx.project, "max_lines_reason", "")
    return Result(FAIL, f"{n} lines exceeds {limit}; move migration notes, changelogs, and long caveats into docs/ and link them" + (f" ({reason})" if reason else ""))


# ============================================================ excellence
def audience_personas(ctx: CheckContext) -> Result:
    text = ctx.readme.prose_text
    if re.search(r"recruiter", text, re.I) and re.search(r"hiring manager", text, re.I) and re.search(r"auditor|technical reviewer", text, re.I):
        return Result(PASS_EXC, "persona table present", classification="project_specific_excellence")
    return Result(FAIL, "no persona table")


def claim_tracing(ctx: CheckContext) -> Result:
    text = ctx.readme.text
    if re.search(r"<!--\s*claim:", text) or re.search(r"NUMERIC_SSOT|digest\.py|render_readme|numbers-gate|readme-numbers", text, re.I):
        return Result(PASS_EXC, "claims traced to artifacts", classification="project_specific_excellence")
    return Result(FAIL, "no claim tracing")


def why_section(ctx: CheckContext) -> Result:
    if ctx.readme.has_section(WHY_ALIASES, level=2):
        return Result(PASS_EXC, "why / surprise section", classification="project_specific_excellence")
    return Result(FAIL, "no why section")


def project_specific_sections(ctx: CheckContext) -> Result:
    extras = []
    for s in ctx.readme.h2_sections:
        n = s.norm
        if n in STANDARD_HEADINGS or any(a in n for a in STANDARD_HEADINGS if len(a) > 5):
            continue
        extras.append(s.heading.title)
    if extras:
        return Result(PASS_EXC, f"{len(extras)} project-specific section(s) preserved: " + "; ".join(extras[:6]), evidence=extras, classification="project_specific_excellence")
    return Result(PASS, "no sections outside the standard vocabulary", classification="standard")


CHECKS = {
    "h1_title": h1_title,
    "hero_visual": hero_visual,
    "badge_row": badge_row,
    "problem_statement": problem_statement,
    "status_line": status_line,
    "executive_summary": executive_summary,
    "primary_evidence": primary_evidence,
    "see_it_running": see_it_running,
    "demo_motion": demo_motion,
    "live_demo": live_demo,
    "audience_paths": audience_paths,
    "decision_stated": decision_stated,
    "results_section": results_section,
    "quantitative_results": quantitative_results,
    "uncertainty_reported": uncertainty_reported,
    "data_provenance": data_provenance,
    "epistemic_tags": epistemic_tags,
    "method_section": method_section,
    "validation_section": validation_section,
    "production_data": production_data,
    "architecture_inline": architecture_inline,
    "repo_structure": repo_structure,
    "reproduce_section": reproduce_section,
    "stack_table": stack_table,
    "minimal_example": minimal_example,
    "behavioural_contract": behavioural_contract,
    "api_reference": api_reference,
    "install_pin": install_pin,
    "limitations_section": limitations_section,
    "falsification_condition": falsification_condition,
    "no_placeholders": no_placeholders,
    "no_hype": no_hype,
    "status_section": status_section,
    "no_results_statement": no_results_statement,
    "images_resolve": images_resolve,
    "links_resolve": links_resolve,
    "license_file": license_file,
    "license_section": license_section,
    "author_block": author_block,
    "readme_length": readme_length,
    "audience_personas": audience_personas,
    "claim_tracing": claim_tracing,
    "why_section": why_section,
    "project_specific_sections": project_specific_sections,
}
