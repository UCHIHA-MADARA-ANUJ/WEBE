#!/usr/bin/env python3
"""Mitali Chincholikar — profile kit.

Eight panels, light and dark, all type outlined by typekit.py so the set
renders identically on every OS with no fonts installed.

The colour system is deliberately narrow: four accents drawn from her own
artwork, assigned one per section so the page reads as a document with
chapters rather than a plate of confetti.

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


# ── the four accents, one per section ──────────────────────────────────────
LIGHT = dict(
    ink="#111116", mid="#4A4A56", soft="#7C7C8A", faint="#8E8E9C",
    rule="#E5E5EB", wash="#F7F7F9",
    crimson="#A30D28", ember="#B4442C", rose="#A63A5E", indigo="#44577F",
)
DARK = dict(
    ink="#F5F5F7", mid="#BDBDC8", soft="#84848F", faint="#7E7E8C",
    rule="#282830", wash="#15151B",
    crimson="#F0637A", ember="#F08A6E", rose="#E86F94", indigo="#7C93C4",
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(s, x, y, size, fill, weight=400, tracking=0.0, anchor="start",
      family="Inter", opacity=None):
    return "  " + tk.text_path(s, x, y, size, family=family, weight=weight,
                               tracking=tracking, anchor=anchor, fill=fill,
                               opacity=opacity)


def M(s, x, y, size, fill, weight=500, tracking=0.0, anchor="start",
      opacity=None):
    return T(s, x, y, size, fill, weight=weight, tracking=tracking,
             anchor=anchor, family="JBMono", opacity=opacity)


def hr(x1, y, x2, color, opacity=1.0, width=1.0):
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
            f'stroke-width="{width}" opacity="{opacity}"/>')


def vr(x, y1, y2, color, opacity=1.0, width=1.0):
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" opacity="{opacity}"/>')


def rect(x, y, w, h, fill, opacity=None, rx=0):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    r = f' rx="{rx}"' if rx else ""
    return f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}"{o}/>'


def eyebrow(text, x, y, c, accent, rule_to=None):
    out = [M(text.upper(), x, y, 12, accent, weight=600, tracking=3.2),
           rect(x, y + 15, 36, 2, accent)]
    if rule_to is not None:
        out.append(hr(x + 50, y + 16, rule_to, c["rule"]))
    return "\n".join(out)


def doc(h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{esc(title)}">\n'
            f'{body}\n</svg>\n')


# ══ 1 · HERO ═══════════════════════════════════════════════════════════════
def hero(c):
    H = 604
    IW = 448
    IH = round(IW * 944 / 700)
    TX = IW + 64
    b = []
    b.append("  " + tk.image_tag(PORTRAIT, 0, 0, IW, IH, mime="image/jpeg"))
    b.append(rect(IW, 0, 1, IH, c["rule"]))

    y = 74
    b.append(eyebrow("Profile", TX, y, c, c["crimson"]))

    y += 100
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

    y += 42
    facts = [("Studying", "Computer Science", c["crimson"]),
             ("From year two", "AI \u00b7 ML", c["ember"]),
             ("Also", "Cybersecurity", c["indigo"])]
    span = (RIGHT - TX) / len(facts)
    for i, (k, v, col) in enumerate(facts):
        x = TX + i * span
        b.append(rect(x, y - 7, 3, 8, col))
        b.append(M(k.upper(), x + 12, y, 9, c["faint"], weight=500, tracking=2.4))
        b.append(T(v, x, y + 32, 18, c["ink"], weight=500, tracking=-0.2))

    return doc(H, "\n".join(b),
               "Mitali Chincholikar, Computer Science, first year, Pune, India")


# ══ 2 · STATS ══════════════════════════════════════════════════════════════
def stats(c):
    H = 214
    b = [rect(0, 0, W, H, c["wash"])]
    items = [("08", "languages in use", c["crimson"]),
             ("03", "study directions", c["ember"]),
             ("Y2", "AI / ML start", c["rose"]),
             ("01", "club leadership role", c["indigo"])]
    span = W / len(items)
    for i, (num, label, col) in enumerate(items):
        x = i * span + PAD
        b.append(T(num, x, 108, 62, col, weight=600, tracking=-2.2))
        b.append(M(label.upper(), x, 144, 9.5, c["soft"], weight=500,
                   tracking=2.2))
        if i:
            b.append(hr(x - 36, 58, x - 36, c["rule"]))
    return doc(H, "\n".join(b), "Eight languages, three directions")


# ══ 3 · ABOUT ══════════════════════════════════════════════════════════════
def about(c):
    H = 300
    b = [eyebrow("About", PAD, 62, c, c["rose"], rule_to=RIGHT)]
    lines = [
        "I am a first-year Computer Science student in Pune, studying",
        "three directions at once: computer science, artificial",
        "intelligence and cybersecurity. I run events for my college",
        "club, play badminton, and am usually in the middle of learning",
        "a language I have no immediate use for.",
    ]
    x = PAD + 30
    b.append(rect(PAD, 118, 3, 150, c["rose"], 0.9))
    y = 132
    for ln in lines:
        b.append(T(ln, x, y, 26, c["ink"], weight=400, tracking=-0.5))
        y += 38
    return doc(H, "\n".join(b), "About Mitali")


# ══ 4 · STUDYING (currently + education, merged) ══════════════════════════
def studying(c):
    """One section, not two.

    The old 'currently' and 'education' panels listed the same three things in
    different words. A reader notices repetition before they notice detail,
    so the two are merged into a single timeline that says each thing once,
    with the date on the left where a timeline puts it.
    """
    H = 372
    b = [eyebrow("Studying", PAD, 62, c, c["crimson"], rule_to=RIGHT)]

    rows = [
        ("Now", "Computer Science", "First year · Dnyan Prasad Global University",
         "Enrolled", c["crimson"]),
        ("Year 2", "Artificial intelligence", "and machine learning · specialisation begins",
         "Upcoming", c["ember"]),
        ("Ongoing", "Cybersecurity", "certification alongside the degree",
         "In progress", c["indigo"]),
    ]
    spine = PAD + 118
    b.append(vr(spine, 132, 348, c["rule"]))
    for i, (when, title, sub, tag, col) in enumerate(rows):
        y = 150 + i * 88
        b.append(M(when.upper(), PAD, y - 2, 10, col, weight=600, tracking=2.0))
        b.append(rect(spine - 6, y - 11, 12, 12, col, rx=6))
        b.append(T(title, spine + 40, y + 6, 30, c["ink"], weight=500, tracking=-0.9))
        b.append(T(sub, spine + 40, y + 34, 14.5, c["soft"], weight=400))
        b.append(M(tag.upper(), RIGHT, y + 6, 9.5, col, weight=600,
                   tracking=2.2, anchor="end"))
        if i < 2:
            b.append(hr(spine + 40, y + 58, RIGHT, c["rule"], 0.6))
    return doc(H, "\n".join(b), "Studying")


# ══ 5 · BEYOND ════════════════════════════════════════════════════════════
def beyond(c):
    H = 236
    b = [eyebrow("Beyond the course", PAD, 62, c, c["rose"], rule_to=RIGHT)]
    items = [("Event manager", "Swarang, her college club", c["rose"]),
             ("Badminton", "a game she actually plays", c["crimson"]),
             ("Tug of war", "team, not solo", c["ember"])]
    gap = 30
    cw = (RIGHT - PAD - gap * 2) / 3
    for i, (title, sub, col) in enumerate(items):
        x = PAD + i * (cw + gap)
        b.append(rect(x, 116, cw, 96, col, 0.055))
        b.append(rect(x, 116, 3, 96, col))
        b.append(T(title, x + 24, 160, 23, c["ink"], weight=500, tracking=-0.7))
        b.append(T(sub, x + 24, 186, 13.5, c["soft"], weight=400))
    return doc(H, "\n".join(b), "Beyond the course")


# ══ 6 · HIRE ═══════════════════════════════════════════════════════════════
def hire(c):
    H = 300
    b = [rect(0, 0, W, H, c["wash"]),
         eyebrow("What she brings", PAD, 62, c, c["crimson"])]

    b.append(T("Three directions, one first year.", PAD, 142, 42, c["ink"],
               weight=600, tracking=-1.5))

    points = [("Ships across five languages", c["crimson"]),
              ("Studies AI and security together", c["ember"]),
              ("Already runs events for a club", c["indigo"])]
    for i, (txt, col) in enumerate(points):
        y = 194 + i * 34
        b.append(rect(PAD, y - 9, 9, 9, col))
        b.append(T(txt, PAD + 24, y, 17, c["mid"], weight=400, tracking=-0.2))

    b.append(rect(RIGHT - 284, 116, 284, 116, c["crimson"], 0.07))
    b.append(rect(RIGHT - 284, 116, 3, 116, c["crimson"]))
    b.append(M("AVAILABLE FOR", RIGHT - 258, 154, 9.5, c["crimson"],
               weight=600, tracking=2.2))
    b.append(T("Internships", RIGHT - 258, 192, 27, c["ink"], weight=600,
               tracking=-0.8))
    b.append(T("and first projects", RIGHT - 258, 214, 16, c["mid"],
               weight=400))
    return doc(H, "\n".join(b), "What she brings")


# ══ 6 · WORKING WITH ═══════════════════════════════════════════════════════
def stack(c):
    H = 340
    b = [eyebrow("Working with", PAD, 62, c, c["ember"], rule_to=RIGHT)]
    langs = [("Python", "scripting", c["crimson"]), ("C", "systems", c["indigo"]),
             ("C++", "algorithms", c["indigo"]), ("Java", "objects", c["ember"]),
             ("SQL", "databases", c["rose"]), ("HTML / CSS", "interfaces", c["rose"]),
             ("JavaScript", "the web", c["ember"]), ("Node.js", "servers", c["rose"])]
    gap = 30
    cw = (RIGHT - PAD - gap * 3) / 4
    for i, (name, note, col) in enumerate(langs):
        x = PAD + (i % 4) * (cw + gap)
        row = i // 4
        y = 152 + row * 88
        b.append(rect(x, y - 34, 26, 3, col))
        b.append(T(name, x, y, 27, c["ink"], weight=500, tracking=-0.8))
        b.append(M(note.upper(), x, y + 26, 10, col, weight=600, tracking=1.8))
        if row == 0:
            b.append(hr(x, y + 52, x + cw - 10, c["rule"], 0.8))

    b.append(hr(PAD, 292, RIGHT, c["rule"], 0.7))
    b.append(M("DAY TO DAY", PAD, 324, 9, c["faint"], weight=500, tracking=2.4))
    for i, t in enumerate(["VS Code", "Windows", "Git"]):
        b.append(T(t, PAD + 128 + i * 136, 324, 15, c["mid"], weight=400))
    return doc(H, "\n".join(b), "Working with")


# ══ 7 · BEYOND ═════════════════════════════════════════════════════════════
# ══ 8 · HIRE ═══════════════════════════════════════════════════════════════
def hire(c):
    H = 320
    b = [rect(0, 0, W, H, c["wash"]),
         eyebrow("What she brings", PAD, 62, c, c["crimson"])]

    b.append(T("Three directions, one first year.", PAD, 138, 44, c["ink"],
               weight=600, tracking=-1.6))

    points = [("Ships across five languages", c["crimson"]),
              ("Studies AI and security together", c["ember"]),
              ("Already runs events for a club", c["indigo"])]
    y = 196
    for txt, col in points:
        b.append(rect(PAD, y - 9, 10, 10, col))
        b.append(T(txt, PAD + 28, y, 19, c["mid"], weight=400, tracking=-0.3))
        y += 38

    b.append(rect(RIGHT - 300, 128, 300, 128, c["crimson"], 0.07))
    b.append(rect(RIGHT - 300, 128, 3, 128, c["crimson"]))
    b.append(M("AVAILABLE FOR", RIGHT - 272, 172, 9, c["crimson"], weight=600,
               tracking=2.4))
    b.append(T("Internships", RIGHT - 272, 208, 26, c["ink"], weight=600,
               tracking=-0.8))
    b.append(T("and first projects", RIGHT - 272, 236, 17, c["mid"],
               weight=400))
    return doc(H, "\n".join(b), "What she brings")


# ══ 9 · REACH ══════════════════════════════════════════════════════════════
def contact(c):
    H = 288
    b = [eyebrow("Reach", PAD, 62, c, c["crimson"], rule_to=RIGHT)]
    b.append(T("chincholikarmitali@gmail.com", PAD, 168, 42, c["ink"],
               weight=500, tracking=-1.1))
    b.append(rect(PAD, 192, 505, 3, c["crimson"]))
    b.append(M("CLICK TO WRITE", PAD, 226, 9.5, c["faint"], weight=500,
               tracking=2.4))

    b.append(M("DISCORD", RIGHT - 210, 226, 9, c["faint"], weight=500,
               tracking=2.4, anchor="end"))
    b.append(T("lunar._.uchiha_", RIGHT, 226, 15, c["mid"], weight=400,
               anchor="end"))
    return doc(H, "\n".join(b), "Reach")


# ══ 10 · FOOTER ════════════════════════════════════════════════════════════
def footer(c):
    H = 78
    b = [hr(PAD, 39, RIGHT, c["rule"])]
    for i, col in enumerate([c["crimson"], c["ember"], c["rose"], c["indigo"]]):
        b.append(rect(PAD + i * 20, 37, 20, 3, col))
    b.append(M("PUNE \u00b7 MAHARASHTRA \u00b7 INDIA", RIGHT, 44, 9,
               c["faint"], weight=500, tracking=2.4, anchor="end"))
    return doc(H, "\n".join(b), "")


PANELS = dict(hero=hero, stats=stats, about=about, studying=studying,
              stack=stack, beyond=beyond, hire=hire, contact=contact,
              footer=footer)


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
    print(f"\n  {len(PANELS) * 2} panels, {total:.0f} KB")


if __name__ == "__main__":
    main()
