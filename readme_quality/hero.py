"""Hero banner generator with layout guardrails (Braga design system v2.1, D-051).

Visual rules (braga-portfolio-v2 design-system/DECISIONS.md §3.1; values from tokens.json):
  ground `surface`; text `ink`, labels `ink-2`; one 1px `ink` rule opens the facts row
  BRAGA wordmark in BKribitz 800 at -0.07em; labels BKribitz Mono 400, uppercase, +0.08em
  title BKribitz 700 at -0.025em; descriptor BKribitz 400 at most 60 characters a line
  the project's status as its D-029 square (drawn, in ink) beside its label
  no accent (a banner has no earned figure and no action), no dots, no image, no gradient

Guardrails (all programmatic):
  - every text block wrapped to the safe width; type shrinks until it fits
  - line-length caps (title <= 3 lines / 44 chars, tagline 1 line, descriptor <= 4 lines / 60 chars)
  - no rectangle overlap between blocks; every block inside the safe area
  - glyph coverage checked per character against the font's cmap; an uncovered character
    renders in the fallback font at the same size, so nothing silently disappears
  - contrast ink/surface >= 4.5 and ink-2/surface >= 4.5 (both are text)
  - post-render pixel scan: nothing painted outside the safe area, and no pixel in the accent
On failure the layout is retried with smaller type; if it still fails, HeroLayoutError.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from . import design

try:  # glyph coverage
    from fontTools.ttLib import TTFont
except Exception:  # pragma: no cover
    TTFont = None


def palette(mode: str) -> dict:
    c = design.color(mode)
    return {"surface": c["surface"], "ink": c["ink"], "ink2": c["ink-2"], "mid": c["mid"], "rule": c["rule-c"], "accent": c["accent-01"]}


PALETTE = {m: palette(m) for m in ("light", "dark")}

W, H = 1600, 640
MARGIN = 72
GRID = 8
DOT = "\u00b7"           # the separator (D-034), a glyph of the face
LABEL_TRACKING = 0.08    # em, --tracking-label
TITLE_TRACKING = -0.025  # em, --tracking-tight
WORDMARK_TRACKING = -0.07
DESC_CHARS = 60          # --measure (D-050)

# README status vocabulary -> D-029 state (DECISIONS.md §3.1)
STATUS_STATE = {
    "complete": "complete", "maintained": "complete",
    "functional": "functional",
    "in development": "in-build", "prototype": "in-build", "foundation": "in-build",
    "archived": "archived",
    "under revision": "under-revision", "under-revision": "under-revision",
}

_MEASURE = ImageDraw.Draw(Image.new("RGB", (1, 1)))


class HeroLayoutError(RuntimeError):
    pass


@dataclass
class HeroSpec:
    title: str
    descriptor: str = ""
    tagline: str = ""         # short motto set as a label under the title (the machine layer)
    kind: str = ""            # Analytical project / Library / Framework / Application
    status: str = ""
    facts: list[tuple[str, str]] = field(default_factory=list)  # (LABEL, value) — repository facts only
    mode: str = "light"
    brand: str = "BRAGA"


@dataclass
class FontSet:
    wordmark: str
    display: str
    body: str
    mono: str
    fallback_display: str
    fallback_body: str
    fallback_mono: str
    source: str = ""


# ------------------------------------------------------------------ fonts
def _first_existing(paths) -> str | None:
    for p in paths:
        if p and Path(p).is_file():
            return str(p)
    return None


def _matplotlib_font(name: str) -> str | None:
    try:
        import matplotlib
        p = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / name
        return str(p) if p.is_file() else None
    except Exception:
        return None


def find_fonts(fonts_dir: str | Path | None = None) -> FontSet:
    win = Path("C:/Windows/Fonts")
    fb_display = _first_existing([win / "arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", _matplotlib_font("DejaVuSans-Bold.ttf")])
    fb_body = _first_existing([win / "arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", _matplotlib_font("DejaVuSans.ttf")])
    fb_mono = _first_existing([win / "consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", _matplotlib_font("DejaVuSansMono.ttf")])
    faces = {r: design.font_path(r, fonts_dir) for r in design.FACES}
    if all(faces.values()):
        fb = (fb_display or faces["display"], fb_body or faces["body"], fb_mono or faces["mono"])
        return FontSet(faces["wordmark"], faces["display"], faces["body"], faces["mono"], *fb,
                       source="BKribitz (" + ("vendored snapshot" if Path(faces["display"]).parent == design.VENDORED_FONTS else "design-system checkout") + ")")
    if not (fb_display and fb_body and fb_mono):
        raise HeroLayoutError("BKribitz not found and no fallback fonts (need a bold sans, a sans and a mono TTF)")
    return FontSet(fb_display, fb_display, fb_body, fb_mono, fb_display, fb_body, fb_mono, source="fallback fonts (BKribitz not found)")


_CMAP_CACHE: dict[str, set[int]] = {}


def glyph_coverage_ok(font_path: str, text: str) -> bool:
    if TTFont is None:
        return True
    if font_path not in _CMAP_CACHE:
        try:
            _CMAP_CACHE[font_path] = set(TTFont(font_path).getBestCmap().keys())
        except Exception:
            _CMAP_CACHE[font_path] = set()
    cmap = _CMAP_CACHE[font_path]
    if not cmap:
        return True
    return all(ord(ch) in cmap or ch in (" ", "\n") for ch in text)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------ colour
def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _lum(rgb) -> float:
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a: str, b: str) -> float:
    la, lb = _lum(_hex(a)), _lum(_hex(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ------------------------------------------------------------------ blocks
@dataclass
class Block:
    name: str
    lines: list[str]
    font: ImageFont.FreeTypeFont
    font_path: str
    x: int
    y: int
    line_height: int
    color: str
    tracking: float = 0.0
    fallback: ImageFont.FreeTypeFont | None = None   # same size; used for glyphs the primary font lacks

    def runs(self, line: str):
        """Split a line into (text, font) runs; glyphs missing from the primary font use the fallback."""
        if self.fallback is None:
            yield line, self.font
            return
        cur, cur_font = "", None
        for ch in line:
            f = self.font if glyph_coverage_ok(self.font_path, ch) else self.fallback
            if cur_font is None or f is cur_font:
                cur += ch
                cur_font = f
            else:
                yield cur, cur_font
                cur, cur_font = ch, f
        if cur:
            yield cur, cur_font

    def _w(self, line: str) -> int:
        w = 0.0
        for text, f in self.runs(line):
            if self.tracking:
                for c in text:
                    w += _MEASURE.textlength(c, font=f) + self.tracking
            else:
                w += _MEASURE.textlength(text, font=f)
        if self.tracking and line:
            w -= self.tracking          # no tracking after the last glyph
        return int(round(w))

    @property
    def bbox(self):
        return (self.x, self.y, self.x + max(self._w(l) for l in self.lines), self.y + self.line_height * len(self.lines))


def wrap(text: str, block: Block, max_width: int, max_chars: int = 0) -> list[str]:
    """Greedy wrap to a pixel width and, when given, a character measure."""
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if (block._w(trial) <= max_width and (not max_chars or len(trial) <= max_chars)) or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def _overlaps(a, b) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 <= bx0 or bx1 <= ax0 or ay1 <= by0 or by1 <= ay0)


def status_state(status: str) -> str:
    return STATUS_STATE.get(status.strip().lower(), "in-build")


# ------------------------------------------------------------------ layout
LABEL = 22          # label size in the banner (12px on the site, scaled with the banner)
SQUARE = 14         # the 7px status square at the same scale
SQUARE_GAP = 16


def _label(name, text, fonts, x, y, color, size=LABEL):
    return Block(name, [text], load_font(fonts.mono, size), fonts.mono, x, y, int(size * 1.4), color,
                 tracking=size * LABEL_TRACKING, fallback=load_font(fonts.fallback_mono, size))


def layout(spec: HeroSpec, fonts: FontSet, title_size: int, desc_size: int) -> list[Block]:
    pal = PALETTE[spec.mode]
    safe_w = W - 2 * MARGIN
    blocks: list[Block] = []

    # top row: BRAGA, then the kind as a label (left); the status square and label (right)
    wm_size = 32
    wb = Block("wordmark", [spec.brand.upper()], load_font(fonts.wordmark, wm_size), fonts.wordmark, MARGIN, MARGIN,
               int(wm_size * 1.1), pal["ink"], tracking=wm_size * WORDMARK_TRACKING, fallback=load_font(fonts.fallback_display, wm_size))
    blocks.append(wb)
    if spec.kind:
        kb = _label("kind", f"{DOT}  {spec.kind.upper()}", fonts, 0, 0, pal["ink2"])
        kb.x = MARGIN + wb._w(wb.lines[0]) + 14
        kb.y = MARGIN + (wb.line_height - kb.line_height) // 2 + 2
        blocks.append(kb)
    if spec.status:
        st = spec.status.upper()
        sb = _label("status", st, fonts, 0, 0, pal["ink2"])
        sb.x = W - MARGIN - sb._w(st)
        sb.y = MARGIN + (wb.line_height - sb.line_height) // 2 + 2
        blocks.append(sb)

    # facts row (bottom), opened by an ink rule; trailing facts are dropped until the row fits
    facts = [f"{k.upper()}  {v}" for k, v in spec.facts if v]
    fb = _label("facts", "", fonts, MARGIN, 0, pal["ink2"])
    fb.y = H - MARGIN - fb.line_height
    while facts:
        if fb._w(f"  {DOT}  ".join(facts)) <= safe_w:
            break
        facts = facts[:-1]
    if facts:
        fb.lines = [f"  {DOT}  ".join(facts)]
        blocks.append(fb)
    body_top = MARGIN + wb.line_height + 32
    body_bottom = (fb.y - 16 - 48) if facts else (H - MARGIN)

    # title, optional tagline, descriptor — vertically centred in the body band.
    tb = Block("title", [], load_font(fonts.display, title_size), fonts.display, MARGIN, 0, int(title_size * 1.05), pal["ink"],
               tracking=title_size * TITLE_TRACKING, fallback=load_font(fonts.fallback_display, title_size))
    tb.lines = wrap(spec.title, tb, safe_w, 44)
    stack = [tb]
    gaps: list[int] = []
    if spec.tagline:
        tag_size = max(LABEL, min(26, int(desc_size * 0.72)))
        gb = _label("tagline", "", fonts, MARGIN, 0, pal["ink2"], size=tag_size)
        gb.lines = wrap(spec.tagline.upper(), gb, safe_w)
        gaps.append(24)
        stack.append(gb)
    if spec.descriptor:
        db = Block("descriptor", [], load_font(fonts.body, desc_size), fonts.body, MARGIN, 0, int(desc_size * 1.4), pal["ink"],
                   fallback=load_font(fonts.fallback_body, desc_size))
        measure = min(int(safe_w * 0.8), int(_MEASURE.textlength("0" * DESC_CHARS, font=db.font)))
        db.lines = wrap(spec.descriptor, db, measure, DESC_CHARS)
        gaps.append(32)
        stack.append(db)
    body_h = sum(b.line_height * len(b.lines) for b in stack) + sum(gaps)
    y = body_top + max(0, (body_bottom - body_top - body_h) // 2)
    y = (y // GRID) * GRID
    for i, b in enumerate(stack):
        b.y = y
        y += b.line_height * len(b.lines) + (gaps[i] if i < len(gaps) else 0)
        blocks.append(b)
    return blocks


def _box(b: Block):
    x0, y0, x1, y1 = b.bbox
    if b.name == "status":          # the square stands left of the label
        x0 -= SQUARE + SQUARE_GAP
    return (x0, y0, x1, y1)


def validate_blocks(blocks: list[Block], spec: HeroSpec) -> list[str]:
    problems: list[str] = []
    safe = (MARGIN - 2, MARGIN - 2, W - MARGIN + 2, H - MARGIN + 2)
    for b in blocks:
        x0, y0, x1, y1 = _box(b)
        if x0 < safe[0] or y0 < safe[1] or x1 > safe[2] or y1 > safe[3]:
            problems.append(f"{b.name} outside safe area: {b.bbox}")
        for line in b.lines:
            if b.name == "title" and len(line) > 44:
                problems.append(f"title line too long ({len(line)} chars): {line[:40]}")
            if b.name == "descriptor" and len(line) > DESC_CHARS:
                problems.append(f"descriptor line too long ({len(line)} chars)")
        if b.name == "title" and len(b.lines) > 3:
            problems.append(f"title wraps to {len(b.lines)} lines (max 3)")
        if b.name == "descriptor" and len(b.lines) > 4:
            problems.append(f"descriptor wraps to {len(b.lines)} lines (max 4)")
        if b.name == "tagline" and len(b.lines) > 1:
            problems.append(f"tagline wraps to {len(b.lines)} lines (max 1) — shorten it")
    named = {b.name: b for b in blocks}
    body_bottom = max(named[n].bbox[3] for n in ("title", "tagline", "descriptor") if n in named)
    if "facts" in named and named["facts"].bbox[1] - body_bottom < 48:
        problems.append("facts row collides with the body text")
    if "title" in named and named["title"].bbox[1] - named["wordmark"].bbox[3] < 24:
        problems.append("title collides with the label row")
    for i, a in enumerate(blocks):
        for b in blocks[i + 1:]:
            if _overlaps(_box(a), _box(b)):
                problems.append(f"{a.name} overlaps {b.name}")
    pal = PALETTE[spec.mode]
    if contrast(pal["ink"], pal["surface"]) < 4.5:
        problems.append("ink/surface contrast below 4.5")
    if contrast(pal["ink2"], pal["surface"]) < 4.5:
        problems.append("ink-2/surface contrast below 4.5")
    return problems


def draw_status_square(draw: ImageDraw.ImageDraw, x: int, y: int, state: str, color: str, size: int = SQUARE) -> None:
    """The D-029 square at banner scale: the site's 1px border of 7 becomes 2px of 14."""
    b = max(1, round(size / 7))
    x1, y1 = x + size - 1, y + size - 1
    if state == "complete":
        draw.rectangle([(x, y), (x1, y1)], fill=color)
        return
    if state == "archived":                      # dotted outline
        for i in range(0, size, 2 * b):
            for (px, py) in ((x + i, y), (x + i, y1 - b + 1), (x, y + i), (x1 - b + 1, y + i)):
                draw.rectangle([(px, py), (px + b - 1, py + b - 1)], fill=color)
        return
    draw.rectangle([(x, y), (x1, y1)], outline=color, width=b)
    if state == "functional":                    # filled centre, one border's gap
        draw.rectangle([(x + 2 * b, y + 2 * b), (x1 - 2 * b, y1 - 2 * b)], fill=color)
    elif state == "under-revision":              # half filled, bottom
        draw.rectangle([(x, y + size - round(size * 4 / 7)), (x1, y1)], fill=color)


def render(blocks: list[Block], spec: HeroSpec) -> Image.Image:
    pal = PALETTE[spec.mode]
    img = Image.new("RGB", (W, H), pal["surface"])
    draw = ImageDraw.Draw(img)
    named = {b.name: b for b in blocks}
    if "facts" in named:  # the rule opens the facts row (D-044): 1px ink
        y = named["facts"].y - 16
        draw.line([(MARGIN, y), (W - MARGIN - 1, y)], fill=pal["ink"], width=1)
    for b in blocks:
        for i, line in enumerate(b.lines):
            y = b.y + i * b.line_height
            x = float(b.x)
            for text, f in b.runs(line):
                if b.tracking:
                    for ch in text:
                        draw.text((x, y), ch, font=f, fill=b.color)
                        x += draw.textlength(ch, font=f) + b.tracking
                else:
                    draw.text((x, y), text, font=f, fill=b.color)
                    x += draw.textlength(text, font=f)
    if "status" in named:
        s = named["status"]
        cap = s.font.getbbox("H")
        cy = s.y + (cap[1] + cap[3]) // 2      # centred on the label's capitals
        draw_status_square(draw, s.x - SQUARE_GAP - SQUARE, cy - SQUARE // 2, status_state(spec.status), pal["ink"])
    return img


def pixel_validate(img: Image.Image, spec: HeroSpec) -> list[str]:
    """Nothing painted outside the safe area; text visible inside it; no accent anywhere."""
    pal = PALETTE[spec.mode]
    surface = _hex(pal["surface"])
    accent = _hex(pal["accent"])
    px = img.load()
    tol = 8
    inside = 0
    band = MARGIN - 12  # letter tracking gets a few pixels of slack
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            r, g, b = px[x, y][:3]
            if abs(r - surface[0]) > tol or abs(g - surface[1]) > tol or abs(b - surface[2]) > tol:
                if x < band or x > W - band or y < band or y > H - band:
                    return [f"paint outside safe area at ({x},{y})"]
                if abs(r - accent[0]) <= 4 and abs(g - accent[1]) <= 4 and abs(b - accent[2]) <= 4:
                    return [f"accent colour painted at ({x},{y}): a banner carries no accent (D-051)"]
                inside += 1
    return [] if inside >= 200 else ["almost nothing rendered inside the safe area"]


def generate(spec: HeroSpec, out_path: Path | str, fonts_dir: str | Path | None = None, report_path: Path | str | None = None) -> dict:
    fonts = find_fonts(fonts_dir)
    attempts = []
    chosen = None
    for ts in (112, 104, 96, 88, 80, 72, 64, 56, 48):
        for ds in (34, 32, 30, 28, 26):
            blocks = layout(spec, fonts, ts, ds)
            problems = validate_blocks(blocks, spec)
            attempts.append({"title_size": ts, "desc_size": ds, "problems": problems})
            if not problems:
                img = render(blocks, spec)
                pp = pixel_validate(img, spec)
                if pp:
                    attempts[-1]["problems"] = pp
                    continue
                chosen = (ts, ds, blocks, img)
                break
        if chosen:
            break
    if not chosen:
        raise HeroLayoutError("no layout satisfied the guardrails; last problems: " + "; ".join(attempts[-1]["problems"][:3]))
    ts, ds, blocks, img = chosen
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    report = {
        "output": out_path.name, "width": W, "height": H, "mode": spec.mode, "fonts": fonts.source,
        "design_system": f"braga {design.tokens().get('version', '?')} (D-051)",
        "status_state": status_state(spec.status) if spec.status else None,
        "title_size": ts, "descriptor_size": ds, "attempts": len(attempts),
        "blocks": {b.name: {"bbox": b.bbox, "lines": b.lines, "font": Path(b.font_path).name} for b in blocks},
        "guardrails": ["safe-area", "wrap-and-shrink", "line-length", "no-overlap", "glyph-coverage-per-char", "contrast>=4.5", "pixel-scan", "no-accent"],
        "validated": True,
    }
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def spec_from_project(project, facts) -> HeroSpec:
    """Build a HeroSpec from registry + repository facts only (no invented values)."""
    kind = {"analytical": "Analytical project", "application": "Application", "library": "Library",
            "framework": "Framework", "docs": "Documentation"}.get(project.type, project.type)
    facts_row: list[tuple[str, str]] = []
    if facts.license_id and facts.license_id != "UNKNOWN":
        facts_row.append(("License", facts.license_id))
    runtime = getattr(project, "runtime", "") or (f"Python {facts.python_requires}" if facts.python_requires else "") \
        or (f"Python {facts.python_version_file}" if facts.python_version_file else "") or (f"Node {facts.node_engine}" if facts.node_engine else "")
    if runtime:
        facts_row.append(("Runtime", runtime))
    if facts.ci_workflow:
        facts_row.append(("CI", "GitHub Actions"))
    gh = getattr(project, "github", "")
    if gh:
        facts_row.append(("Repo", f"github.com/{gh}"))
    title = project.title or re.sub(r"[-_]+", " ", project.name).title()
    return HeroSpec(title=title, descriptor=project.descriptor or "", tagline=getattr(project, "tagline", "") or "",
                    kind=kind, status=project.status or "", facts=facts_row)
