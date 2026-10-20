#!/usr/bin/env python3
"""Wave three: the pieces that make it look engineered, not decorated.

  stats.svg    attribute sheet - animated kekkei genkai bars + rank medallion
  arsenal.svg  custom tech grid, self-hosted (no shields.io dependency)

Run after build_svgs.py:  python3 build_extra2.py
"""
import pathlib

from build_svgs import (
    DEFS, VOID, INK, BLOOD, CRIMSON, SCARLET, BLAZE, EMBER, GOLD,
    IVORY, ASH, DIM, MONO, SERIF, BLACK,
)
from build_extra import EXTRA_DEFS, stage3

HERE = pathlib.Path(__file__).parent


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ─── stats.svg ───────────────────────────────────────────────────────────────
SW_, SH_ = 1000, 396
ROWS = [
    ("INTERFACE SYSTEMS",      96, "#E01E2B"),
    ("BEHAVIOURAL ENGINE",     92, "#F0413F"),
    ("FULL-STACK",             88, "#FF5A3C"),
    ("AI / LLM PIPELINES",     84, "#FF7A18"),
    ("DESIGN / MOTION",        90, "#FF8C2B"),
    ("HARDWARE / IoT",         78, "#FFB020"),
]

BAR_X, BAR_W = 268, 470
ROW_Y0, ROW_GAP = 138, 40
DELAY0 = 0.35


def bar_row(i, label, val, colour):
    y = ROW_Y0 + i * ROW_GAP
    w = BAR_W * val / 100.0
    delay = DELAY0 + i * 0.13
    return f'''
  <g>
    <text x="62" y="{y + 5}" font-family="{MONO}" font-size="10.5" letter-spacing="2.1" fill="{ASH}">{esc(label)}</text>

    <rect x="{BAR_X}" y="{y - 7}" width="{BAR_W}" height="9" rx="4.5" fill="#FFFFFF" fill-opacity="0.055"/>
    <rect x="{BAR_X}" y="{y - 7}" width="0" height="9" rx="4.5" fill="{colour}" fill-opacity="0.92">
      <animate attributeName="width" from="0" to="{w:.0f}" dur="1.25s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
    </rect>
    <rect x="{BAR_X}" y="{y - 7}" width="{w:.0f}" height="9" rx="4.5" fill="{colour}" fill-opacity="0.18" opacity="0">
      <animate attributeName="opacity" from="0" to="0.55" dur=".4s" begin="{delay + 1.1:.2f}s" fill="freeze"/>
    </rect>

    <text x="{BAR_X + BAR_W + 18}" y="{y + 5}" font-family="{MONO}" font-size="10.5" letter-spacing="1.4" fill="{IVORY}" text-anchor="start" opacity="0">
      {val}
      <animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{delay + 0.85:.2f}s" fill="freeze"/>
    </text>
  </g>'''


stats = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SW_}" height="{SH_}" viewBox="0 0 {SW_} {SH_}" fill="none" role="img" aria-label="Attribute sheet">
{DEFS}
{EXTRA_DEFS}
  <rect width="{SW_}" height="{SH_}" rx="10" fill="url(#cardGrad)"/>
  <rect width="{SW_}" height="{SH_}" rx="10" fill="url(#grain)"/>
  <rect x="0.75" y="0.75" width="{SW_ - 1.5}" height="{SH_ - 1.5}" rx="9.5" fill="none" stroke="{CRIMSON}" stroke-opacity="0.32" stroke-width="1.5"/>

  <rect x="0" y="0" width="5" height="{SH_}" fill="{CRIMSON}" fill-opacity="0.5"/>

  <text x="34" y="40" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{ASH}">KEKKEI GENKAI · ATTRIBUTE SHEET</text>
  <text x="{SW_ - 34}" y="40" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{BLAZE}" text-anchor="end">UNIT 001</text>
  <line x1="34" y1="56" x2="{SW_ - 34}" y2="56" stroke="{CRIMSON}" stroke-opacity="0.28"/>

  <!-- medallion -->
  <g transform="translate(892,206) scale(0.62)">{stage3(0, 0, 108, dur="9s")}</g>
  <circle cx="892" cy="206" r="86" fill="none" stroke="{CRIMSON}" stroke-opacity="0.22" stroke-width="1">
    <animate attributeName="r" values="84;90;84" dur="5s" repeatCount="indefinite"/>
  </circle>
  <text x="892" y="318" font-family="{BLACK}" font-size="17" letter-spacing="3" fill="{IVORY}" text-anchor="middle">S-RANK</text>
  <text x="892" y="336" font-family="{MONO}" font-size="8.5" letter-spacing="2.4" fill="{DIM}" text-anchor="middle">NO RECORDED DEFEATS</text>

  {''.join(bar_row(i, *r) for i, r in enumerate(ROWS))}

  <line x1="34" y1="{ROW_Y0 + len(ROWS) * ROW_GAP + 4}" x2="{SW_ - 34}" y2="{ROW_Y0 + len(ROWS) * ROW_GAP + 4}" stroke="{CRIMSON}" stroke-opacity="0.2"/>

  <text x="34" y="{ROW_Y0 + len(ROWS) * ROW_GAP + 30}" font-family="{MONO}" font-size="9" letter-spacing="2.6" fill="{DIM}">01 UCHIHA · INTERFACE ENGINEER · JAIPUR</text>
  <text x="{SW_ - 34}" y="{ROW_Y0 + len(ROWS) * ROW_GAP + 30}" font-family="{MONO}" font-size="9" letter-spacing="2.6" fill="{DIM}" text-anchor="end">ACTIVE</text>
</svg>
'''


# ─── arsenal.svg ─────────────────────────────────────────────────────────────
AW, AH = 1000, 268
GROUPS = [
    ("FRONTEND",  ["TypeScript", "React", "Next.js", "Tailwind", "Vite"], "#C1121F"),
    ("BACKEND",   ["Node", "Firebase", "Supabase", "Postgres", "REST"], "#8B0A14"),
    ("MOTION",    ["Three.js", "GSAP", "GLSL", "Framer", "SMIL"], "#FF7A18"),
    ("HARDWARE",  ["ESP32", "C++", "TFLite", "KiCad", "MQTT"], "#FFB020"),
]


def pill(x, y, text, colour):
    w = len(text) * 7.15 + 30
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{colour}" fill-opacity="0.10" '
        f'stroke="{colour}" stroke-opacity="0.42"/>'
        f'<circle cx="{x + 13}" cy="{y + 13}" r="2.6" fill="{colour}"/>'
        f'<text x="{x + 23}" y="{y + 17.5}" font-family="{MONO}" font-size="10.5" fill="{IVORY}">{esc(text)}</text>',
        w,
    )


rows_svg = []
y = 92
for name, items, colour in GROUPS:
    parts = [f'<text x="34" y="{y + 18}" font-family="{MONO}" font-size="9.5" letter-spacing="2.8" fill="{ASH}">{name}</text>']
    x = 176
    for it in items:
        frag, w = pill(x, y, it, colour)
        parts.append(frag)
        x += w + 9
    rows_svg.append("".join(parts))
    y += 42

arsenal = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{AW}" height="{AH}" viewBox="0 0 {AW} {AH}" fill="none" role="img" aria-label="Arsenal">
{DEFS}
{EXTRA_DEFS}
  <rect width="{AW}" height="{AH}" rx="10" fill="url(#cardGrad)"/>
  <rect width="{AW}" height="{AH}" rx="10" fill="url(#grain)"/>
  <rect x="0.75" y="0.75" width="{AW - 1.5}" height="{AH - 1.5}" rx="9.5" fill="none" stroke="{CRIMSON}" stroke-opacity="0.32" stroke-width="1.5"/>
  <rect x="0" y="0" width="5" height="{AH}" fill="{CRIMSON}" fill-opacity="0.5"/>

  <text x="34" y="42" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{ASH}">ARSENAL</text>
  <text x="{AW - 34}" y="42" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{DIM}" text-anchor="end">SELF-HOSTED · NO EXTERNAL BADGES</text>
  <line x1="34" y1="58" x2="{AW - 34}" y2="58" stroke="{CRIMSON}" stroke-opacity="0.28"/>

  {''.join(rows_svg)}

  <line x1="34" y1="{y + 4}" x2="{AW - 34}" y2="{y + 4}" stroke="{CRIMSON}" stroke-opacity="0.2"/>
  <text x="34" y="{y + 30}" font-family="{MONO}" font-size="9" letter-spacing="2.4" fill="{DIM}">TWENTY TOOLS · ONE OBSESSION</text>
</svg>
'''

if __name__ == "__main__":
    for name, content in [("stats.svg", stats), ("arsenal.svg", arsenal)]:
        (HERE / name).write_text(content, encoding="utf-8")
        print(f"wrote {name:14s} {len(content):6d} bytes")
