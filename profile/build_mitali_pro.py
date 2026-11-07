#!/usr/bin/env python3
"""Mitali Chincholikar — professional profile kit.

Design rules, and they are rules, not suggestions:

  · No chapters, no timecodes, no REC dots, no eclipse, no stamps.
    A profile is a document, not a title sequence.
  · Nothing moves. A static SVG cannot break, cannot be caught mid-frame,
    and cannot be dramatic at the wrong moment.
  · Two grades only: one neutral ramp and one accent, taken from her own
    artwork. No colour is allowed in unless it earns its place.
  · Light and dark are built as a pair and shipped as a pair. A profile
    that only works in one theme is half a profile.
  · Text is left-aligned on a single optical margin. Nothing is centred,
    because centred text is a poster habit.
  · Every string in here is a fact she gave us. No invented claims.

    python3 build_mitali_pro.py
"""
import pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "mitali"

W = 1200
MARGIN = 72
RIGHT = W - MARGIN

SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
        "Helvetica, Arial, sans-serif")

# ── palettes ────────────────────────────────────────────────────────────────
LIGHT = dict(
    ink="#16161C",      # primary text
    soft="#5C5C68",     # secondary text
    faint="#9696A2",    # tertiary
    rule="#E3E3E9",     # hairlines
    accent="#B0132F",   # her red, held back
    accent_soft="#D7687A",
)
DARK = dict(
    ink="#F3F3F5",
    soft="#A2A2AE",
    faint="#6E6E7A",
    rule="#2B2B35",
    accent="#E8576C",
    accent_soft="#8E2434",
)


# ── primitives ──────────────────────────────────────────────────────────────
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, weight=400, ls=0.0, anchor=None, opacity=1.0):
    bits = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"',
            f'font-weight="{weight}"', f'fill="{fill}"']
    if ls:
        bits.append(f'letter-spacing="{ls}"')
    if anchor:
        bits.append(f'text-anchor="{anchor}"')
    if opacity != 1.0:
        bits.append(f'opacity="{opacity}"')
    return (f'  <text {" ".join(bits)}>{esc(s)}</text>')


def label(x, y, s, c):
    """Small caps eyebrow. The only place tracking gets loud."""
    return text(x, y, s.upper(), 10.5, c["soft"], weight=600, ls=3.2)


def rule(x1, x2, y, c, opacity=1.0):
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
            f'stroke="{c["rule"]}" stroke-width="1" opacity="{opacity}"/>')


def doc(h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{esc(title)}">\n'
            f'  {body}\n'
            f'</svg>\n')


# ── panels ──────────────────────────────────────────────────────────────────
def header(c):
    """Name, discipline, place. The whole identity in three lines."""
    b = []
    # a single accent tick, the only filled shape in the kit
    b.append(f'  <rect x="{MARGIN}" y="96" width="30" height="3" fill="{c["accent"]}"/>')
    b.append(text(MARGIN, 168, "MITALI CHINCHOLIKAR", 46, c["ink"],
                  weight=600, ls=5.4))
    b.append(text(MARGIN, 208, "Computer Science \u00b7 First Year", 17, c["soft"],
                  weight=400, ls=0.2))
    b.append(text(MARGIN, 240, "PUNE \u00b7 MAHARASHTRA \u00b7 INDIA", 11, c["faint"],
                  weight=600, ls=2.9))
    b.append(rule(MARGIN, RIGHT, 292, c))
    return doc(300, "\n".join(b),
               "Mitali Chincholikar, Computer Science, First Year, Pune, India")


def focus(c):
    """Three rows, tabular. A list is calmer than a diagram."""
    rows = [
        ("01", "Computer Science, first year", "Dnyan Prasad Global University"),
        ("02", "Artificial intelligence and machine learning", "from year two"),
        ("03", "Cybersecurity", "course in progress"),
    ]
    b = [label(MARGIN, 44, "Currently", c), rule(MARGIN, RIGHT, 62, c)]
    y = 106
    for num, main, sub in rows:
        b.append(text(MARGIN, y, num, 10.5, c["accent"], weight=600, ls=1.6))
        b.append(text(MARGIN + 52, y, main, 16.5, c["ink"], weight=400))
        b.append(text(RIGHT, y, sub, 12, c["faint"], weight=400, anchor="end"))
        y += 44
    return doc(206, "\n".join(b), "Currently")


def stack(c):
    """Eight languages, four columns. No bars, no percentages, no ranking."""
    items = ["Python", "C", "C++", "Java", "SQL", "HTML / CSS",
             "JavaScript", "Node.js"]
    cols = [MARGIN, 330, 588, 846]
    b = [label(MARGIN, 44, "Working with", c), rule(MARGIN, RIGHT, 62, c)]
    for i, it in enumerate(items):
        x = cols[i % 4]
        y = 104 + (i // 4) * 38
        b.append(text(x, y, it, 15.5, c["ink"], weight=400))
    b.append(rule(MARGIN, RIGHT, 168, c, 0.7))
    b.append(text(MARGIN, 196, "Day to day", 12, c["faint"], weight=400))
    b.append(text(MARGIN + 96, 196, "VS Code \u00b7 Windows", 12.5,
                  c["soft"], weight=400))
    return doc(214, "\n".join(b), "Working with")


def contact(c):
    """Mail is the front door. The card is wrapped in mailto by the README."""
    b = [label(MARGIN, 44, "Reach", c), rule(MARGIN, RIGHT, 62, c)]
    b.append(text(MARGIN, 112, "chincholikarmitali@gmail.com", 19, c["accent"],
                  weight=500, ls=0.2))
    b.append(text(RIGHT, 112, "Discord \u00b7 lunar._.uchiha_", 12.5, c["faint"],
                  weight=400, anchor="end"))
    return doc(150, "\n".join(b), "Reach")


def divider(c):
    b = [f'  <line x1="{MARGIN}" y1="4" x2="{RIGHT}" y2="4" stroke="{c["rule"]}" stroke-width="1"/>',
         f'  <line x1="{MARGIN}" y1="4" x2="{MARGIN + 44}" y2="4" stroke="{c["accent"]}" stroke-width="1"/>']
    return doc(8, "\n".join(b), "Divider")


PANELS = {"header": header, "focus": focus, "stack": stack,
          "contact": contact, "divider": divider}


def main():
    OUT.mkdir(exist_ok=True)
    made = []
    for name, fn in PANELS.items():
        for theme, c in (("light", LIGHT), ("dark", DARK)):
            p = OUT / f"{name}-{theme}.svg"
            p.write_text(fn(c), encoding="utf-8")
            made.append((p.name, len(p.read_text(encoding="utf-8"))))
    for n, size in made:
        print(f"  {n:<22}{size:>7} b")
    print(f"\n{len(made)} panels")


if __name__ == "__main__":
    main()
