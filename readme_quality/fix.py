"""Safe automatic remediation. Every fix here is derived from repository evidence or the
registry; none writes prose that claims something about the project's results.

Fixes (id -> what it does):
  identity.h1           slug title -> registry title
  identity.hero         generate a design-system banner (or insert the declared chart) after the H1
  identity.badges       add missing CI / reproducibility / governance / runtime / license / status badges
  identity.status_line  insert or correct `**Status:** <registry status>`
  honesty.status_section  insert or correct `## Status` with the vocabulary term and the last-commit date
  meta.license_file     create LICENSE per docs/LICENSE_POLICY.md (never changes an existing one)
  meta.license_section  insert or correct `## License` to match the LICENSE file
  meta.author           insert or replace the canonical author block
  technical.structure   insert a factual top-level tree (names and file counts only)
  links.images / links.internal  repair a broken relative path when the basename is unique in the repo
  navigation.audience   turn bare section names in audience rows into anchor links
  analytical.epistemic  insert the tag legend under the Data section when tags are used but unexplained
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
from string import Template

from . import checks as C
from .audit import Report, audit_repo
from .parse import TABLE_SEP_RE, Readme, github_slug, parse, resolve_relative, is_external
from .registry import Author, Project, Registry
from .repofacts import RepoFacts, collect

HERE = Path(__file__).resolve().parent.parent
BLOCKS = HERE / "blocks"

STATUS_COLORS = {"Complete": "brightgreen", "Maintained": "brightgreen", "Functional": "green",
                 "In development": "blue", "Foundation": "orange", "Prototype": "orange", "Archived": "lightgrey"}

LICENSE_TEXTS = {
    "MIT": "mit.txt", "Apache-2.0": "apache-2.0.txt", "ISC": "isc.txt",
}
PERMISSIVE_ALIASES = {"mit": "MIT", "mit license": "MIT", "apache-2.0": "Apache-2.0", "apache 2.0": "Apache-2.0", "apache": "Apache-2.0", "isc": "ISC"}


def block(block_name: str, **vars) -> str:
    text = (BLOCKS / f"{block_name}.md").read_text(encoding="utf-8")
    return Template(text).safe_substitute(**vars).rstrip("\n") + "\n"


def _shield(label: str, value: str, color: str) -> str:
    def enc(s: str) -> str:
        return s.replace("-", "--").replace("_", "__").replace(" ", "%20")
    return f"https://img.shields.io/badge/{enc(label)}-{enc(value)}-{color}"


class Fixer:
    def __init__(self, repo_dir: Path, project: Project, registry: Registry | None, manifest, dry_run: bool = False, fonts_dir=None):
        self.repo_dir = Path(repo_dir).resolve()
        self.project = project
        self.registry = registry
        self.manifest = manifest
        self.author: Author = registry.author if registry else Author()
        self.dry_run = dry_run
        self.fonts_dir = fonts_dir
        self.changes: list[str] = []
        self.readme_path = self.repo_dir / "README.md"

    # ------------------------------------------------------------ helpers
    def _read(self) -> str:
        return self.readme_path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n") if self.readme_path.exists() else ""

    def _write(self, text: str, why: str) -> None:
        if not text.endswith("\n"):
            text += "\n"
        if not self.dry_run:
            self.readme_path.write_text(text, encoding="utf-8", newline="\n")
        self.changes.append(why)

    def _facts(self) -> RepoFacts:
        return collect(self.repo_dir)

    def _insert_before_section(self, text: str, aliases, new_block: str, fallback_end: bool = True) -> str:
        rd = parse(text)
        targets = rd.find_sections(aliases, level=2, contains=False)
        if targets:
            line = targets[0].start
            lines = text.split("\n")
            return "\n".join(lines[:line]).rstrip("\n") + "\n\n" + new_block.rstrip("\n") + "\n\n" + "\n".join(lines[line:])
        if fallback_end:
            return text.rstrip("\n") + "\n\n" + new_block
        return text

    # ------------------------------------------------------------ fixes
    def fix_h1(self, text: str) -> str:
        rd = parse(text)
        if rd.h1 and "_" in rd.h1.title and self.project.title:
            lines = text.split("\n")
            lines[rd.h1.line] = f"# {self.project.title}"
            self.changes.append(f"identity.h1: '{rd.h1.title}' -> '{self.project.title}' (registry title)")
            return "\n".join(lines)
        if not rd.h1:
            title = self.project.title or re.sub(r"[-_]+", " ", self.project.name).title()
            self.changes.append(f"identity.h1: added H1 '{title}'")
            return f"# {title}\n\n" + text
        return text

    def fix_hero(self, text: str) -> str:
        rd = parse(text)
        if not rd.h1:
            return text
        hero_imgs = [im for im in rd.images if im.line < rd.first_h2_line]
        if hero_imgs and all(is_external(i.target) or (resolve_relative(self.repo_dir, self.readme_path, i.target) or Path("/nonexistent")).exists() for i in hero_imgs):
            return text
        declared = getattr(self.project, "hero", "generated") or "generated"
        if declared != "generated":
            target = declared
            if not (self.repo_dir / target).exists():
                self.changes.append(f"identity.hero: declared hero {target} does not exist; falling back to generated banner")
                declared = "generated"
        if declared == "generated":
            from .hero import generate, spec_from_project
            facts = self._facts()
            spec = spec_from_project(self.project, facts)
            target = getattr(self.project, "hero_path", "") or "docs/assets/hero.png"
            out = self.repo_dir / target
            if not self.dry_run:
                rep = generate(spec, out, fonts_dir=self.fonts_dir, report_path=out.with_suffix(".layout.json"))
                self.changes.append(f"identity.hero: generated {target} ({rep['fonts']}, title {rep['title_size']}px, {rep['attempts']} layout attempt(s), validated)")
            else:
                self.changes.append(f"identity.hero: would generate {target}")
        alt = f"{self.project.title or self.project.name} — {self.project.descriptor}".strip(" —") if self.project.descriptor else (self.project.title or self.project.name)
        alt = alt.replace("]", ")").replace("[", "(")
        line = f"![{alt}]({target})"
        lines = text.split("\n")
        # drop a broken hero image line if present
        for im in hero_imgs:
            if not is_external(im.target) and not (resolve_relative(self.repo_dir, self.readme_path, im.target) or Path("/nonexistent")).exists():
                if lines[im.line].strip().startswith("!["):
                    lines[im.line] = ""
                    self.changes.append(f"identity.hero: removed broken hero reference {im.target}")
        insert_at = rd.h1.line + 1
        lines[insert_at:insert_at] = ["", line]
        self.changes.append(f"identity.hero: inserted hero image reference {target}")
        return "\n".join(lines)

    def fix_badges(self, text: str) -> str:
        rd = parse(text)
        facts = self._facts()
        ident = rd.identity
        gh = self.project.github or ""
        new: list[str] = []
        if facts.ci_workflow and "actions/workflows" not in ident and gh:
            new.append(f"[![CI](https://github.com/{gh}/actions/workflows/{facts.ci_workflow}/badge.svg)](https://github.com/{gh}/actions/workflows/{facts.ci_workflow})")
        for wf in facts.workflows:
            low = wf.lower()
            if ("repro" in low or "governance" in low) and wf not in ident and gh:
                label = "Reproducibility" if "repro" in low else "Governance"
                new.append(f"[![{label}](https://github.com/{gh}/actions/workflows/{wf}/badge.svg)](https://github.com/{gh}/actions/workflows/{wf})")
        py = facts.python_requires or facts.python_version_file
        if py and not re.search(r"badge/python", ident, re.I):
            ver = re.sub(r"^[>=~^]+", "", py).strip()
            new.append(f"[![Python {ver}](https://img.shields.io/badge/python-{ver.replace('-', '--')}-blue)](pyproject.toml)" if facts.has_pyproject else f"[![Python {ver}](https://img.shields.io/badge/python-{ver}-blue)](.python-version)")
        elif facts.node_engine and not re.search(r"badge/node", ident, re.I):
            new.append(f"[![Node {facts.node_engine}](https://img.shields.io/badge/node-{facts.node_engine.replace('>=', '%3E%3D')}-green)](package.json)")
        if facts.license_file and not re.search(r"licen[cs]e", ident, re.I):
            new.append(f"[![License: {facts.license_id}]({_shield('license', facts.license_id, 'green')})]({facts.license_file.name})")
        elif facts.license_file and re.search(r"badge/licen[cs]e-([A-Za-z0-9.]+)", ident, re.I):
            m = re.search(r"badge/licen[cs]e-([A-Za-z0-9.]+)", ident, re.I)
            claimed = m.group(1)
            if claimed.lower() != C._license_name(facts.license_id).lower() and facts.license_id != "UNKNOWN":
                text = re.sub(r"\[!\[License:[^\]]*\]\([^)]*\)\]\([^)]*\)\s*\n?", "", text, count=1)
                rd = parse(text); ident = rd.identity
                new.append(f"[![License: {facts.license_id}]({_shield('license', facts.license_id, 'green')})]({facts.license_file.name})")
                self.changes.append(f"identity.badges: replaced license badge ({claimed} -> {facts.license_id})")
        if not facts.license_file and re.search(r"badge/licen[cs]e-", ident, re.I):
            text = re.sub(r"\[!\[License:[^\]]*\]\([^)]*\)\]\([^)]*\)\s*\n?", "", text, count=1)
            rd = parse(text); ident = rd.identity
            self.changes.append("identity.badges: removed license badge (no LICENSE file)")
        if self.project.status and not re.search(r"badge/status-", ident, re.I):
            st = self.project.status
            new.append(f"[![Status: {st}]({_shield('status', st, STATUS_COLORS.get(st, 'blue'))})](#status)")
        if not new:
            return text
        lines = text.split("\n")
        badge_lines = rd.badge_lines()
        if badge_lines:
            at = badge_lines[-1] + 1
        else:
            hero = [im for im in rd.images if im.line < rd.first_h2_line]
            at = (hero[0].line + 1) if hero else (rd.h1.line + 1 if rd.h1 else 0)
            # skip over a multi-line <p><img></p> block
            while at < len(lines) and lines[at].strip().startswith(("</p>", "</picture>", "/>", "<img", "src=", "alt=", "width=")):
                at += 1
            new = [""] + new
        lines[at:at] = new + ([""] if not badge_lines else [])
        self.changes.append(f"identity.badges: added {len([n for n in new if n])} badge(s)")
        return "\n".join(lines)

    def fix_status_line(self, text: str) -> str:
        st = self.project.status
        if not st:
            return text
        rd = parse(text)
        ident_lines = rd.identity_lines
        for i, l in enumerate(ident_lines):
            m = C.STATUS_LINE_RE.match(l)
            if m:
                if C._vocab_match(m.group(1), self.manifest.status_vocabulary) == st:
                    return text
                rest = l[m.end(1):]
                lines = text.split("\n")
                lines[i] = f"**Status:** {st}{rest}"
                self.changes.append(f"identity.status_line: '{m.group(1).strip()}' -> '{st}' (registry)")
                return "\n".join(lines)
        lines = text.split("\n")
        badge_lines = rd.badge_lines()
        if badge_lines:
            at = badge_lines[-1] + 1
        else:
            hero = [im for im in rd.images if im.line < rd.first_h2_line]
            at = (hero[0].line + 1) if hero else (rd.h1.line + 1 if rd.h1 else 0)
        lines[at:at] = ["", f"**Status:** {st}"]
        self.changes.append(f"identity.status_line: inserted '**Status:** {st}'")
        return "\n".join(lines)

    def fix_status_section(self, text: str) -> str:
        st = self.project.status
        if not st:
            return text
        facts = self._facts()
        date = facts.last_commit_date or _dt.date.today().isoformat()
        rd = parse(text)
        secs = rd.find_sections(C.STATUS_ALIASES, level=2, contains=False)
        if secs:
            s = secs[-1]
            lines = text.split("\n")
            body = s.body
            m = C.STATUS_LINE_RE.search(body)
            changed = False
            if m:
                term = C._vocab_match(m.group(1), self.manifest.status_vocabulary)
                if term != st:
                    for i in range(s.start + 1, s.end):
                        if C.STATUS_LINE_RE.match(lines[i]):
                            lines[i] = re.sub(r"(\**status\**\s*:\**\s*[*`]*)[A-Za-z][A-Za-z ]+?(?=[*`]*\s*(?:[·|(—-]|$))", rf"\g<1>{st}", lines[i], count=1, flags=re.I)
                            changed = True
                            break
            else:
                lines[s.start + 1:s.start + 1] = ["", f"**Status:** {st}"]
                changed = True
                s = parse("\n".join(lines)).find_sections(C.STATUS_ALIASES, level=2, contains=False)[-1]
            if not C.DATE_RE.search("\n".join(lines[s.start + 1:s.end])):
                lines[s.end:s.end] = [f"Repository last updated {date} (date of the last commit).", ""]
                changed = True
            if changed:
                self.changes.append(f"honesty.status_section: aligned Status section to '{st}' / added date")
                return "\n".join(lines)
            return text
        new = block("status", status=st, date=date)
        self.changes.append(f"honesty.status_section: inserted '## Status' ({st}, {date})")
        return self._insert_before_section(text, C.LICENSE_ALIASES | C.AUTHOR_ALIASES, new)

    # ---- license policy --------------------------------------------------
    def decide_license(self, facts: RepoFacts) -> tuple[str, str]:
        """Return (license_id, reason). Empty id means: do not create a file."""
        if facts.license_file:
            return facts.license_id, f"existing {facts.license_file.name}"
        if getattr(self.project, "license_blocked_reason", ""):
            return "", f"blocked: {self.project.license_blocked_reason}"
        override = (getattr(self.project, "license", "") or "").strip()
        if override:
            return PERMISSIVE_ALIASES.get(override.lower(), override), "registry override"
        declared = (facts.license_declared or "").strip()
        if declared:
            lid = PERMISSIVE_ALIASES.get(declared.lower(), declared)
            return lid, f"declared in {facts.license_declared_source}"
        readme = self._read()
        m = re.search(r"^##\s*Licen[cs]e.*?\n(.*?)(?=^## |\Z)", readme, re.S | re.M)
        if m and re.search(r"\bMIT\b", m.group(1)):
            return "MIT", "declared in README License section"
        if m and re.search(r"Apache", m.group(1)):
            return "Apache-2.0", "declared in README License section"
        if re.search(r"^\*\*Status:\*\*.*\bMIT\b", readme, re.M):
            return "MIT", "declared in README status line"
        return "MIT", "portfolio default (docs/LICENSE_POLICY.md §3): author-owned portfolio code, no third-party bundled material declared"

    def fix_license_file(self) -> None:
        facts = self._facts()
        if facts.license_file:
            return
        lid, reason = self.decide_license(facts)
        if not lid:
            self.changes.append(f"meta.license_file: BLOCKED_HUMAN — {reason}")
            return
        fname = LICENSE_TEXTS.get(lid)
        if not fname:
            self.changes.append(f"meta.license_file: BLOCKED_HUMAN — no canonical text for {lid}")
            return
        year = facts.first_commit_year or str(_dt.date.today().year)
        body = Template((BLOCKS / "licenses" / fname).read_text(encoding="utf-8")).safe_substitute(year=year, holder=self.author.name)
        if not self.dry_run:
            (self.repo_dir / "LICENSE").write_text(body, encoding="utf-8", newline="\n")
        self.changes.append(f"meta.license_file: created LICENSE ({lid}, {year}, {self.author.name}) — basis: {reason}")

    def fix_license_section(self, text: str) -> str:
        facts = self._facts()
        rd = parse(text)
        secs = rd.find_sections(C.LICENSE_ALIASES, level=2)
        if facts.license_file and facts.license_id != "UNKNOWN":
            wanted = block("license", license=facts.license_id, file=facts.license_file.name)
            name = C._license_name(facts.license_id)
            if secs and re.search(re.escape(name), secs[0].body, re.I):
                return text
            if secs:
                s = secs[0]
                lines = text.split("\n")
                body_end = s.end
                # keep extra provenance sentences (e.g. credits) that follow the first paragraph
                extra = [l for l in lines[s.start + 1:body_end] if l.strip() and not re.search(r"no `?licen[cs]e`? file|no licen|not licensed|source-available|unlicensed|pending an explicit|\b(MIT|Apache|ISC|BSD|GPL)\b|see \[?`?LICENSE", l, re.I)]
                repl = wanted.rstrip("\n").split("\n")
                if extra:
                    repl += [""] + extra
                lines[s.start:body_end] = repl + [""]
                self.changes.append(f"meta.license_section: rewritten to name {facts.license_id}")
                return "\n".join(lines)
            self.changes.append(f"meta.license_section: inserted '## License' ({facts.license_id})")
            return self._insert_before_section(text, C.AUTHOR_ALIASES, wanted)
        if not facts.license_file:
            wanted = block("license-none")
            if secs and re.search(r"no licen|not licensed|source-available|unlicensed", secs[0].body, re.I) and not re.search(r"\b(MIT|Apache|ISC)\b", secs[0].body):
                return text
            if secs:
                s = secs[0]
                lines = text.split("\n")
                lines[s.start:s.end] = wanted.rstrip("\n").split("\n") + [""]
                self.changes.append("meta.license_section: rewritten to state that no LICENSE file exists")
                return "\n".join(lines)
            self.changes.append("meta.license_section: inserted truthful no-license section")
            return self._insert_before_section(text, C.AUTHOR_ALIASES, wanted)
        return text

    def fix_author(self, text: str) -> str:
        a = self.author
        wanted = block("author", name=a.name, place=a.place, year=a.year, linkedin=a.linkedin, email=a.email)
        rd = parse(text)
        secs = rd.find_sections(C.AUTHOR_ALIASES, level=2)
        if secs:
            s = secs[-1]
            if all(x in s.body for x in (a.name, a.location, str(a.year), a.linkedin)):
                return text
            lines = text.split("\n")
            lines[s.start:s.end] = wanted.rstrip("\n").split("\n") + [""]
            self.changes.append("meta.author: replaced author block with the canonical block")
            return "\n".join(lines)
        self.changes.append("meta.author: appended canonical author block")
        return text.rstrip("\n") + "\n\n" + wanted

    def fix_repo_structure(self, text: str) -> str:
        facts = self._facts()
        rd = parse(text)
        if rd.find_sections(C.STRUCTURE_ALIASES):
            return text
        rows = []
        for name, is_dir, count in facts.top_level[:16]:
            if name.startswith("."):
                continue
            rows.append(f"{name + '/' if is_dir else name:<28}{(str(count) + ' files') if is_dir else ''}".rstrip())
        if len([r for r in rows if r.endswith("files")]) < 2:
            return text
        new = block("structure", tree="\n".join(rows))
        self.changes.append("technical.structure: inserted factual top-level tree (names and file counts only)")
        return self._insert_before_section(text, C.STATUS_ALIASES | C.LICENSE_ALIASES | C.AUTHOR_ALIASES, new)

    def fix_paths(self, text: str) -> str:
        facts = self._facts()
        idx = facts.basename_index()
        rd = parse(text)
        replaced = 0
        for ref in list(rd.images) + list(rd.links):
            t = ref.target.strip()
            if is_external(t) or t.startswith("#") or not t:
                continue
            p = resolve_relative(self.repo_dir, self.readme_path, t)
            if p is None or p.exists():
                continue
            base = Path(t.split("#")[0]).name.lower()
            cands = idx.get(base, [])
            if len(cands) == 1:
                newrel = cands[0].relative_to(self.repo_dir).as_posix()
                text = text.replace(f"({t})", f"({newrel})").replace(f'"{t}"', f'"{newrel}"').replace(f"'{t}'", f"'{newrel}'")
                self.changes.append(f"links: repaired {t} -> {newrel}")
                replaced += 1
        return text

    def fix_audience_links(self, text: str) -> str:
        rd = parse(text)
        secs = rd.find_sections(C.AUDIENCE_ALIASES, level=2)
        if not secs:
            return text
        s = secs[0]
        lines = text.split("\n")
        heads = [(h.title, h.slug) for h in rd.headings if h.level == 2]
        changed = 0
        for i in range(s.start + 1, s.end):
            l = lines[i]
            if not l.strip().startswith("|") or TABLE_SEP_RE.match(l):
                continue
            if re.search(r"\]\(|`[^`]+`|#[a-z]", l):
                continue
            cells = l.split("|")
            if len(cells) < 3:
                continue
            target_cell = cells[-2]
            new_cell = target_cell
            for title, slug in sorted(heads, key=lambda x: -len(x[0])):
                if title.lower() in new_cell.lower() and f"(#{slug})" not in new_cell:
                    new_cell = re.sub(re.escape(title), f"[{title}](#{slug})", new_cell, count=1, flags=re.I)
            if new_cell != target_cell:
                cells[-2] = new_cell
                lines[i] = "|".join(cells)
                changed += 1
        if changed:
            self.changes.append(f"navigation.audience: linked {changed} audience row(s) to their sections")
        return "\n".join(lines)

    def fix_epistemic_legend(self, text: str) -> str:
        rd = parse(text)
        tags = self.manifest.epistemic_tags
        if not any(re.search(rf"\b{t}\b", rd.prose_text) for t in tags):
            return text
        if re.search(r"\|\s*`?(VERIFIED|CALIBRATED|SIMULATED|ILLUSTRATIVE)`?\s*\|", rd.prose_text) or re.search(r"epistemic_boundaries|Tag \| Meaning", rd.prose_text):
            return text
        secs = rd.find_sections(C.DATA_ALIASES, level=2)
        if not secs:
            return text
        s = secs[0]
        lines = text.split("\n")
        legend = block("epistemic-legend").rstrip("\n").split("\n")
        lines[s.start + 1:s.start + 1] = [""] + legend
        self.changes.append("analytical.epistemic: inserted the tag legend under the Data section")
        return "\n".join(lines)

    # ------------------------------------------------------------ driver
    def run(self, max_rounds: int = 3) -> tuple[Report, list[str]]:
        report = audit_repo(self.repo_dir, self.project, self.manifest, self.registry)
        if report.readme is None:
            self.changes.append("readme.exists: no README — create one from templates/<type>.md (not auto-generated: prose needs repository evidence)")
            return report, self.changes
        for _ in range(max_rounds):
            failing = {f.id for f in report.findings if f.status in (C.FAIL, C.BLOCKED)}
            if not failing:
                break
            text = self._read()
            before = text
            if "identity.h1" in failing:
                text = self.fix_h1(text)
            if "identity.hero" in failing:
                text = self.fix_hero(text)
            if "meta.license_file" in failing:
                self.fix_license_file()
            if "identity.badges" in failing:
                text = self.fix_badges(text)
            if "identity.status_line" in failing:
                text = self.fix_status_line(text)
            if "honesty.status_section" in failing:
                text = self.fix_status_section(text)
            if "meta.license_section" in failing or "meta.license_file" in failing:
                text = self.fix_license_section(text)
            if "meta.author" in failing:
                text = self.fix_author(text)
            if "technical.structure" in failing:
                text = self.fix_repo_structure(text)
            if "links.images" in failing or "links.internal" in failing or "identity.hero" in failing:
                text = self.fix_paths(text)
            if "navigation.audience" in failing:
                text = self.fix_audience_links(text)
            if "analytical.epistemic" in failing:
                text = self.fix_epistemic_legend(text)
            if text != before:
                self._write(text, "README.md updated")
            report = audit_repo(self.repo_dir, self.project, self.manifest, self.registry)
            still = {f.id for f in report.findings if f.status in (C.FAIL, C.BLOCKED)}
            if still == failing and text == before:
                break
        return report, self.changes
