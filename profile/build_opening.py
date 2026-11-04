#!/usr/bin/env python3
"""Anuj Phulera — the opening.

Design rule: FRAME ZERO IS THE POSTER.

Nothing hides behind an opacity-0 gate waiting for a clock to start. Every
element is fully painted at t=0 at full strength; the animation only adds
life on top — the spiral turns, the ticks counter-rotate, the eight project
chips pulse in sequence, a light crosses the name, the seal ring breathes.

If the SMIL clock never runs — phone, reduced motion, deferred decode,
GitHub's file viewer — you still land on a finished title card.

Run:  python3 build_opening.py
"""
import math
import pathlib
import random

random.seed(23)
HERE = pathlib.Path(__file__).parent

INK      = "#07060A"
CREAM    = "#F2E8D5"
SAND     = "#C9BBA3"
ASH      = "#93899B"
DIM      = "#5C5466"
VERM     = "#C1272D"
VERM_L   = "#E8453F"
CHAKRA   = "#4FB3D9"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

W, H = 1200, 700
BAR = 44

CX = 600
RING_CY = 268
RING_R = 142
NAME_Y = 486
CHIP_Y = 596


def grain(w, h, n=58):
    return "".join(
        f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.uniform(0.3, 0.95):.1f}" fill="#FFFFFF" fill-opacity="0.045">'
        f'<animate attributeName="fill-opacity" values="0.02;0.06;0.03;0.065;0.02" '
        f'dur="{random.uniform(1.0, 2.4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(n)
    )


def scan(w, h, step=3):
    return "".join(
        f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#000000" stroke-opacity="0.16" stroke-width="1"/>'
        for y in range(0, h, step)
    )


def spiral_d(r0, r1, turns, steps=340):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        pts.append((r * math.cos(th), r * math.sin(th)))
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts)


# ── seal ring ticks, all painted ────────────────────────────────────────────
ticks = []
for i in range(72):
    ang = 2 * math.pi * i / 72 - math.pi / 2
    major = i % 6 == 0
    r0 = RING_R + 10
    r1 = RING_R + (26 if major else 17)
    ticks.append(
        f'<line x1="{r0 * math.cos(ang):.1f}" y1="{r0 * math.sin(ang):.1f}" '
        f'x2="{r1 * math.cos(ang):.1f}" y2="{r1 * math.sin(ang):.1f}" '
        f'stroke="{VERM_L if major else VERM}" stroke-opacity="{0.55 if major else 0.26}" '
        f'stroke-width="{1.2 if major else 0.8}"/>'
    )
ticks = "".join(ticks)

# ── the eight, as chips ─────────────────────────────────────────────────────
PROJECTS = [
    ("VERDE PORTFOLIO",    "#5BD69B"),
    ("VERDE APP",          "#4FB3D9"),
    ("NIRMAAN APP",        "#00E08A"),
    ("NIRMAN PORTFOLIO",   "#C1272D"),
    ("SKILL-VERSE",        "#7C6BF0"),
    ("RESONATE",           "#E0563F"),
    ("RAKSHABANDHAN",      "#E8A33D"),
    ("VERDE PREVIOUS",     "#6E8B7A"),
]
CW_, GAP_ = 132, 8
total = len(PROJECTS) * CW_ + (len(PROJECTS) - 1) * GAP_
x0 = CX - total / 2
chips = []
for i, (name, col) in enumerate(PROJECTS):
    cx = x0 + i * (CW_ + GAP_)
    chips.append(
        f'<g>'
        f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="28" rx="3" '
        f'fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.32"/>'
        f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="1.4" fill="{col}" fill-opacity="0.75"/>'
        f'<circle cx="{cx + 11:.1f}" cy="{CHIP_Y + 14}" r="2.4" fill="{col}">'
        f'<animate attributeName="fill-opacity" values="0.3;1;0.3" dur="3.6s" '
        f'begin="{i * 0.3:.2f}s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx + 20:.1f}" y="{CHIP_Y + 17.5}" font-family="{MONO}" font-size="6.6" '
        f'letter-spacing="0.7" fill="{CREAM}" fill-opacity="0.85">{name}</text>'
        f'</g>'
    )
chips = "".join(chips)


def build():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — the seal">
  <defs>
    <radialGradient id="sealGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.20"/>
      <stop offset="0.40" stop-color="{VERM}" stop-opacity="0.08"/>
      <stop offset="0.72" stop-color="{VERM}" stop-opacity="0.04"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sealSky" cx="0.5" cy="0.40" r="0.66">
      <stop offset="0" stop-color="#160A0E"/>
      <stop offset="0.55" stop-color="#0B0709"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <linearGradient id="sealRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{VERM_L}"/>
      <stop offset="0.35" stop-color="{VERM}"/>
      <stop offset="0.62" stop-color="{VERM_L}"/>
      <stop offset="0.82" stop-color="{CHAKRA}"/>
      <stop offset="1" stop-color="{VERM_L}"/>
    </linearGradient>
    <linearGradient id="sealName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFDF6"/>
      <stop offset="0.55" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#B3A78E"/>
    </linearGradient>
    <linearGradient id="sealRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.22" stop-color="{VERM_L}" stop-opacity="0.8"/>
      <stop offset="0.5" stop-color="{CREAM}" stop-opacity="0.85"/>
      <stop offset="0.78" stop-color="{VERM_L}" stop-opacity="0.8"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sealSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM_L}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CREAM}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{VERM_L}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="sealGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.014" stroke-width="1"/>
    </pattern>
    <clipPath id="sealFrame">
      <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g clip-path="url(#sealFrame)">
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#sealSky)"/>
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#sealGrid)"/>
    <circle cx="{CX}" cy="{RING_CY}" r="310" fill="url(#sealGlow)" opacity="0.34"/>

    <!-- ══ the seal ═══════════════════════════════════════════════════ -->
    <g transform="translate({CX},{RING_CY})">
      <!-- turning ticks -->
      <g opacity="0.9">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="200s" repeatCount="indefinite"/>
        {ticks}
      </g>

      <!-- counter-turning outer marks -->
      <g opacity="0.5">
        <animateTransform attributeName="transform" type="rotate" from="360" to="0"
                          dur="140s" repeatCount="indefinite"/>
        <circle r="{RING_R + 58}" fill="none" stroke="{VERM}" stroke-opacity="0.16"
                stroke-width="0.7" stroke-dasharray="3 12"/>
      </g>

      <!-- ring -->
      <circle r="{RING_R}" fill="none" stroke="url(#sealRing)" stroke-width="2.2"/>
      <circle r="{RING_R - 8}" fill="none" stroke="{VERM}" stroke-opacity="0.22" stroke-width="0.8"/>
      <circle r="{RING_R + 3}" fill="none" stroke="{VERM_L}" stroke-opacity="0.14" stroke-width="9">
        <animate attributeName="stroke-opacity" values="0.10;0.24;0.10" dur="5.5s" repeatCount="indefinite"/>
      </circle>

      <!-- spiral, turning -->
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="80s" repeatCount="indefinite"/>
        <path d="{spiral_d(9, RING_R - 20, 2.6)}" fill="none" stroke="{VERM_L}"
              stroke-opacity="0.92" stroke-width="7.5" stroke-linecap="round"/>
        <path d="{spiral_d(9, RING_R - 20, 2.6)}" fill="none" stroke="{CREAM}"
              stroke-opacity="0.18" stroke-width="1.2" stroke-linecap="round"/>
      </g>

      <!-- core -->
      <circle r="7" fill="{CREAM}" fill-opacity="0.9">
        <animate attributeName="r" values="6;9;6" dur="3.8s" repeatCount="indefinite"/>
      </circle>
      <circle r="18" fill="{VERM_L}" fill-opacity="0.16"/>
    </g>

    <!-- ══ title ══════════════════════════════════════════════════════ -->
    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="74"
          letter-spacing="5" fill="url(#sealName)">ANUJ PHULERA</text>

    <rect x="{CX - 250}" y="{NAME_Y + 28}" width="500" height="1.3" fill="url(#sealRule)"/>

    <text x="{CX}" y="{NAME_Y + 62}" text-anchor="middle" font-family="{MONO}" font-size="15"
          letter-spacing="1.4" fill="{CREAM}" fill-opacity="0.92">I don't chase attention.</text>
    <text x="{CX}" y="{NAME_Y + 86}" text-anchor="middle" font-family="{MONO}" font-size="15"
          letter-spacing="1.4" fill="{VERM_L}">I build things that command it.</text>

    <!-- a light crossing the name -->
    <rect x="-230" y="{NAME_Y - 78}" width="230" height="106" fill="url(#sealSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1660 0;1660 0"
                        keyTimes="0;0.30;0.64;1" dur="14s" repeatCount="indefinite"/>
    </rect>

    <!-- ══ the eight ══════════════════════════════════════════════════ -->
    {chips}
    <text x="{CX}" y="{CHIP_Y + 48}" text-anchor="middle" font-family="{MONO}" font-size="8"
          letter-spacing="3.6" fill="{DIM}">EIGHT SEALS · ONE HAND</text>

    <!-- ══ eyebrow ════════════════════════════════════════════════════ -->
    <text x="{CX}" y="86" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{ASH}">CHAPTER 001</text>
    <text x="{CX}" y="106" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{VERM_L}" fill-opacity="0.75">THE SEAL</text>
  </g>

  <!-- ══ letterbox + HUD ═══════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.26"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.26"/>

  <text x="28" y="27" font-family="{MONO}" font-size="8.5" letter-spacing="3.6" fill="{ASH}">
    SEALING CORPS</text>
  <text x="{W - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{ASH}" fill-opacity="0.7">CHAPTER 001 · THE SEAL</text>

  <text x="28" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2" fill="{DIM}">
    GURUGRAM · HARYANA · INDIA</text>

  <text x="{CX}" y="{H - BAR + 28}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{DIM}" fill-opacity="0.8">
    GENIN · CLASS 10 · INTERFACE SYSTEMS</text>

  <circle cx="{W - 118}" cy="{H - BAR + 25}" r="3" fill="{VERM_L}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 106}" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5"
        letter-spacing="2.4" fill="{ASH}">REC</text>
  <text x="{W - 28}" y="{H - BAR + 28}" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="1.8" fill="{ASH}" fill-opacity="0.8">00:00:24</text>

  <g>{grain(W, H, 54)}</g>
  <g opacity="0.40">{scan(W, H)}</g>
</svg>
'''


if __name__ == "__main__":
    svg = build()
    (HERE / "opening.svg").write_text(svg, encoding="utf-8")
    print(f"wrote opening.svg  {len(svg):6d} b  {W}x{H}")
