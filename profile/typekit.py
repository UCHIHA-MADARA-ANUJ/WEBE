#!/usr/bin/env python3
"""Type as geometry.

A profile SVG that says <text font-family="Inter"> is a request, not a
decision. whomever opens the image decides what it looks like: SF Pro on a
Mac, Segoe on Windows, Roboto on Android, a fallback with the wrong weights
and the wrong tracking on a Linux box. That is why most SVG profiles look
slightly wrong in someone else's browser.

So this module converts every string to outlines at build time. What ships
is geometry, and geometry renders identically everywhere, at every zoom,
with no fonts installed.

    from typekit import text_path, text_width, image_tag
"""
import base64
import pathlib
from functools import lru_cache

from fontTools.misc.transform import Transform
from fontTools.pens.basePen import BasePen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"


def _nearest(family, weight):
    """Snap to the closest cut that exists. Asking for 550 should not crash."""
    want = int(round(float(weight) / 100.0)) * 100
    want = max(100, min(900, want))
    cuts = sorted(int(f.stem.split("-")[1]) for f in FONTS.glob(f"{family}-*.ttf"))
    if not cuts:
        raise FileNotFoundError(f"no cuts installed for {family}")
    return min(cuts, key=lambda c: (abs(c - want), c))


@lru_cache(maxsize=None)
def _load(family, weight):
    weight = _nearest(family, weight)
    path = FONTS / f"{family}-{weight}.ttf"
    if not path.exists():
        raise FileNotFoundError(
            f"missing {path.name} — run the font build in SETUP.md")
    font = TTFont(str(path))
    return font, font.getGlyphSet(), font["head"].unitsPerEm, \
        font["cmap"].getBestCmap()


def _num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


class AbsPen(BasePen):
    """Absolute M/L/Q/C/Z only.

    fontTools' SVGPathPen is clever and emits H and V for straight runs, plus
    a few other shorthands. Clever output is output two renderers can disagree
    about. This pen writes the dumbest possible thing, which is the point.
    """

    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.parts = []

    def _pt(self, p):
        return f"{_num(p[0])} {_num(p[1])}"

    def _moveTo(self, p):
        self.parts.append("M" + self._pt(p))

    def _lineTo(self, p):
        self.parts.append("L" + self._pt(p))

    def _curveToOne(self, p1, p2, p3):
        self.parts.append("C" + self._pt(p1) + " " + self._pt(p2)
                          + " " + self._pt(p3))

    def _qCurveToOne(self, p1, p2):
        self.parts.append("Q" + self._pt(p1) + " " + self._pt(p2))

    def _closePath(self):
        self.parts.append("Z")

    def commands(self):
        return "".join(self.parts)


def runs(s, family, weight):
    """Split a string into (glyph_name, advance_in_font_units) pairs."""
    _font, gs, _upm, cmap = _load(family, weight)
    out = []
    for ch in s:
        name = cmap.get(ord(ch))
        if name is None:
            name = cmap.get(ord("?"))
        out.append((name, gs[name].width if name else 0))
    return out


def text_width(s, size, family="Inter", weight=400, tracking=0.0):
    """Width of the drawn run, in user units."""
    _font, _gs, upm, _cmap = _load(family, weight)
    pairs = runs(s, family, weight)
    scl = size / upm
    return sum(a * scl for _n, a in pairs) + tracking * max(0, len(s) - 1)


def text_path(s, x, y, size, family="Inter", weight=400, tracking=0.0,
              anchor="start", fill="#000000", opacity=None, cls=None):
    """Return a single <path> holding the whole string as outlines.

    x/y is the baseline origin, exactly like <text>. anchor is start, middle
    or end, exactly like <text>. tracking is letter-spacing in user units.
    """
    if not s:
        return ""
    _font, gs, upm, _cmap = _load(family, weight)
    scl = size / upm
    pairs = runs(s, family, weight)

    total = sum(a * scl for _n, a in pairs) + tracking * max(0, len(pairs) - 1)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total

    parts, cursor = [], x
    for name, adv in pairs:
        pen = AbsPen(gs)
        gs[name].draw(TransformPen(pen, Transform(scl, 0, 0, -scl, cursor, y)))
        cmds = pen.commands()
        if cmds:
            parts.append(cmds)
        cursor += adv * scl + tracking

    if not parts:
        return ""
    attrs = [f'd="{"".join(parts)}"', f'fill="{fill}"']
    if opacity is not None and opacity != 1:
        attrs.append(f'opacity="{_num(opacity)}"')
    if cls:
        attrs.append(f'class="{cls}"')
    return f'<path {" ".join(attrs)}/>'


def image_tag(path, x, y, w, h, mime="image/png"):
    """Inline a raster as a data URI. GitHub's image proxy will not fetch a
    second file from inside an SVG, so anything raster must travel with it."""
    data = base64.b64encode(pathlib.Path(path).read_bytes()).decode("ascii")
    return (f'<image x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" '
            f'height="{_num(h)}" href="data:{mime};base64,{data}"/>')


def data_uri(path, mime="image/png"):
    return "data:%s;base64,%s" % (
        mime, base64.b64encode(pathlib.Path(path).read_bytes()).decode("ascii"))
