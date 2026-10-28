"""One sentence model for README prose: used by the `prose` command and by three checks.

The model reads Markdown and keeps only what a reader reads as sentences. Code (fenced and
indented), tables, headings, badges and link lists are dropped first. The remaining lines are joined
into blocks: a paragraph or a list item (with its wrapped continuation lines) is one block, and a
blank line, a new list item, a heading, a table, a code block, an HTML block or a hard line break
(two trailing spaces, a backslash, `<br>`) ends it. Each block is joined before it is split into
sentences, so hard-wrapping the source does not change the measurement. The model then measures
sentence length, a passive-voice heuristic, bare internal codes and whether the opening names a role
that decides. Pure functions, no I/O, standard library only.

Measurement, not judgement: the gate uses sentence length (`plain_language`), the code list
(`no_internal_codes`) and the decision owner (`decision_owner`). The passive-voice figure is a
heuristic that only the `prose` command reports.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

LONG_WORDS = 25      # a sentence with more words than this is "long"
MIN_WORDS = 3        # shorter fragments are not sentences

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
QUOTE_PREFIX_RE = re.compile(r"^(?:\s*>\s?)+")
LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
TAG_ONLY_RE = re.compile(r"(?:\s*</?[A-Za-z][^>]*>)+\s*")
TAG_START_RE = re.compile(r"</?[A-Za-z]")
TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
LINKED_IMG_RE = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)|\[!\[[^\]]*\]\([^)]*\)\]\[[^\]]*\]")
IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)|!\[[^\]]*\]\[[^\]]*\]")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
REF_LINK_RE = re.compile(r"\[([^\]]+)\]\[[^\]]*\]")
LINK_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*\S+")
LINK_ONLY_RE = re.compile(r"(?:\[[^\]]*\]\([^)]*\)[\s·|,/–-]*)+")
URL_RE = re.compile(r"<?https?://[^\s>)]+>?")
CODE_SPAN_RE = re.compile(r"(`+)(?!`).+?(?<!`)\1(?!`)")
LIST_RE = re.compile(r"^(?:[-*+]|\d+[.)])\s+")
CHECKBOX_RE = re.compile(r"^\[[ xX]\]\s+")
ALERT_RE = re.compile(r"^\[!\w+\]$")
HR_RE = re.compile(r"^(?:[-*_]\s*){3,}$|^=+$")
HARD_BREAK_RE = re.compile(r"(?:\\|<br\s*/?>)\s*$|  $", re.I)
EMPH_RE = re.compile(r"\*+|(?<!\w)_+|_+(?!\w)")
COMMENT_RE = re.compile(r"<!--.*?-->")

ABBREVIATIONS = ("e.g.", "i.e.", "vs.", "etc.", "fig.", "no.", "approx.", "ca.", "dr.", "st.", "cf.", "al.")
SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“‘(\[])")

# Heuristic, not grammar: a form of "to be" followed by a regular or common irregular participle.
PASSIVE_RE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+(\w+ed|\w+en|built|made|done|shown|given|taken|kept|held|run|set|put|read"
    r"|written|found|known|seen|drawn|chosen|hidden|sent|left|met|cut|split|spent|won|lost|bought|sold|paid|led)\b",
    re.I,
)

# ---- internal codes -----------------------------------------------------------
CODE_PATTERNS = (
    r"\b[A-Z]{1,3}-\d{2,4}\b",                                   # F-222, D-026, OQ-02, ADR-001
    r"\bBQ\d{1,2}\b",                                            # BQ45
    r"\bS\d_\d{2}\b",                                            # S1_03
    r"\bS-[a-z]+(?:-[a-z]+)+\b",                                 # S-pricing-tier
    r"\bLayer\s+(?:\d|[A-Z])(?:/(?:\d|[A-Z]))*\b(?![\w/])",       # Layer 2, Layer P, Layer 1/2/3
    r"\bModule\s+[A-Z]\b(?!\w)",                                 # Module A
    r"\b[A-Z]{1,2}\d{1,2}[a-z]?_[A-Za-z]\w*\b",                  # C1_forecast_timeline
)
CODE_RES = tuple(re.compile(p) for p in CODE_PATTERNS)
CODE_ALLOWLIST = {"ISO", "UTF", "RFC", "SHA", "COVID", "DIN", "IEC", "EN", "CVE", "GPT", "MD", "ASD", "STE", "A"}
LEGEND_RE = re.compile(r"legend|glossary", re.I)

# ---- decision owner -----------------------------------------------------------
ROLE_TERMS = (
    r"head of \w+", r"chief \w+ officer", "CFO", "CMO", "CEO", "COO", "CTO", "CIO", "director", "manager", "lead",
    "analyst", "buyer", "controller", "planner", "owner", "engineer", "scientist", "officer", "recruiter", "team",
    "job seeker", "candidate", "campaign", "operator", "operations", "procurement", "marketing", "finance",
    "maintainer", "founder", "stakeholder", r"decision[- ]makers?", "hiring manager", "data team", "product",
    "developer", "practitioner", "researcher", "editor", "strategist", r"reader who", r"anyone who",
)
DECISION_TERMS = (
    r"decid(?:e|es)", "decision", r"choos(?:e|es)", "choice", "selects?", "allocates?", "picks?", "invests?",
    "buys?", "hedges?", "targets?", "applies|apply", "moves?", "commits?", "prioriti[sz]es?", "approves?",
    r"signs? off", "adopts?", r"which\b.{0,60}?\bfirst",
)
ROLE_RE = re.compile(r"\b(?:" + "|".join(ROLE_TERMS) + r")s?\b", re.I)
DECISION_RE = re.compile(r"\b(?:" + "|".join(DECISION_TERMS) + r")\b", re.I)


@dataclass
class Sentence:
    line: int
    text: str
    words: int
    passive: bool


@dataclass
class ProseStats:
    n_sentences: int
    n_long: int
    long_share: float
    n_passive: int
    passive_share: float
    n_ste_ok: int
    ste_share: float


@dataclass
class CodeHit:
    line: int
    code: str


@dataclass
class DecisionOwner:
    role: str
    verb: str
    line: int


@dataclass
class _Line:
    no: int
    text: str
    legend: bool      # inside a section whose heading holds "legend" or "glossary"
    lead: bool        # before the first H2
    new_block: bool   # starts a new paragraph, list item or quote block


def _clean(s: str) -> str:
    """One prose line: markers, links, code spans and emphasis reduced to the words a reader sees."""
    s = CODE_SPAN_RE.sub("x", s)
    s = LINKED_IMG_RE.sub("", s)
    s = IMG_RE.sub("", s)
    s = LINK_RE.sub(r"\1", s)
    s = REF_LINK_RE.sub(r"\1", s)
    s = URL_RE.sub("", s)
    s = TAG_RE.sub(" ", s)
    s = EMPH_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def _fence_of(raw: str):
    """(delimiter run, info string, inside a blockquote) when the line is a fence, else None.

    Blockquote markers and a list marker are container prefixes: they are removed first. A backtick
    fence whose info string holds a backtick is inline code, not a fence."""
    inner = QUOTE_PREFIX_RE.sub("", raw)
    for cand in (inner, LIST_PREFIX_RE.sub("", inner)):
        m = FENCE_RE.match(cand)
        if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
            return m.group(1), m.group(2), inner != raw
    return None


def _walk(text: str) -> list[_Line]:
    """The prose lines of a Markdown text, each marked with whether it starts a new block."""
    out: list[_Line] = []
    fence = None        # (character, length, opened inside a blockquote) while inside a fenced block
    in_comment = in_tag = seen_h2 = html = icode = prev_quote = prev_hard = False
    legend_level = 0
    list_ctx = None     # content column of the current list item, None outside a list
    kind = "blank"      # what the previous source line was: blank | prose | other
    for no, raw in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
        f = _fence_of(raw)
        if fence:
            if fence[2] and not raw.lstrip().startswith(">"):
                fence = None            # the blockquote that held the fence has ended
            else:
                if f and f[0][0] == fence[0] and len(f[0]) >= fence[1] and not f[1].strip():
                    fence = None        # a closing fence: same character, at least as long, no info string
                continue
        if f:
            fence, kind, icode = (f[0][0], len(f[0]), f[2]), "other", False
            continue
        line = raw
        if in_comment:
            if "-->" not in line:
                continue
            line, in_comment = line.split("-->", 1)[1], False
        line = COMMENT_RE.sub(" ", line)
        if "<!--" in line:
            line, in_comment = line.split("<!--", 1)[0], True
        s = line.strip()
        if in_tag:                      # inside a multi-line HTML tag: attributes are not prose
            in_tag = ">" not in s
            continue
        if not s:
            kind, html = "blank", False
            continue
        ex = line.expandtabs(4)
        indent = len(ex) - len(ex.lstrip())
        if (not html and indent >= (4 if list_ctx is None else list_ctx + 4)
                and (icode or kind != "prose")):    # indented code: never interrupts a paragraph
            icode, kind = True, "other"
            continue
        icode = False
        if kind == "blank" and list_ctx is not None and indent < list_ctx and not LIST_RE.match(s):
            list_ctx = None
        h = HEADING_RE.match(s)
        if h:
            level = len(h.group(1))
            if legend_level and level <= legend_level:
                legend_level = 0
            if LEGEND_RE.search(h.group(2)) and not legend_level:
                legend_level = level
            seen_h2, kind, list_ctx = seen_h2 or level == 2, "other", None
            continue
        if s.startswith("|") or LINK_DEF_RE.match(s) or HR_RE.match(s):
            kind = "other"
            continue
        html = html or bool(TAG_START_RE.match(s))
        if TAG_START_RE.match(s) and ">" not in s:
            in_tag, kind = True, "other"
            continue
        if TAG_ONLY_RE.fullmatch(s):
            kind = "other"
            continue
        quote = s.startswith(">")
        s = re.sub(r"^(?:>\s*)+", "", s)
        if quote and not s:
            kind = "blank"
            continue
        lm = LIST_RE.match(s)
        if lm and not quote:
            list_ctx = indent + lm.end()
        s = CHECKBOX_RE.sub("", LIST_RE.sub("", s))
        if ALERT_RE.match(s) or LINK_ONLY_RE.fullmatch(s):
            kind = "other"
            continue
        s = _clean(s)
        if not s:
            kind = "other"
            continue
        joins = kind == "prose" and not prev_hard and not lm and not (quote and not prev_quote)
        out.append(_Line(no, s, bool(legend_level), not seen_h2, not joins))
        kind, prev_quote, prev_hard = "prose", quote, bool(HARD_BREAK_RE.search(raw))
    return out


def prose_lines(text: str) -> list[tuple[int, str]]:
    """(1-based line number, cleaned text) for every line a reader reads as prose."""
    return [(ln.no, ln.text) for ln in _walk(text)]


def _split(block: str) -> list[tuple[int, str]]:
    """(start offset, text) of each sentence in a joined block."""
    parts, start = [], 0
    for m in SPLIT_RE.finditer(block):
        words = block[start:m.start()].split()
        if words and words[-1].lower() in ABBREVIATIONS:
            continue
        parts.append((start, block[start:m.start()]))
        start = m.end()
    parts.append((start, block[start:]))
    return parts


def _words(s: str) -> int:
    return sum(1 for t in s.split() if any(c.isalnum() for c in t))


def _blocks(lines: list[_Line]) -> list[list[_Line]]:
    blocks: list[list[_Line]] = []
    for ln in lines:
        if ln.new_block or not blocks:
            blocks.append([])
        blocks[-1].append(ln)
    return blocks


def _join(blk: list[_Line]) -> tuple[str, list[tuple[int, _Line]]]:
    """A block as one string, with the offset at which each source line starts."""
    joined, starts = "", []
    for ln in blk:
        joined += " " if joined else ""
        starts.append((len(joined), ln))
        joined += ln.text
    return joined, starts


def sentences(text: str) -> list[Sentence]:
    """Sentences of at least three words, reported at the line where each one starts.

    A paragraph or list item is joined (wrapped source lines become one line of text) before it is
    split, so two list items stay two sentences and hard-wrapping changes nothing. `passive` is a
    heuristic: a form of "to be" followed by a word that looks like a participle. It misses some
    passives and flags some adjectives ("is open"); use it as a trend, not a verdict.
    """
    out = []
    for blk in _blocks(_walk(text)):
        joined, starts = _join(blk)
        for off, part in _split(joined):
            n = _words(part)
            if n >= MIN_WORDS:
                out.append(Sentence([ln.no for o, ln in starts if o <= off][-1], part.strip(), n, bool(PASSIVE_RE.search(part))))
    return out


def _share(n: int, total: int) -> float:
    return round(100 * n / total, 1) if total else 0.0


def stats_of(sents: list[Sentence]) -> ProseStats:
    total = len(sents)
    n_long = sum(1 for s in sents if s.words > LONG_WORDS)
    n_passive = sum(1 for s in sents if s.passive)
    n_ok = sum(1 for s in sents if s.words <= LONG_WORDS and not s.passive)
    return ProseStats(total, n_long, _share(n_long, total), n_passive, _share(n_passive, total), n_ok, _share(n_ok, total))


def prose_stats(text: str) -> ProseStats:
    return stats_of(sentences(text))


def internal_codes(text: str) -> list[CodeHit]:
    """Bare internal codes in prose: not in code, tables or link targets, not in a legend or glossary
    section, not on a line that defines the code, and not an allowlisted prefix such as ISO-8601."""
    hits: list[tuple[int, CodeHit]] = []
    for blk in _blocks(_walk(text)):
        if blk[0].legend:
            continue
        joined, starts = _join(blk)          # the blocks sentences() builds: a code can wrap over a line end
        for rx in CODE_RES:
            for m in rx.finditer(joined):
                code = m.group(0)
                lead = re.match(r"[A-Z]+", code)
                if lead and lead.group(0) in CODE_ALLOWLIST:
                    continue
                off, ln = [(o, l) for o, l in starts if o <= m.start()][-1]
                if m.start() == off and re.match(re.escape(code) + r"\s*[:=—–-](?:\s|$)", ln.text):
                    continue                 # a line that defines the code: `F-222: the lean mix`
                if not any(h.line == ln.no and h.code == code for _, h in hits):
                    hits.append((m.start(), CodeHit(ln.no, code)))
    return [h for _, h in sorted(hits, key=lambda t: (t[1].line, t[0]))]


def decision_owner(text: str) -> DecisionOwner | None:
    """A role and a decision term both occur in the prose before the first H2."""
    lead = [ln for ln in _walk(text) if ln.lead]
    zone = " ".join(ln.text for ln in lead)
    role, verb = ROLE_RE.search(zone), DECISION_RE.search(zone)
    if not (role and verb):
        return None
    line = next((ln.no for ln in lead if ROLE_RE.search(ln.text)), lead[0].no)
    return DecisionOwner(role.group(0), verb.group(0), line)


def prose_report(text: str) -> dict:
    """Everything the `prose` command prints, as one dictionary."""
    owner = decision_owner(text)
    return {**asdict(prose_stats(text)), "codes": [asdict(h) for h in internal_codes(text)],
            "decision_owner": asdict(owner) if owner else None}
