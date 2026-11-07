#!/usr/bin/env python3
"""Right Now — three boards, one hand.

Replaces the emoji table in the README with three instrument panels: what is
being built, grown and shipped at the moment, with the real specs on them.

Run: python3 build_now.py
Out: now.svg
"""
import pathlib

HERE = pathlib.Path(__file__).parent

INK   = "#07060A"
CARD  = "#0E0B11"
CREAM = "#F2E8D5"
ASH   = "#8A8090"
DIM   = "#4A4353"
VERM  = "#C1272D"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

W = 1200
PAD, GAP = 10, 17
CW = (W - PAD * 2 - GAP * 2) // 3      # 382
CH = 262
H = PAD * 2 + CH + 24

BOARDS = [
    {
        "idx": "01",
        "state": "BUILDING",
        "name": "DEEP FIELD",
        "line": "a living atlas with no fixed interface",
        "accent": "#4FB3D9",
        "specs": ["SIX STRUCTURAL PARADIGMS", "ELEVEN BEHAVIOURAL SIGNALS", "NINE-SECOND COOLDOWN"],
    },
    {
        "idx": "02",
        "state": "GROWING",
        "name": "VERDE",
        "line": "a vertical farm that waters itself",
        "accent": "#5BD69B",
        "specs": ["ESP32 FIRMWARE", "TFLITE DISEASE MODEL", "HINDI / ENGLISH CHANNEL"],
    },
    {
        "idx": "03",
        "state": "SHIPPING",
        "name": "NIRMAAN",
        "line": "an AI e-waste pickup network for India",
        "accent": "#C1272D",
        "specs": ["THREE ROLES", "LIVE ROUTING", "END-TO-END BOOKINGS"],
    },
]


def board(i, b):
    x = PAD + i * (CW + GAP)
    y = PAD
    a = b["accent"]
    specs = "".join(
        f'<circle cx="{x + 18}" cy="{y + 176 + k * 22}" r="2" fill="{a}" fill-opacity="0.85"/>'
        f'<text x="{x + 28}" y="{y + 179 + k * 22}" font-family="{MONO}" font-size="8.6" '
        f'letter-spacing="1.7" fill="{ASH}">{t}</text>'
        for k, t in enumerate(b["specs"])
    )
    return f'''
  <g>
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="7" fill="{CARD}" stroke="#FFFFFF" stroke-opacity="0.07"/>
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="7" fill="{a}" fill-opacity="0.018"/>

    <rect x="{x}" y="{y}" width="{CW}" height="2" rx="1" fill="{a}" fill-opacity="0.65"/>
    <rect x="{x}" y="{y}" width="70" height="2" rx="1" fill="#FFFFFF" fill-opacity="0.9">
      <animateTransform attributeName="transform" type="translate"
                        values="-70 0;{CW + 20} 0" dur="4.6s" begin="{i * 1.4:.1f}s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" values="0;0.55;0.2;0.5;0" dur="4.6s"
               begin="{i * 1.4:.1f}s" repeatCount="indefinite"/>
    </rect>

    <text x="{x + CW - 18}" y="{y + 62}" text-anchor="end" font-family="{BLACK}" font-size="46"
          fill="#FFFFFF" fill-opacity="0.045">{b["idx"]}</text>

    <circle cx="{x + 22}" cy="{y + 30}" r="3.4" fill="{a}">
      <animate attributeName="opacity" values="1;0.15;1" dur="1.9s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/>
    </circle>
    <text x="{x + 34}" y="{y + 33.5}" font-family="{MONO}" font-size="9" letter-spacing="3"
          fill="{a}" fill-opacity="0.9">{b["state"]}</text>

    <text x="{x + 18}" y="{y + 86}" font-family="{BLACK}" font-size="23" letter-spacing="1.2"
          fill="{CREAM}">{b["name"]}</text>
    <text x="{x + 18}" y="{y + 108}" font-family="{MONO}" font-size="9.2" letter-spacing="0.9"
          fill="{DIM}">{b["line"]}</text>

    <line x1="{x + 18}" y1="{y + 130}" x2="{x + CW - 18}" y2="{y + 130}"
          stroke="#FFFFFF" stroke-opacity="0.06"/>
    <text x="{x + 18}" y="{y + 152}" font-family="{MONO}" font-size="7.6" letter-spacing="2.6"
          fill="{DIM}">ON THE BENCH</text>

    {specs}

    <line x1="{x + 18}" y1="{y + CH - 34}" x2="{x + CW - 18}" y2="{y + CH - 34}"
          stroke="{a}" stroke-opacity="0.18"/>
    <text x="{x + 18}" y="{y + CH - 16}" font-family="{MONO}" font-size="7.8" letter-spacing="2.4"
          fill="{a}" fill-opacity="0.7">STATUS · LIVE</text>
    <text x="{x + CW - 18}" y="{y + CH - 16}" text-anchor="end" font-family="{MONO}" font-size="7.8"
          letter-spacing="1.8" fill="{DIM}">GURUGRAM</text>
  </g>'''


boards = "".join(board(i, b) for i, b in enumerate(BOARDS))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Right now: DEEP FIELD, VERDE, NIRMAAN">
  <defs>
    <radialGradient id="nwGlow" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="nwGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.014" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#nwGrid)"/>
  <rect width="{W}" height="{H}" fill="url(#nwGlow)"/>
{boards}
  <text x="{W / 2}" y="{H - 4}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.4" fill="{ASH}" fill-opacity="0.6">THREE FRONTS · ONE OPERATOR</text>
</svg>
'''

if __name__ == "__main__":
    (HERE / "now.svg").write_text(svg, encoding="utf-8")
    print(f"wrote now.svg  {len(svg):6d} bytes  {W}x{H}")
