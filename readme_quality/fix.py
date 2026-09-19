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


def _identity_blocks(lines: list[str]) -> list[dict]:
    """Split the identity zone (after the H1, before the first H2) into typed blocks."""
    from .parse import BADGE_RE, HTML_IMG_RE, MD_IMG_RE
    blocks: list[dict] = []
    i = 0
    n = len(lines)

    def caption_after(j: int) -> tuple[list[str], int]:
        k = j
        while k < n and not lines[k].strip():
            k += 1
        if k < n and lines[k].strip().startswith(("*", "_")) and not lines[k].strip().startswith("**"):
            cap = []
            while k < n and lines[k].strip():
                cap.append(lines[k])
                k += 1
            if cap and cap[-1].rstrip().endswith(("*", "_", "*)", ".*")):
                return cap, k
        return [], j

    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while j < n and not lines[j].strip().startswith("```"):
                j += 1
            blocks.append({"kind": "fence", "lines": lines[i:j + 1]})
            i = j + 1
            continue
        if C.STATUS_LINE_RE.match(s):
            blocks.append({"kind": "status", "lines": [lines[i]]})
            i += 1
            continue
        if BADGE_RE.search(s):
            j = i
            while j < n and lines[j].strip() and BADGE_RE.search(lines[j]):
                j += 1
            blocks.append({"kind": "badges", "lines": lines[i:j]})
            i = j
            continue
        m = MD_IMG_RE.search(s)
        if m and s.startswith("!["):
            cap, k = caption_after(i + 1)
            blocks.append({"kind": "image", "target": m.group(2), "lines": [lines[i]] + ([""] + cap if cap else [])})
            i = k if cap else i + 1
            continue
        if s.startswith(("<p", "<picture", "<div", "<img", "<a ")):
            j = i
            while j < n:
                if re.search(r"</p>|</picture>|</div>|</a>", lines[j]) or (s.startswith("<img") and lines[j].rstrip().endswith(">")):
                    break
                j += 1
            j = min(j, n - 1)
            html = "\n".join(lines[i:j + 1])
            mm = HTML_IMG_RE.search(html)
            cap, k = caption_after(j + 1)
            blocks.append({"kind": "html", "target": mm.group(1) if mm else "", "lines": lines[i:j + 1] + ([""] + cap if cap else [])})
            i = k if cap else j + 1
            continue
        if s.startswith("<!--") or s in ("---", "***"):
            blocks.append({"kind": "other", "lines": [lines[i]]})
            i += 1
            continue
        j = i
        while j < n and lines[j].strip() and not lines[j].strip().startswith(("```", "![", "<p", "<picture", "<img", "[![")) and not C.STATUS_LINE_RE.match(lines[j].strip()):
            j += 1
        if j == i:
            j = i + 1
        blocks.append({"kind": "prose", "lines": lines[i:j]})
        i = j
    return blocks


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

    # ---- banner + identity order --------------------------------------------
    def _banner_target(self) -> str:
        return C.banner_target(self.project)

    def ensure_banner_file(self) -> str:
        """Make sure the vanity banner exists (generate it when declared as `generated`)."""
        b = getattr(self.project, "banner", "generated") or "generated"
        target = self._banner_target()
        if b != "generated" and not (self.repo_dir / target).exists():
            self.changes.append(f"identity.hero: declared banner {target} does not exist; generating the design-system banner instead")
            target = getattr(self.project, "banner_path", "") or "docs/assets/hero.png"
            b = "generated"
        if b == "generated" and not (self.repo_dir / target).exists():
            from .hero import generate, spec_from_project
            spec = spec_from_project(self.project, self._facts())
            out = self.repo_dir / target
            if not self.dry_run:
                rep = generate(spec, out, fonts_dir=self.fonts_dir, report_path=out.with_suffix(".layout.json"))
                self.changes.append(f"identity.hero: generated {target} ({rep['fonts']}, title {rep['title_size']}px, validated)")
            else:
                self.changes.append(f"identity.hero: would generate {target}")
        return target

    def regenerate_banner(self) -> None:
        """Force a fresh generated banner (used after generator changes)."""
        if (getattr(self.project, "banner", "generated") or "generated") != "generated":
            return
        from .hero import generate, spec_from_project
        target = self._banner_target()
        out = self.repo_dir / target
        if not self.dry_run:
            rep = generate(spec_from_project(self.project, self._facts()), out, fonts_dir=self.fonts_dir, report_path=out.with_suffix(".layout.json"))
            self.changes.append(f"identity.hero: regenerated {target} ({rep['fonts']}, title {rep['title_size']}px, validated)")

    def fix_hero(self, text: str) -> str:
        """Banner first, then badges, then the status line, then prose, then every other visual."""
        rd = parse(text)
        if not rd.h1:
            return text
        target = self.ensure_banner_file()
        lines = text.split("\n")
        end = rd.first_h2_line
        ident = lines[rd.h1.line + 1:end]
        blocks = _identity_blocks(ident)
        want = C._norm(target)
        banner_block = None
        for b in blocks:
            if b["kind"] == "image" and C._norm(b["target"]) == want:
                banner_block = b
                break
        if banner_block is None:
            alt = f"{self.project.title or self.project.name}: {self.project.descriptor}".strip(": ") if self.project.descriptor else (self.project.title or self.project.name)
            alt = alt.replace("]", ")").replace("[", "(")
            banner_block = {"kind": "image", "target": target, "lines": [f"![{alt}]({target})"]}
            self.changes.append(f"identity.hero: inserted banner reference {target}")
        badges = [b for b in blocks if b["kind"] == "badges"]
        status = [b for b in blocks if b["kind"] == "status"]
        prose = [b for b in blocks if b["kind"] == "prose"]
        visuals = [b for b in blocks if b["kind"] in ("image", "html", "fence") and b is not banner_block]
        other = [b for b in blocks if b["kind"] == "other"]
        kept = []
        for b in visuals:
            tgt = b.get("target")
            if b["kind"] == "image" and tgt and not is_external(tgt) and not (resolve_relative(self.repo_dir, self.readme_path, tgt) or Path("/nonexistent")).exists():
                self.changes.append(f"identity.hero: removed broken image reference {tgt}")
                continue
            kept.append(b)
        order = [banner_block] + badges + status + prose + kept + other
        out: list[str] = []
        for b in order:
            out.extend(b["lines"])
            out.append("")
        rebuilt = lines[:rd.h1.line + 1] + [""] + out + lines[end:]
        new_text = "\n".join(rebuilt)
        new_text = re.sub(r"\n{3,}", "\n\n", new_text)
        if new_text != text:
            self.changes.append("identity.hero: identity zone reordered (banner, badges, status, prose, other visuals)")
        return new_text

    def fix_badges(self, text: str) -> str:
        rd = parse(text)
        facts = self._facts()
        ident = rd.identity
        gh = self.project.github or ""
        new: list[str] = []
        if facts.ci_workflow and not re.search(r"actions/workflows|img\.shields\.io/github/(check-runs|actions)|/actions\)", ident) and gh:
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
        self.ensure_notice()

    def ensure_notice(self) -> None:
        text = (getattr(self.project, "license_notice", "") or "").strip()
        if not text:
            return
        dst = self.repo_dir / "NOTICE"
        if dst.exists():
            return
        if not self.dry_run:
            dst.write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")
        self.changes.append("meta.license_file: created NOTICE (third-party material excluded from the grant)")

    def fix_license_section(self, text: str) -> str:
        facts = self._facts()
        rd = parse(text)
        secs = rd.find_sections(C.LICENSE_ALIASES, level=2)
        if facts.license_file and facts.license_id != "UNKNOWN":
            self.ensure_notice()
            wanted = block("license", license=facts.license_id, file=facts.license_file.name)
            if (self.repo_dir / "NOTICE").exists():
                wanted = wanted.rstrip("\n") + " Third-party material bundled in this repository is listed in [`NOTICE`](NOTICE) and is not covered by that grant.\n"
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

    def ensure_portrait(self) -> str:
        a = self.author
        photo = getattr(a, "photo", "Author_MDS_Rafael_Braga-Kribitz_kroped.png")
        dst = self.repo_dir / "docs" / "assets" / photo
        if not dst.exists():
            src = BLOCKS / "assets" / photo
            if src.exists() and not self.dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src.read_bytes())
                self.changes.append(f"meta.author: vendored portrait to docs/assets/{photo}")
        return f"docs/assets/{photo}"

    def fix_author(self, text: str) -> str:
        a = self.author
        photo_rel = self.ensure_portrait()
        wanted = block("author", name=a.name, place=a.place, year=a.year, linkedin=a.linkedin, email=a.email, photo=photo_rel)
        rd = parse(text)
        secs = rd.find_sections(C.AUTHOR_ALIASES, level=2)
        if secs:
            s = secs[-1]
            if all(x in s.body for x in (a.name, a.location, str(a.year), a.linkedin)) and photo_rel.split("/")[-1] in s.body:
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
