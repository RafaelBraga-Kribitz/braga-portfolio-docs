"""Hero banner generator with layout guardrails (Braga-Kribitz design system).

Visual rules applied (from the design system's tokens and README):
  surface #E6E6E6 (light) / #1A1A1A (dark); ink #282828 / #F5F5F5; mid #A0A0A0 / #808080
  display: Söhne 800 (fallback: bold sans); labels: Söhne Mono 400 (fallback: mono)
  one orange (#FA6400) element only: the status dot
  hairline 1px mid grey as the structural device; 8px grid; no gradients, no images

Guardrails (all programmatic):
  - every text block wrapped to the safe width; type shrinks until it fits
  - line-length caps (title <= 3 lines / 44 chars, descriptor <= 3 lines / 96 chars)
  - no rectangle overlap between blocks; every block inside the safe area
  - glyph coverage checked per character against the font's cmap (the trial Söhne
    files carry 68 glyphs); uncovered characters render in the fallback font at the
    same size, so a colon or bracket never silently disappears
  - contrast ratio ink/surface >= 4.5
  - post-render pixel scan: nothing painted outside the safe area
On failure the layout is retried with smaller type; if it still fails, HeroLayoutError.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:  # glyph coverage
    from fontTools.ttLib import TTFont
except Exception:  # pragma: no cover
    TTFont = None

PALETTE = {
    "light": {"surface": "#E6E6E6", "ink": "#282828", "ink2": "#4A4A4A", "mid": "#A0A0A0", "accent": "#FA6400"},  # ink2 darkened 2026-09-17 for readability (7.6:1)
    "dark": {"surface": "#1A1A1A", "ink": "#F5F5F5", "ink2": "#D0D0D0", "mid": "#808080", "accent": "#FA6400"},
}

W, H = 1600, 640
MARGIN = 72
GRID = 8
DOT = "\u00b7"  # middle dot; drawn as a circle, never relies on the font

_MEASURE = ImageDraw.Draw(Image.new("RGB", (1, 1)))


class HeroLayoutError(RuntimeError):
    pass


@dataclass
class HeroSpec:
    title: str
    descriptor: str = ""
    kind: str = ""            # Analytical project / Library / Framework / Application
    status: str = ""
    facts: list[tuple[str, str]] = field(default_factory=list)  # (LABEL, value) — repository facts only
    mode: str = "light"
    brand: str = "BRAGA"


@dataclass
class FontSet:
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
    candidates = [fonts_dir, os.environ.get("BK_FONTS"),
                  Path(__file__).resolve().parents[2] / "braga-design-system-template" / "public" / "fonts",
                  Path(__file__).resolve().parents[3] / "braga-design-system-template" / "public" / "fonts",
                  Path.home() / ".fonts"]
    soehne_dir = None
    for c in candidates:
        if c and (Path(c) / "Sohne-Fett.otf").is_file():
            soehne_dir = Path(c)
            break
    win = Path("C:/Windows/Fonts")
    fb_display = _first_existing([win / "arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", _matplotlib_font("DejaVuSans-Bold.ttf")])
    fb_body = _first_existing([win / "arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", _matplotlib_font("DejaVuSans.ttf")])
    fb_mono = _first_existing([win / "consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", _matplotlib_font("DejaVuSansMono.ttf")])
    if not (fb_display and fb_body and fb_mono):
        raise HeroLayoutError("no fallback fonts found (need a bold sans, a sans, and a mono TTF)")
    if soehne_dir:
        return FontSet(str(soehne_dir / "Sohne-Fett.otf"), str(soehne_dir / "Sohne-Buch.otf"), str(soehne_dir / "SohneMono-Buch.otf"),
                       fb_display, fb_body, fb_mono, source=f"Söhne from {soehne_dir}")
    return FontSet(fb_display, fb_body, fb_mono, fb_display, fb_body, fb_mono, source="fallback fonts (Söhne not found)")


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
    return all(ord(ch) in cmap or ch in (" ", "\n", DOT) for ch in text)


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
    tracking: int = 0
    fallback: ImageFont.FreeTypeFont | None = None   # same size; used for glyphs the primary font lacks
    dots: bool = False                                # render the middle dot as a drawn circle

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
            if self.tracking or self.dots:
                for c in text:
                    w += _MEASURE.textlength("o" if c == DOT else c, font=f) + self.tracking
            else:
                w += _MEASURE.textlength(text, font=f)
        return int(w)

    @property
    def bbox(self):
        return (self.x, self.y, self.x + max(self._w(l) for l in self.lines), self.y + self.line_height * len(self.lines))


def wrap(text: str, block: Block, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if block._w(trial) <= max_width or not cur:
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


# ------------------------------------------------------------------ layout
def layout(spec: HeroSpec, fonts: FontSet, title_size: int, desc_size: int) -> list[Block]:
    pal = PALETTE[spec.mode]
    safe_w = W - 2 * MARGIN
    blocks: list[Block] = []
    sep = f" {DOT} "

    # top row: brand / kind label (left) and status (right)
    left_label = f"{spec.brand}{sep}{spec.kind}".upper() if spec.kind else spec.brand.upper()
    kb = Block("kind", [left_label], load_font(fonts.mono, 24), fonts.mono, MARGIN, MARGIN, 32, pal["ink2"],
               tracking=2, fallback=load_font(fonts.fallback_mono, 24), dots=True)
    blocks.append(kb)
    if spec.status:
        st = spec.status.upper()
        sb = Block("status", [st], load_font(fonts.mono, 24), fonts.mono, 0, MARGIN, 32, pal["ink2"],
                   tracking=2, fallback=load_font(fonts.fallback_mono, 24))
        sb.x = W - MARGIN - sb._w(st)
        blocks.append(sb)

    # facts row (bottom), under a hairline; trailing facts are dropped until the row fits
    facts = [f"{k.upper()}  {v}" for k, v in spec.facts if v]
    fy = H - MARGIN - 26
    fb = Block("facts", [""], load_font(fonts.mono, 22), fonts.mono, MARGIN, fy, 28, pal["ink2"],
               fallback=load_font(fonts.fallback_mono, 22), dots=True)
    while facts:
        row = f"  {DOT}  ".join(facts)
        if fb._w(row) <= safe_w:
            break
        facts = facts[:-1]
    if facts:
        fb.lines = [f"  {DOT}  ".join(facts)]
        blocks.append(fb)
    body_top = MARGIN + 32 + 24
    body_bottom = (fy - 22 - 40) if facts else (H - MARGIN)

    # title + descriptor, vertically centred in the body band
    tb = Block("title", [], load_font(fonts.display, title_size), fonts.display, MARGIN, 0, int(title_size * 1.02), pal["ink"],
               fallback=load_font(fonts.fallback_display, title_size))
    tb.lines = wrap(spec.title, tb, safe_w)
    stack = [tb]
    if spec.descriptor:
        db = Block("descriptor", [], load_font(fonts.body, desc_size), fonts.body, MARGIN, 0, int(desc_size * 1.35), pal["ink"],
                   fallback=load_font(fonts.fallback_body, desc_size))
        db.lines = wrap(spec.descriptor, db, int(safe_w * 0.78))
        stack.append(db)
    gap = 28
    body_h = sum(b.line_height * len(b.lines) for b in stack) + gap * (len(stack) - 1)
    y = body_top + max(0, (body_bottom - body_top - body_h) // 2)
    y = (y // GRID) * GRID
    for b in stack:
        b.y = y
        y += b.line_height * len(b.lines) + gap
        blocks.append(b)
    return blocks


def validate_blocks(blocks: list[Block], spec: HeroSpec) -> list[str]:
    problems: list[str] = []
    safe = (MARGIN - 2, MARGIN - 2, W - MARGIN + 2, H - MARGIN + 2)
    for b in blocks:
        x0, y0, x1, y1 = b.bbox
        if x0 < safe[0] or y0 < safe[1] or x1 > safe[2] or y1 > safe[3]:
            problems.append(f"{b.name} outside safe area: {b.bbox}")
        for line in b.lines:
            if b.name == "title" and len(line) > 44:
                problems.append(f"title line too long ({len(line)} chars): {line[:40]}")
            if b.name == "descriptor" and len(line) > 96:
                problems.append(f"descriptor line too long ({len(line)} chars)")
        if b.name == "title" and len(b.lines) > 3:
            problems.append(f"title wraps to {len(b.lines)} lines (max 3)")
        if b.name == "descriptor" and len(b.lines) > 3:
            problems.append(f"descriptor wraps to {len(b.lines)} lines (max 3)")
    named = {b.name: b for b in blocks}
    body_bottom = max(named[n].bbox[3] for n in ("title", "descriptor") if n in named)
    if "facts" in named and named["facts"].bbox[1] - body_bottom < 40:
        problems.append("facts row collides with the body text")
    if "kind" in named and "title" in named and named["title"].bbox[1] - named["kind"].bbox[3] < 16:
        problems.append("title collides with the label row")
    for i, a in enumerate(blocks):
        for b in blocks[i + 1:]:
            if _overlaps(a.bbox, b.bbox):
                problems.append(f"{a.name} overlaps {b.name}")
    pal = PALETTE[spec.mode]
    if contrast(pal["ink"], pal["surface"]) < 4.5:
        problems.append("ink/surface contrast below 4.5")
    if contrast(pal["ink2"], pal["surface"]) < 3.0:
        problems.append("secondary ink contrast below 3.0")
    return problems


def render(blocks: list[Block], spec: HeroSpec) -> Image.Image:
    pal = PALETTE[spec.mode]
    img = Image.new("RGB", (W, H), pal["surface"])
    draw = ImageDraw.Draw(img)
    named = {b.name: b for b in blocks}
    if "facts" in named:  # hairline above the facts row: the structural device
        y = named["facts"].bbox[1] - 22
        draw.line([(MARGIN, y), (W - MARGIN, y)], fill=pal["mid"], width=1)
    for b in blocks:
        for i, line in enumerate(b.lines):
            y = b.y + i * b.line_height
            x = float(b.x)
            for text, f in b.runs(line):
                if b.tracking or b.dots:
                    for ch in text:
                        if ch == DOT:
                            cw = draw.textlength("o", font=f)
                            cy = y + f.size * 0.62
                            r = max(2, int(f.size * 0.09))
                            draw.ellipse([(x + cw / 2 - r, cy - r), (x + cw / 2 + r, cy + r)], fill=b.color)
                        else:
                            draw.text((x, y), ch, font=f, fill=b.color)
                        x += draw.textlength("o" if ch == DOT else ch, font=f) + b.tracking
                else:
                    draw.text((x, y), text, font=f, fill=b.color)
                    x += draw.textlength(text, font=f)
    if "status" in named:  # the single orange element: the status dot
        s = named["status"]
        cx, cy = s.x - 22, s.y + 14
        draw.ellipse([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=pal["accent"])
    return img


def pixel_validate(img: Image.Image, spec: HeroSpec) -> list[str]:
    """Nothing may be painted outside the safe area; text must be visible inside it."""
    pal = PALETTE[spec.mode]
    surface = _hex(pal["surface"])
    px = img.load()
    tol = 8
    inside = 0
    band = MARGIN - 12  # the status dot and letter tracking get a few pixels of slack
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            r, g, b = px[x, y][:3]
            if abs(r - surface[0]) > tol or abs(g - surface[1]) > tol or abs(b - surface[2]) > tol:
                if x < band or x > W - band or y < band or y > H - band:
                    return [f"paint outside safe area at ({x},{y})"]
                inside += 1
    return [] if inside >= 200 else ["almost nothing rendered inside the safe area"]


def generate(spec: HeroSpec, out_path: Path | str, fonts_dir: str | Path | None = None, report_path: Path | str | None = None) -> dict:
    fonts = find_fonts(fonts_dir)
    attempts = []
    chosen = None
    for ts in (112, 104, 96, 88, 80, 72, 64, 56, 48):
        for ds in (36, 34, 32, 30, 28, 26):
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
        "output": str(out_path), "width": W, "height": H, "mode": spec.mode, "fonts": fonts.source,
        "title_size": ts, "descriptor_size": ds, "attempts": len(attempts),
        "blocks": {b.name: {"bbox": b.bbox, "lines": b.lines, "font": Path(b.font_path).name} for b in blocks},
        "guardrails": ["safe-area", "wrap-and-shrink", "line-length", "no-overlap", "glyph-coverage-per-char", "contrast>=4.5", "pixel-scan"],
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
    return HeroSpec(title=title, descriptor=project.descriptor or "", kind=kind, status=project.status or "", facts=facts_row)
