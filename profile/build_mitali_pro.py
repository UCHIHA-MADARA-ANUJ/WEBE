#!/usr/bin/env python3
"""Mitali Chincholikar — profile kit, built on outlines.

The previous version asked the browser for a font and hoped. This one bakes
every string to geometry with typekit.py, so the panels are identical on a
Mac, a Windows box, an Android phone and a print shop's Linux RIP. Nothing
here depends on a font, a network, or a theme someone forgot to test.

Rules the design follows:
  · nothing moves
  · no chapters, timecodes, stamps, or title-sequence framing
  · light and dark are built as a pair and switched with <picture>
  · one neutral ramp, one accent lifted from her own artwork
  · a single optical margin, left aligned, nothing centred
  · eight languages stated plainly — no bars, no percentages, no ranking

    python3 build_mitali_pro.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

import typekit as tk  # noqa: E402

OUT = HERE / "mitali"
PORTRAIT = OUT / "portrait.jpg"

W = 1200
PAD = 80              # outer margin
COL = 420             # portrait column
GUT = 56              # gutter between portrait and text
TEXT_X = PAD + COL + GUT
RIGHT = W - PAD


# ── palettes ────────────────────────────────────────────────────────────────
LIGHT = dict(
    ink="#141419",
    mid="#4E4E5A",
    soft="#82828F",
    faint="#A8A8B4",
    rule="#E4E4EA",
    wash="#F6F6F8",
    accent="#A80F2B",
    accent_wash="#FBEDEF",
)
DARK = dict(
    ink="#F4F4F6",
    mid="#B4B4C0",
    soft="#82828F",
    faint="#5E5E6A",
    rule="#2A2A33",
    wash="#16161C",
    accent="#F0637A",
    accent_wash="#2A1119",
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(s, x, y, size, fill, weight=400, tracking=0.0, anchor="start",
      family="Inter", opacity=None):
    return "  " + tk.text_path(s, x, y, size, family=family, weight=weight,
                               tracking=tracking, anchor=anchor, fill=fill,
                               opacity=opacity)


def M(s, x, y, size, fill, weight=400, tracking=0.0, anchor="start",
      opacity=None):
    """Monospace eyebrow / label."""
    return T(s, x, y, size, fill, weight=weight, tracking=tracking,
             anchor=anchor, family="JBMono", opacity=opacity)


def hr(x1, y, x2, color, opacity=1.0, width=1.0):
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
            f'stroke-width="{width}" opacity="{opacity}"/>')


def doc(h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{esc(title)}">\n'
            f'{body}\n</svg>\n')


def portrait(h, radius_px=None):
    """Her artwork, embedded as a data URI.

    GitHub serves an SVG through its image proxy, and that proxy does not
    fetch a second file referenced from inside it. Anything raster has to
    travel inside the SVG or it simply does not render.
    """
    return "  " + tk.image_tag(PORTRAIT, PAD, (h - COL) / 2, COL, COL, mime="image/jpeg")


# ── the hero: portrait beside the identity ─────────────────────────────────
def hero(c):
    H = COL + PAD * 2
    b = [f'  <rect width="{W}" height="{H}" fill="none"/>']

    # portrait, square, no rounded corners — corners are a trend that dates
    b.append(portrait(H))
    b.append(f'  <rect x="{PAD}" y="{PAD}" width="{COL}" height="{COL}" '
             f'fill="none" stroke="{c["rule"]}" stroke-width="1"/>')

    y = PAD + 26
    b.append(M("PROFILE", TEXT_X, y, 11, c["accent"], weight=600, tracking=3.4))
    b.append(hr(TEXT_X, y + 20, TEXT_X + 40, c["accent"], 1, 2))

    y += 96
    b.append(T("Mitali", TEXT_X, y, 74, c["ink"], weight=600, tracking=-2.2))
    y += 78
    b.append(T("Chincholikar", TEXT_X, y, 74, c["ink"], weight=600, tracking=-2.2))

    y += 56
    b.append(T("Computer Science \u00b7 First Year", TEXT_X, y, 23, c["mid"],
               weight=400, tracking=-0.2))

    y += 40
    b.append(M("PUNE \u00b7 MAHARASHTRA \u00b7 INDIA", TEXT_X, y, 12,
               c["soft"], weight=500, tracking=2.8))

    y += 46
    b.append(hr(TEXT_X, y, RIGHT, c["rule"]))

    # three facts on one line, the way a masthead does it
    y += 44
    facts = [("STUDYING", "Computer Science"),
             ("FROM YEAR TWO", "AI \u00b7 ML"),
             ("ALSO", "Cybersecurity")]
    span = (RIGHT - TEXT_X) / len(facts)
    for i, (k, v) in enumerate(facts):
        x = TEXT_X + i * span
        b.append(M(k, x, y, 9.5, c["faint"], weight=500, tracking=2.4))
        b.append(T(v, x, y + 30, 19, c["ink"], weight=500, tracking=-0.2))

    return doc(H, "\n".join(b),
               "Mitali Chincholikar, Computer Science, first year, Pune, India")


# ── currently ──────────────────────────────────────────────────────────────
def currently(c):
    H = 300
    b = []
    b.append(M("CURRENTLY", PAD, 58, 11, c["accent"], weight=600, tracking=3.4))
    b.append(hr(PAD, 78, RIGHT, c["rule"]))

    rows = [
        ("Computer Science, first year", "Dnyan Prasad Global University",
         "enrolled"),
        ("Artificial intelligence and machine learning", "begins year two",
         "upcoming"),
        ("Cybersecurity", "course in progress", "now"),
    ]
    y = 122
    for i, (main, sub, tag) in enumerate(rows):
        b.append(T(f"{i + 1:02d}", PAD, y, 13, c["faint"], weight=500))
        b.append(T(main, PAD + 56, y, 21, c["ink"], weight=500, tracking=-0.3))
        b.append(M(tag.upper(), RIGHT, y, 10, c["soft"], weight=500,
                   tracking=2.2, anchor="end"))
        b.append(T(sub, PAD + 56, y + 26, 14, c["soft"], weight=400))
        if i < len(rows) - 1:
            b.append(hr(PAD, y + 48, RIGHT, c["rule"], 0.65))
        y += 74
    return doc(H, "\n".join(b), "Currently")


# ── working with ───────────────────────────────────────────────────────────
def stack(c):
    H = 286
    b = []
    b.append(M("WORKING WITH", PAD, 58, 11, c["accent"], weight=600, tracking=3.4))
    b.append(hr(PAD, 78, RIGHT, c["rule"]))

    langs = ["Python", "C", "C++", "Java", "SQL", "HTML / CSS",
             "JavaScript", "Node.js"]
    # 4 x 2 grid, generous
    col_w = (RIGHT - PAD) / 4
    y = 130
    for i, lang in enumerate(langs):
        x = PAD + (i % 4) * col_w
        row = i // 4
        b.append(T(lang, x, y + row * 54, 22, c["ink"], weight=500,
                   tracking=-0.4))
    b.append(hr(PAD, 218, RIGHT, c["rule"], 0.65))

    b.append(M("DAY TO DAY", PAD, 250, 9.5, c["faint"], weight=500, tracking=2.4))
    b.append(T("VS Code", PAD + 108, 250, 15, c["mid"], weight=400))
    b.append(T("Windows", PAD + 210, 250, 15, c["mid"], weight=400))
    b.append(T("Git", PAD + 320, 250, 15, c["mid"], weight=400))

    return doc(H, "\n".join(b), "Working with")


# ── reach ──────────────────────────────────────────────────────────────────
def contact(c):
    H = 248
    b = []
    b.append(M("REACH", PAD, 58, 11, c["accent"], weight=600, tracking=3.4))
    b.append(hr(PAD, 78, RIGHT, c["rule"]))

    b.append(T("chincholikarmitali@gmail.com", PAD, 148, 32, c["ink"],
               weight=500, tracking=-0.7))
    b.append(hr(PAD, 166, PAD + 430, c["accent"], 1, 2))
    b.append(M("EMAIL \u00b7 CLICK TO WRITE", PAD, 192, 9.5, c["faint"],
               weight=500, tracking=2.4))

    b.append(hr(PAD, 216, RIGHT, c["rule"], 0.65))
    return doc(H, "\n".join(b), "Reach")


# ── footer rule ────────────────────────────────────────────────────────────
def footer(c):
    H = 64
    b = [hr(PAD, 32, RIGHT, c["rule"]),
         f'  <rect x="{PAD}" y="31" width="72" height="2" fill="{c["accent"]}"/>']
    return doc(H, "\n".join(b), "")


PANELS = dict(hero=hero, currently=currently, stack=stack,
              contact=contact, footer=footer)


def main():
    OUT.mkdir(exist_ok=True)
    if not PORTRAIT.exists():
        raise SystemExit("missing mitali/portrait.png")
    total = 0
    for name, fn in PANELS.items():
        for theme, c in (("light", LIGHT), ("dark", DARK)):
            p = OUT / f"{name}-{theme}.svg"
            body = fn(c)
            p.write_text(body, encoding="utf-8")
            kb = len(body.encode()) / 1024
            total += kb
            print(f"  {p.name:<24}{kb:8.1f} KB")
    print(f"\n  10 panels, {total:.0f} KB")


if __name__ == "__main__":
    main()
