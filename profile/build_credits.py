#!/usr/bin/env python3
"""End credits.

A slow, silent roll over the same ink the rest of the kit is printed on.
Every line is true: the eight repos, the real toolkit, the real origin.

Run: python3 build_credits.py
Out: credits.svg
"""
import pathlib
import random

random.seed(7)

HERE = pathlib.Path(__file__).parent

INK   = "#07060A"
CREAM = "#F2E8D5"
ASH   = "#8A8090"
DIM   = "#4A4353"
VERM  = "#C1272D"
VERM_L = "#E8453F"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

W, H = 1200, 340
TRAVEL = 64  # seconds for one full pass

SECTIONS = [
    ("STARRING", ["ANUJ PHULERA"]),
    ("ORIGIN", ["GURUGRAM · HARYANA · INDIA"]),
    ("GRADE", ["FIFTEEN · CLASS 10"]),
    ("SPECIALITY", ["INTERFACE SYSTEMS"]),
    ("THE EIGHT", [
        "VERDE PORTFOLIO",
        "VERDE APP",
        "NIRMAAN APP",
        "NIRMAN PORTFOLIO",
        "SKILL-VERSE",
        "RESONATE",
        "RAKSHABANDHAN",
        "VERDE PREVIOUS",
    ]),
    ("TOOLKIT", [
        "NEXT.JS · REACT · TYPESCRIPT",
        "TAILWIND · SUPABASE · GEMINI",
        "ESP32 · TENSORFLOW LITE",
    ]),
    ("SHOT ON LOCATION", ["IN A BROWSER TAB"]),
    ("SOUND", ["NONE. IT IS AN SVG."]),
    ("CHAPTER 001", ["THE SEAL"]),
]

# ── build the roll ──────────────────────────────────────────────────────────
body = []
y = 0.0
for label, lines in SECTIONS:
    y += 34
    body.append(
        f'<text x="{W / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="9" letter-spacing="5.5" fill="{DIM}">{label}</text>'
    )
    for line in lines:
        y += 23
        body.append(
            f'<text x="{W / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="12.5" letter-spacing="1.4" fill="{CREAM}" fill-opacity="0.88">{line}</text>'
        )
    y += 20

y += 30
body.append(f'<line x1="{W / 2 - 70}" y1="{y:.1f}" x2="{W / 2 + 70}" y2="{y:.1f}" stroke="{VERM}" stroke-opacity="0.55"/>')
y += 26
body.append(
    f'<text x="{W / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
    f'font-size="8.5" letter-spacing="3.6" fill="{ASH}">ANUJ PHULERA · 2026</text>'
)

TOTAL = y + 40

grain = "".join(
    f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, H):.0f}" '
    f'r="{random.uniform(0.3, 0.9):.1f}" fill="#FFFFFF" fill-opacity="0.04">'
    f'<animate attributeName="fill-opacity" values="0.015;0.05;0.02;0.06;0.015" '
    f'dur="{random.uniform(1.0, 2.4):.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(70)
)

scan = "".join(
    f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#000000" stroke-opacity="0.18" stroke-width="1"/>'
    for yy in range(0, H, 3)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="End credits">
  <defs>
    <linearGradient id="crTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}" stop-opacity="1"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="crBot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}" stop-opacity="0"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="1"/>
    </linearGradient>
    <radialGradient id="crGlow" cx="0.5" cy="0.5" r="0.6">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="crGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.014" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#crGrid)"/>
  <rect width="{W}" height="{H}" fill="url(#crGlow)"/>

  <!-- the roll -->
  <g>
    <animateTransform attributeName="transform" type="translate"
                      values="0 {H + 20};0 {-TOTAL:.1f}"
                      dur="{TRAVEL}s" repeatCount="indefinite"/>
    {''.join(body)}
  </g>

  <!-- fixed frame -->
  <g>
    <rect x="0" y="0" width="{W}" height="74" fill="url(#crTop)"/>
    <rect x="0" y="{H - 74}" width="{W}" height="74" fill="url(#crBot)"/>
  </g>

  <g>
    <text x="28" y="28" font-family="{MONO}" font-size="8.5" letter-spacing="3.6" fill="{ASH}">END CREDITS</text>
    <text x="{W - 28}" y="28" text-anchor="end" font-family="{MONO}" font-size="8.5" letter-spacing="3.4"
          fill="{ASH}" fill-opacity="0.8">CHAPTER 001 · THE SEAL</text>
    <line x1="28" y1="38" x2="{W - 28}" y2="38" stroke="{VERM}" stroke-opacity="0.22"/>

    <text x="28" y="{H - 15}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2" fill="{DIM}">
      SILENT · {TRAVEL} SECONDS · LOOPS
    </text>
    <circle cx="{W - 176}" cy="{H - 19}" r="3" fill="{VERM_L}">
      <animate attributeName="opacity" values="1;0.12;1" dur="1.4s" repeatCount="indefinite"/>
    </circle>
    <text x="{W - 164}" y="{H - 15}" font-family="{MONO}" font-size="8.5" letter-spacing="2.4" fill="{ASH}">END</text>
  </g>

  <g>{grain}</g>
  <g opacity="0.42">{scan}</g>
</svg>
'''

if __name__ == "__main__":
    (HERE / "credits.svg").write_text(svg, encoding="utf-8")
    print(f"wrote credits.svg  {len(svg):6d} bytes  {W}x{H}  roll={TOTAL:.0f}px / {TRAVEL}s")
