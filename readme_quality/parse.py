"""Markdown README parser: headings, sections, identity zone, images, links, fences.

Also computes the *rendered* line count used by `meta.length`: the lines a reader
actually sees, which is not the same as the number of lines in the file. A fenced
Mermaid block renders as one figure and an HTML claim comment renders as nothing,
so neither is counted; `meta.length_total` keeps the raw file size in check instead.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^(```+|~~~+)\s*([A-Za-z0-9_+-]*)")
MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_IMG_RE = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"'][^>]*>", re.I | re.S)
HTML_ALT_RE = re.compile(r"\balt\s*=\s*[\"']([^\"']*)[\"']", re.I)
HTML_SRCSET_RE = re.compile(r"<source\b[^>]*?\bsrcset\s*=\s*[\"']([^\"'\s,]+)", re.I)
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_A_RE = re.compile(r"<a\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)[\"']", re.I)
BADGE_RE = re.compile(r"img\.shields\.io|/badge\.svg|badge/", re.I)
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
OPEN_COMMENT_RE = re.compile(r"<!--(?:(?!-->).)*$", re.S)
LINKED_IMG_RE = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)")
HTML_ANCHOR_BLOCK_RE = re.compile(r"<a\s[^>]*>.*?</a>", re.I | re.S)
MERMAID_CLICK_RE = re.compile(r"^\s*click\s+(\S+)\s+[\"']([^\"']+)[\"']", re.M)
GITHUB_BLOB_RE = re.compile(r"^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/(?:blob|tree)/[^/]+/(.+?)/?$", re.I)


def normalize_heading(title: str) -> str:
    t = re.sub(r"`+", "", title)
    t = re.sub(r"\*+", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s'+.&/-]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def github_slug(title: str) -> str:
    """Approximation of GitHub's heading anchor algorithm."""
    t = re.sub(r"`+", "", title)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)  # keep word chars, hyphen, space
    t = t.replace(" ", "-")
    return t


@dataclass
class Heading:
    level: int
    title: str
    norm: str
    line: int  # 0-based line index

    @property
    def slug(self) -> str:
        return github_slug(self.title)


@dataclass
class Section:
    heading: Heading
    start: int  # line index of heading
    end: int    # exclusive line index
    body_lines: list[str]

    @property
    def body(self) -> str:
        return "\n".join(self.body_lines)

    @property
    def norm(self) -> str:
        return self.heading.norm

    @property
    def level(self) -> int:
        return self.heading.level


@dataclass
class Fence:
    lang: str
    body: str
    line: int


@dataclass
class ImageRef:
    alt: str
    target: str
    line: int


@dataclass
class LinkRef:
    text: str
    target: str
    line: int


@dataclass
class Readme:
    path: Path | None
    text: str
    lines: list[str] = field(default_factory=list)
    headings: list[Heading] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    fences: list[Fence] = field(default_factory=list)
    images: list[ImageRef] = field(default_factory=list)
    links: list[LinkRef] = field(default_factory=list)
    masked_lines: list[str] = field(default_factory=list)  # fences blanked out
    fence_line_flags: list[bool] = field(default_factory=list)

    # ---- derived ---------------------------------------------------------
    @property
    def first_h2_line(self) -> int:
        for h in self.headings:
            if h.level == 2:
                return h.line
        return len(self.lines)

    @property
    def identity_lines(self) -> list[str]:
        return self.lines[: self.first_h2_line]

    @property
    def identity(self) -> str:
        return "\n".join(self.identity_lines)

    @property
    def masked_text(self) -> str:
        return "\n".join(self.masked_lines)

    @property
    def prose_text(self) -> str:
        """Text without code fences and without HTML comments."""
        return re.sub(r"<!--.*?-->", " ", self.masked_text, flags=re.S)

    @property
    def h1(self) -> Heading | None:
        for h in self.headings:
            if h.level == 1:
                return h
        return None

    @property
    def h2_sections(self) -> list[Section]:
        return [s for s in self.sections if s.level == 2]

    def find_sections(self, aliases, level: int | None = None, contains: bool = True) -> list[Section]:
        """Sections whose normalized heading equals or contains one of the aliases."""
        out = []
        for s in self.sections:
            if level and s.level != level:
                continue
            n = s.norm
            for a in aliases:
                a = a.lower()
                if n == a or (contains and a in n):
                    out.append(s)
                    break
        return out

    def has_section(self, aliases, level: int | None = None, contains: bool = True) -> bool:
        return bool(self.find_sections(aliases, level, contains))

    def section_for_line(self, line: int) -> Section | None:
        for s in self.sections:
            if s.start <= line < s.end:
                return s
        return None

    def images_in(self, start: int, end: int) -> list[ImageRef]:
        return [i for i in self.images if start <= i.line < end]

    def fences_in(self, start: int, end: int) -> list[Fence]:
        return [f for f in self.fences if start <= f.line < end]

    def badge_lines(self) -> list[int]:
        return [i for i, l in enumerate(self.identity_lines) if BADGE_RE.search(l)]

    @property
    def rendered_lines(self) -> list[int]:
        """Indices of the lines a reader actually sees rendered (see `rendered_line_numbers`)."""
        return rendered_line_numbers(self)

    @property
    def rendered_line_count(self) -> int:
        return len(self.rendered_lines)

    def mermaid_clicks(self) -> list[tuple[str, str, int]]:
        """(node_id, target, line) for every `click` line in a ```mermaid fence."""
        out: list[tuple[str, str, int]] = []
        for f in self.fences:
            if f.lang != "mermaid":
                continue
            for i, line in enumerate(f.body.split("\n")):
                m = MERMAID_CLICK_RE.match(line)
                if m:
                    out.append((m.group(1), m.group(2), f.line + 1 + i))
        return out

    def tables_in(self, start: int, end: int) -> list[tuple[int, int]]:
        """(header_line, n_body_rows) for pipe tables between start and end."""
        out = []
        i = start
        while i < end - 1:
            if self.masked_lines[i].strip().startswith("|") and TABLE_SEP_RE.match(self.masked_lines[i + 1]):
                j = i + 2
                while j < end and self.masked_lines[j].strip().startswith("|"):
                    j += 1
                out.append((i, j - i - 2))
                i = j
            else:
                i += 1
        return out


def _html_alt(tag: str) -> str:
    """The `alt` attribute of an <img> tag, empty when absent."""
    m = HTML_ALT_RE.search(tag)
    return m.group(1).strip() if m else ""


def strip_badge_constructs(line: str) -> str:
    """Remove the markdown/HTML constructs on a line whose target is a badge shield."""
    def drop(m: re.Match) -> str:
        return "" if BADGE_RE.search(m.group(0)) else m.group(0)
    line = LINKED_IMG_RE.sub(drop, line)          # [![alt](shield)](link)
    line = MD_IMG_RE.sub(drop, line)              # ![alt](shield)
    line = HTML_ANCHOR_BLOCK_RE.sub(drop, line)   # <a href=…><img src=shield …></a>
    line = HTML_IMG_RE.sub(drop, line)            # <img src=shield …>
    return line


def is_badge_only(line: str) -> bool:
    """True when a line carries badge shields and nothing else that renders."""
    s = line.strip()
    return bool(s) and bool(BADGE_RE.search(s)) and not strip_badge_constructs(s).strip()


def comment_masked_lines(masked_lines: list[str]) -> list[str]:
    """`masked_lines` with HTML comment spans blanked out, line numbering preserved."""
    def blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    text = COMMENT_RE.sub(blank, "\n".join(masked_lines))
    return OPEN_COMMENT_RE.sub(blank, text).split("\n")


def rendered_line_numbers(rd: Readme) -> list[int]:
    """Indices of the lines that render as prose, headings, list items, tables or images.

    Excluded: fenced code blocks and their ``` delimiters (a Mermaid graph renders as one
    figure, not as its source), HTML comment lines (claim comments render as nothing),
    badge-only lines, and blank lines. This is what `meta.length` measures; the raw file
    length is measured separately by `meta.length_total`.
    """
    nocomment = comment_masked_lines(rd.masked_lines)
    out: list[int] = []
    for i in range(len(rd.masked_lines)):
        if i < len(rd.fence_line_flags) and rd.fence_line_flags[i]:
            continue
        s = nocomment[i].strip() if i < len(nocomment) else ""
        if not s or is_badge_only(s):
            continue
        out.append(i)
    return out


def parse(text: str, path: Path | None = None) -> Readme:
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    rd = Readme(path=path, text=text, lines=lines)

    # fences
    in_fence = False
    fence_marker = ""
    fence_lang = ""
    fence_start = 0
    fence_body: list[str] = []
    masked: list[str] = []
    flags: list[bool] = []
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if not in_fence and m:
            in_fence = True
            fence_marker = m.group(1)[0] * 3
            fence_lang = (m.group(2) or "").lower()
            fence_start = i
            fence_body = []
            masked.append("")
            flags.append(True)
            continue
        if in_fence and line.strip().startswith(fence_marker):
            in_fence = False
            rd.fences.append(Fence(fence_lang, "\n".join(fence_body), fence_start))
            masked.append("")
            flags.append(True)
            continue
        if in_fence:
            fence_body.append(line)
            masked.append("")
            flags.append(True)
        else:
            masked.append(line)
            flags.append(False)
    if in_fence:  # unterminated fence: treat rest as fence
        rd.fences.append(Fence(fence_lang, "\n".join(fence_body), fence_start))
    rd.masked_lines = masked
    rd.fence_line_flags = flags

    # headings (outside fences)
    for i, line in enumerate(masked):
        m = HEADING_RE.match(line)
        if m:
            rd.headings.append(Heading(len(m.group(1)), m.group(2).strip(), normalize_heading(m.group(2)), i))

    # sections: each heading owns lines until the next heading of same or higher level
    for idx, h in enumerate(rd.headings):
        end = len(lines)
        for nxt in rd.headings[idx + 1:]:
            if nxt.level <= h.level:
                end = nxt.line
                break
        rd.sections.append(Section(h, h.line, end, lines[h.line + 1:end]))

    # images and links (outside fences, comments kept because <img> may be inside HTML)
    for i, line in enumerate(masked):
        for m in MD_IMG_RE.finditer(line):
            rd.images.append(ImageRef(m.group(1), m.group(2), i))
        for m in HTML_IMG_RE.finditer(line):
            rd.images.append(ImageRef(_html_alt(m.group(0)), m.group(1), i))
        for m in HTML_SRCSET_RE.finditer(line):
            rd.images.append(ImageRef("", m.group(1), i))
        for m in MD_LINK_RE.finditer(line):
            tgt = m.group(2)
            if BADGE_RE.search(tgt) or m.group(1).startswith("!["):
                pass
            rd.links.append(LinkRef(m.group(1), tgt, i))
        for m in HTML_A_RE.finditer(line):
            rd.links.append(LinkRef("", m.group(1), i))
    # multi-line <img ...> tags: scan the joined text once more
    joined = "\n".join(masked)
    seen = {(im.target, im.line) for im in rd.images}
    for m in HTML_IMG_RE.finditer(joined):
        line_no = joined.count("\n", 0, m.start())
        if (m.group(1), line_no) not in seen and not any(im.target == m.group(1) for im in rd.images):
            rd.images.append(ImageRef(_html_alt(m.group(0)), m.group(1), line_no))
    rd.images.sort(key=lambda x: x.line)
    return rd


def parse_file(path: Path) -> Readme:
    return parse(Path(path).read_text(encoding="utf-8", errors="replace"), Path(path))


def find_readme(repo_dir: Path) -> Path | None:
    for cand in ("README.md", "readme.md", "Readme.md", "README.MD", "README.rst", "README"):
        p = Path(repo_dir) / cand
        if p.is_file():
            return p
    return None


def is_external(target: str) -> bool:
    t = target.strip().lower()
    return t.startswith(("http://", "https://", "mailto:", "tel:", "ftp://", "//", "data:"))


def resolve_relative(repo_dir: Path, readme_path: Path, target: str) -> Path | None:
    """Resolve a relative README reference to a filesystem path (None if external/anchor)."""
    t = target.strip()
    if is_external(t) or t.startswith("#") or not t:
        return None
    t = t.split("#", 1)[0].split("?", 1)[0]
    try:
        from urllib.parse import unquote
        t = unquote(t)
    except Exception:  # pragma: no cover
        pass
    if t.startswith("/"):
        return (Path(repo_dir) / t.lstrip("/")).resolve()
    base = Path(readme_path).parent if readme_path else Path(repo_dir)
    return (base / t).resolve()
