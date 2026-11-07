#!/usr/bin/env python3
"""Mitali Chincholikar — profile kit.

Everything is geometry: type is converted to outlines by typekit.py, so the
panels render identically on macOS, Windows, Linux and Android with no fonts
installed. Nothing animates. Every panel ships as a light/dark pair.

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
PAD = 72
RIGHT = W - PAD


# ── palettes ────────────────────────────────────────────────────────────────
LIGHT = dict(
    ink="#111116",
    mid="#4A4A56",
    soft="#7C7C8A",
    faint="#A6A6B2",
    rule="#E5E5EB",
    accent="#A30D28",
)
DARK = dict(
    ink="#F5F5F7",
    mid="#BDBDC8",
    soft="#84848F",
    faint="#5C5C68",
    rule="#282830",
    accent="#F0637A",
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(s, x, y, size, fill, weight=400, tracking=0.0, anchor="start",
      family="Inter", opacity=None):
    return "  " + tk.text_path(s, x, y, size, family=family, weight=weight,
                               tracking=tracking, anchor=anchor, fill=fill,
                               opacity=opacity)


def M(s, x, y, size, fill, weight=500, tracking=0.0, anchor="start"):
    return T(s, x, y, size, fill, weight=weight, tracking=tracking,
             anchor=anchor, family="JBMono")


def hr(x1, y, x2, color, opacity=1.0, width=1.0):
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
            f'stroke-width="{width}" opacity="{opacity}"/>')


def vr(x, y1, y2, color, opacity=1.0, width=1.0):
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" opacity="{opacity}"/>')


def eyebrow(text, x, y, c, rule_to=None):
    """The one repeated device across every panel. Consistency is the design."""
    out = [M(text.upper(), x, y, 10.5, c["accent"], weight=600, tracking=3.6),
           f'  <rect x="{x}" y="{y + 14}" width="34" height="2" fill="{c["accent"]}"/>']
    if rule_to is not None:
        out.append(hr(x + 46, y + 15, rule_to, c["rule"]))
    return "\n".join(out)


def doc(h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{esc(title)}">\n'
            f'{body}\n</svg>\n')


# ══ 1 · THE HERO ═══════════════════════════════════════════════════════════
def hero(c):
    H = 604
    IW = 448                       # portrait block, bleeding left and bottom
    TX = IW + 64                   # type column
    b = []

    # portrait, cropped to the block and bled into three edges
    IH = round(IW * 944 / 700)     # exact ratio of the cropped artwork
    b.append("  " + tk.image_tag(PORTRAIT, 0, 0, IW, IH, mime="image/jpeg"))
    b.append(f'  <rect x="{IW}" y="0" width="1" height="{IH}" fill="{c["rule"]}"/>')

    y = 78
    b.append(eyebrow("Profile", TX, y, c))

    y += 96
    b.append(T("Mitali", TX, y, 88, c["ink"], weight=600, tracking=-2.8))
    y += 96
    b.append(T("Chincholikar", TX, y, 88, c["ink"], weight=600, tracking=-2.8))

    y += 58
    b.append(T("Computer Science \u00b7 First Year", TX, y, 23, c["mid"],
               weight=400, tracking=-0.2))

    y += 38
    b.append(M("PUNE \u00b7 MAHARASHTRA \u00b7 INDIA", TX, y, 11.5, c["soft"],
               weight=500, tracking=3.0))

    y += 44
    b.append(hr(TX, y, RIGHT, c["rule"]))

    y += 40
    facts = [("Studying", "Computer Science"),
             ("From year two", "AI \u00b7 ML"),
             ("Also", "Cybersecurity")]
    span = (RIGHT - TX) / len(facts)
    for i, (k, v) in enumerate(facts):
        x = TX + i * span
        b.append(M(k.upper(), x, y, 9, c["faint"], weight=500, tracking=2.4))
        b.append(T(v, x, y + 30, 18, c["ink"], weight=500, tracking=-0.2))

    return doc(H, "\n".join(b),
               "Mitali Chincholikar, Computer Science, first year, Pune, India")


# ══ 2 · CURRENTLY ══════════════════════════════════════════════════════════
def currently(c):
    H = 292
    b = [eyebrow("Currently", PAD, 62, c, rule_to=RIGHT)]

    cards = [
        ("01", "Computer Science", "First year \u00b7 Dnyan Prasad Global University", "Enrolled"),
        ("02", "Artificial intelligence", "and machine learning \u00b7 begins in year two", "Upcoming"),
        ("03", "Cybersecurity", "course in progress", "Now"),
    ]
    gap = 30
    cw = (RIGHT - PAD - gap * 2) / 3
    for i, (num, title, sub, tag) in enumerate(cards):
        x = PAD + i * (cw + gap)
        b.append(hr(x, 132, x + cw, c["rule"]))
        b.append(M(num, x, 172, 10, c["faint"], weight=500, tracking=2.4))
        b.append(M(tag.upper(), x + cw, 172, 9, c["accent"], weight=600,
                   tracking=2.4, anchor="end"))
        b.append(T(title, x, 216, 26, c["ink"], weight=500, tracking=-0.7))
        b.append(T(sub, x, 246, 14.5, c["soft"], weight=400))
    return doc(H, "\n".join(b), "Currently")


# ══ 3 · WORKING WITH ═══════════════════════════════════════════════════════
def stack(c):
    H = 330
    b = [eyebrow("Working with", PAD, 62, c, rule_to=RIGHT)]

    langs = [("Python", "scripting"), ("C", "systems"),
             ("C++", "algorithms"), ("Java", "objects"),
             ("SQL", "databases"), ("HTML / CSS", "interfaces"),
             ("JavaScript", "the web"), ("Node.js", "servers")]
    gap = 30
    cw = (RIGHT - PAD - gap * 3) / 4
    for i, (name, note) in enumerate(langs):
        x = PAD + (i % 4) * (cw + gap)
        row = i // 4
        y = 156 + row * 84
        b.append(T(name, x, y, 27, c["ink"], weight=500, tracking=-0.8))
        b.append(M(note.upper(), x, y + 26, 8.5, c["faint"], weight=500,
                   tracking=1.9))
        if row == 0:
            b.append(hr(x, y + 52, x + cw - 10, c["rule"], 0.8))

    b.append(hr(PAD, 288, RIGHT, c["rule"], 0.7))
    b.append(M("DAY TO DAY", PAD, 314, 9, c["faint"], weight=500, tracking=2.4))
    for i, t in enumerate(["VS Code", "Windows", "Git"]):
        b.append(T(t, PAD + 128 + i * 136, 314, 15, c["mid"], weight=400))
    return doc(H, "\n".join(b), "Working with")


# ══ 4 · REACH ══════════════════════════════════════════════════════════════
def contact(c):
    H = 268
    b = [eyebrow("Reach", PAD, 62, c, rule_to=RIGHT)]
    b.append(T("chincholikarmitali@gmail.com", PAD, 156, 40, c["ink"],
               weight=500, tracking=-1.0))
    b.append(f'  <rect x="{PAD}" y="178" width="486" height="3" fill="{c["accent"]}"/>')
    b.append(M("EMAIL", PAD, 210, 9, c["faint"],
               weight=500, tracking=2.4))
    return doc(H, "\n".join(b), "Reach")


# ══ 5 · FOOTER ═════════════════════════════════════════════════════════════
def footer(c):
    H = 72
    b = [hr(PAD, 36, RIGHT, c["rule"]),
         f'  <rect x="{PAD}" y="35" width="68" height="2" fill="{c["accent"]}"/>']
    return doc(H, "\n".join(b), "")


PANELS = dict(hero=hero, currently=currently, stack=stack,
              contact=contact, footer=footer)


def main():
    OUT.mkdir(exist_ok=True)
    if not PORTRAIT.exists():
        raise SystemExit("missing mitali/portrait.jpg")
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
