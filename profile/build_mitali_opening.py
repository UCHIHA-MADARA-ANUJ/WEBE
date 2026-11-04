#!/usr/bin/env python3
"""Mitali Chincholikar — the opening.

Design rule, learned the hard way: FRAME ZERO IS THE POSTER.

Nothing is hidden behind an opacity-0 gate waiting for a clock to start. Every
element is fully painted at t=0, at full strength. The animation only adds
life on top of an already-finished composition:

    the moon drifts, the corona breathes, stars twinkle, a light crosses
    the name, the queue chips pulse in sequence, the eclipse turns.

If the SMIL clock never runs — phone, reduced motion, deferred decode,
GitHub's file viewer — the result is still the finished poster.

Run:  python3 build_mitali.py
      python3 build_mitali.py --poster   # writes the t=0 frame as a standalone PNG-source
"""
import math
import pathlib
import random

random.seed(41)
HERE = pathlib.Path(__file__).parent
OUT = HERE / "mitali"
OUT.mkdir(exist_ok=True)

# ── palette ─────────────────────────────────────────────────────────────────
INK      = "#05040A"
CHERRY   = "#D01731"
CHERRY_L = "#FF4D5E"
CORAL    = "#FF8A7A"
AQUA     = "#5FE3C0"
CELESTE  = "#A8DEF0"
ICE      = "#DCEFF6"
CREAM    = "#F4EEF2"
ASH      = "#9C93A6"
DIM      = "#5A5265"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Work Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"

W, H = 1200, 700
BAR = 44

CX = 600
EYE_CY = 276          # centre of the eclipse
EYE_R = 128
NAME_Y = 476
QUEUE_Y = 590


def grain(w, h, n=64):
    return "".join(
        f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.uniform(0.3, 0.95):.1f}" fill="#FFFFFF" fill-opacity="0.05">'
        f'<animate attributeName="fill-opacity" values="0.02;0.06;0.03;0.07;0.02" '
        f'dur="{random.uniform(1.0, 2.4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(n)
    )


def scan(w, h, step=3):
    return "".join(
        f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#000000" stroke-opacity="0.16" stroke-width="1"/>'
        for y in range(0, h, step)
    )


# ── corona rays, all painted at t=0 ─────────────────────────────────────────
rays = []
for i in range(96):
    ang = 2 * math.pi * i / 96 + random.uniform(-0.010, 0.010)
    r0 = EYE_R + 6
    r1 = EYE_R + random.uniform(20, 108)
    x1, y1 = CX + r0 * math.cos(ang), EYE_CY + r0 * math.sin(ang)
    x2, y2 = CX + r1 * math.cos(ang), EYE_CY + r1 * math.sin(ang)
    col = random.choice([CORAL, CHERRY_L, CORAL, CELESTE, AQUA, ICE])
    o = random.uniform(0.20, 0.70)
    sw = random.uniform(0.5, 1.8)
    d = random.uniform(2.8, 6.2)
    lo = o * random.uniform(0.35, 0.6)
    rays.append(
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
        f'stroke-opacity="{o:.2f}" stroke-width="{sw:.1f}" stroke-linecap="round">'
        f'<animate attributeName="stroke-opacity" values="{o:.2f};{lo:.2f};{o:.2f}" '
        f'dur="{d:.1f}s" begin="{random.uniform(0, 3):.1f}s" repeatCount="indefinite"/>'
        f'</line>'
    )
rays = "".join(rays)

# ── stars, painted, twinkling ───────────────────────────────────────────────
stars = []
for _ in range(70):
    sx = random.uniform(16, W - 16)
    sy = random.uniform(BAR + 8, H - BAR - 8)
    # keep them off the eclipse itself
    if math.hypot(sx - CX, sy - EYE_CY) < EYE_R + 120:
        continue
    o = random.uniform(0.12, 0.55)
    stars.append(
        f'<circle cx="{sx:.0f}" cy="{sy:.1f}" r="{random.uniform(0.4, 1.4):.1f}" '
        f'fill="{random.choice([ICE, CELESTE, CREAM])}" fill-opacity="{o:.2f}">'
        f'<animate attributeName="fill-opacity" values="{o:.2f};{o * 0.15:.2f};{o:.2f}" '
        f'dur="{random.uniform(2.0, 5.5):.1f}s" begin="{random.uniform(0, 4):.1f}s" '
        f'repeatCount="indefinite"/></circle>'
    )
stars = "".join(stars)

# ── the queue chips, all readable at t=0 ───────────────────────────────────
ITEMS = ["ADVANCED PYTHON", "C", "UI / UX", "SQL", "C++", "NODE.JS", "JAVA"]
CHIP_COLS = [AQUA, CELESTE, CORAL, AQUA, CELESTE, CORAL, AQUA]

chips = []
total_w = 7 * 138 + 6 * 10
x0 = CX - total_w / 2
for i, (label, col) in enumerate(zip(ITEMS, CHIP_COLS)):
    cx = x0 + i * 148
    chips.append(
        f'<g>'
        f'<rect x="{cx:.1f}" y="{QUEUE_Y}" width="138" height="30" rx="4" '
        f'fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.30"/>'
        f'<circle cx="{cx + 13:.1f}" cy="{QUEUE_Y + 15}" r="2.6" fill="{col}">'
        f'<animate attributeName="fill-opacity" values="0.25;1;0.25" dur="3.5s" '
        f'begin="{i * 0.35:.2f}s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx + 24:.1f}" y="{QUEUE_Y + 19}" font-family="{MONO}" font-size="8" '
        f'letter-spacing="1.1" fill="{CREAM}" fill-opacity="0.86">{label}</text>'
        f'<text x="{cx + 126:.1f}" y="{QUEUE_Y + 19}" text-anchor="end" font-family="{MONO}" '
        f'font-size="6.6" letter-spacing="1" fill="{DIM}">0{i + 1}</text>'
        f'</g>'
    )
chips = "".join(chips)


def build():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Mitali Chincholikar — the eclipse">
  <defs>
    <radialGradient id="mHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.24"/>
      <stop offset="0.34" stop-color="{CHERRY}" stop-opacity="0.10"/>
      <stop offset="0.68" stop-color="{CHERRY}" stop-opacity="0.03"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="mSky" cx="0.5" cy="0.42" r="0.62">
      <stop offset="0" stop-color="#170A15"/>
      <stop offset="0.55" stop-color="#0A0610"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <linearGradient id="mCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ICE}"/>
      <stop offset="0.22" stop-color="{CORAL}"/>
      <stop offset="0.44" stop-color="{CHERRY_L}"/>
      <stop offset="0.62" stop-color="{CORAL}"/>
      <stop offset="0.80" stop-color="{CELESTE}"/>
      <stop offset="1" stop-color="{ICE}"/>
    </linearGradient>
    <linearGradient id="mName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.52" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#AFA4B8"/>
    </linearGradient>
    <linearGradient id="mRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.2" stop-color="{CHERRY_L}" stop-opacity="0.7"/>
      <stop offset="0.5" stop-color="{ICE}" stop-opacity="0.9"/>
      <stop offset="0.8" stop-color="{CHERRY_L}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="mSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CORAL}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{ICE}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="mGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.013" stroke-width="1"/>
    </pattern>
    <clipPath id="mFrame">
      <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g clip-path="url(#mFrame)">
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#mSky)"/>
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#mGrid)"/>

    <!-- the light the mark throws -->
    <circle cx="{CX}" cy="{EYE_CY}" r="286" fill="url(#mHalo)" opacity="0.40"/>

    {stars}

    <!-- corona -->
    {rays}
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 24}" fill="none" stroke="{CORAL}"
            stroke-opacity="0.10" stroke-width="16"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 52}" fill="none" stroke="{CELESTE}"
            stroke-opacity="0.05" stroke-width="26"/>

    <!-- the sun's last light, then the disc that eats it -->
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="{CORAL}" fill-opacity="0.16"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="#030207"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="none" stroke="url(#mCorona)"
            stroke-width="3.2"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R - 4}" fill="none" stroke="{ICE}"
            stroke-opacity="0.55" stroke-width="0.9"/>

    <!-- the moon drifting across the rim -->
    <g transform="translate({CX},{EYE_CY})">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="-360"
                          dur="120s" repeatCount="indefinite"/>
        <circle cx="{EYE_R + 20}" r="11" fill="{ICE}" fill-opacity="0.28"/>
        <circle cx="{EYE_R + 20}" r="11" fill="none" stroke="{ICE}" stroke-opacity="0.45" stroke-width="0.8"/>
      </g>
    </g>

    <!-- concentric tracking rings -->
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 92}" fill="none" stroke="{CHERRY}"
            stroke-opacity="0.13" stroke-width="0.8" stroke-dasharray="2 9">
      <animateTransform attributeName="transform" type="rotate" from="0 {CX} {EYE_CY}"
                        to="360 {CX} {EYE_CY}" dur="220s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 122}" fill="none" stroke="{CELESTE}"
            stroke-opacity="0.07" stroke-width="0.7"/>

    <!-- title -->
    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="72"
          font-weight="300" letter-spacing="9" fill="url(#mName)">MITALI CHINCHOLIKAR</text>

    <rect x="{CX - 280}" y="{NAME_Y + 30}" width="560" height="1.3" fill="url(#mRule)"/>

    <text x="{CX}" y="{NAME_Y + 68}" text-anchor="middle" font-family="{SANS}" font-size="19"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.9">
      I don't wait to be senior to build.
    </text>

    <!-- a light crossing the name, forever -->
    <rect x="-210" y="{NAME_Y - 74}" width="200" height="104" fill="url(#mSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1640 0;1640 0"
                        keyTimes="0;0.28;0.62;1" dur="13s" repeatCount="indefinite"/>
    </rect>

    <!-- the queue, all seven, readable -->
    {chips}

    <text x="{CX}" y="{QUEUE_Y + 56}" text-anchor="middle" font-family="{MONO}" font-size="8.2"
          letter-spacing="3.6" fill="{DIM}">SEVEN ON THE QUEUE · NONE OF THEM LEARNED YET</text>
  </g>

  <!-- ══ letterbox + HUD ═══════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.28"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.28"/>

  <text x="28" y="27" font-family="{MONO}" font-size="8.5" letter-spacing="3.6" fill="{ASH}">
    MITALI CHINCHOLIKAR</text>
  <text x="{W - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{ASH}" fill-opacity="0.7">CHAPTER 001 · THE ECLIPSE</text>

  <text x="28" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2" fill="{DIM}">
    PUNE · MAHARASHTRA · INDIA</text>

  <text x="{CX}" y="{H - BAR + 28}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{DIM}" fill-opacity="0.8">CSE · FIRST YEAR · AI / ML FROM YEAR 2</text>

  <circle cx="{W - 118}" cy="{H - BAR + 25}" r="3" fill="{CHERRY_L}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 106}" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5"
        letter-spacing="2.4" fill="{ASH}">REC</text>
  <text x="{W - 28}" y="{H - BAR + 28}" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="1.8" fill="{ASH}" fill-opacity="0.8">00:00:18</text>

  <g>{grain(W, H, 58)}</g>
  <g opacity="0.40">{scan(W, H)}</g>
</svg>
'''


if __name__ == "__main__":
    svg = build()
    (OUT / "opening.svg").write_text(svg, encoding="utf-8")
    print(f"wrote mitali/opening.svg  {len(svg):6d} b  {W}x{H}")
