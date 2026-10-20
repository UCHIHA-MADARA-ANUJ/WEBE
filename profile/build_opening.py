#!/usr/bin/env python3
"""The opening title sequence.

A 12-second anime-style title card that loops: letterbox bars, a vermilion
slash, a masked title reveal, a seal ring drawing itself into existence,
and a chapter stamp.

Everything is SMIL, so it plays inside GitHub's <img> sandbox.

Run:  python3 build_opening.py          # writes opening.svg
      python3 build_opening.py --proof  # also writes a static proof frame
"""
import math
import pathlib
import random
import sys

random.seed(23)

HERE = pathlib.Path(__file__).parent

INK    = "#07060A"
CREAM  = "#F2E8D5"
ASH    = "#8A8090"
DIM    = "#4A4353"
VERM   = "#C1272D"
VERM_L = "#E8453F"
CHAKRA = "#4FB3D9"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

W, H = 1200, 560
BAR = 46                      # letterbox thickness
CYCLE = 12.0                  # seconds per loop

CX, CY = W / 2, 268
RING_R = 172


def kt(*seconds):
    """Seconds -> keyTime fractions for a 12s loop."""
    return ";".join(f"{max(0.0, min(1.0, s / CYCLE)):.4f}" for s in seconds)


def spiral_len(r0, r1, turns, steps=400):
    total = 0.0
    prev = None
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        p = (r * math.cos(th), r * math.sin(th))
        if prev:
            total += math.hypot(p[0] - prev[0], p[1] - prev[1])
        prev = p
    return total


def spiral_d(r0, r1, turns, steps=360):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        pts.append((r * math.cos(th), r * math.sin(th)))
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts)


CIRC = 2 * math.pi * RING_R
SPIRAL = spiral_len(26, 132, 2.5)
SPIRAL_D = spiral_d(26, 132, 2.5)

# film grain: static specks, briefly redistributed by opacity flicker
grain = []
for _ in range(90):
    grain.append(
        f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, H):.0f}" '
        f'r="{random.uniform(0.4, 1.1):.1f}" fill="#FFFFFF" '
        f'fill-opacity="{random.uniform(0.02, 0.07):.3f}">'
        f'<animate attributeName="fill-opacity" '
        f'values="0.02;0.06;0.03;0.07;0.02" dur="{random.uniform(0.7, 1.6):.1f}s" '
        f'repeatCount="indefinite"/></circle>'
    )

# scanlines
scan = "".join(
    f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#000000" stroke-opacity="0.18" stroke-width="1"/>'
    for y in range(0, H, 3)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — title sequence">
  <defs>
    <radialGradient id="opGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.30"/>
      <stop offset="0.55" stop-color="{VERM}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="opName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFDF6"/>
      <stop offset="0.62" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#B9A88E"/>
    </linearGradient>
    <linearGradient id="opRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{VERM_L}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="opReveal">
      <rect x="0" y="0" width="0" height="{H}">
        <animate attributeName="width" values="0;0;1180;1180;1180"
                 keyTimes="{kt(0, 0.9, 2.2, 11.2, 11.9)}" dur="{CYCLE}s" repeatCount="indefinite"/>
      </rect>
    </clipPath>
    <pattern id="opGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.016" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#opGrid)"/>
  <rect width="{W}" height="{H}" fill="url(#opGlow)"/>

  <!-- ── the seal ring, drawing itself ─────────────────────────────── -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0"
             keyTimes="{kt(0, 1.6, 2.4, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    <circle cx="{CX}" cy="{CY}" r="{RING_R}" fill="none" stroke="{VERM}" stroke-opacity="0.55"
            stroke-width="1.6" stroke-dasharray="{CIRC:.1f}" stroke-dashoffset="{CIRC:.1f}">
      <animate attributeName="stroke-dashoffset" values="{CIRC:.1f};{CIRC:.1f};0;0"
               keyTimes="{kt(0, 1.8, 4.6, 11.9)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{CX}" cy="{CY}" r="{RING_R * 0.80:.1f}" fill="none" stroke="{VERM}" stroke-opacity="0.20"
            stroke-width="0.8" stroke-dasharray="{2 * math.pi * RING_R * 0.80:.1f}"
            stroke-dashoffset="{2 * math.pi * RING_R * 0.80:.1f}">
      <animate attributeName="stroke-dashoffset"
               values="{2 * math.pi * RING_R * 0.80:.1f};{2 * math.pi * RING_R * 0.80:.1f};0;0"
               keyTimes="{kt(0, 2.3, 5.1, 11.9)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- ── the spiral, drawing itself, slow turn ─────────────────────── -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0"
             keyTimes="{kt(0, 3.0, 3.9, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    <g transform="translate({CX},{CY})">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0"
                          dur="70s" repeatCount="indefinite"/>
        <path d="{SPIRAL_D}" fill="none" stroke="{VERM_L}" stroke-opacity="0.85" stroke-width="6"
              stroke-linecap="round" stroke-dasharray="{SPIRAL:.1f}" stroke-dashoffset="{SPIRAL:.1f}">
          <animate attributeName="stroke-dashoffset" values="{SPIRAL:.1f};{SPIRAL:.1f};0;0"
                   keyTimes="{kt(0, 3.2, 5.4, 11.9)}" dur="{CYCLE}s" repeatCount="indefinite"/>
        </path>
      </g>
    </g>
  </g>

  <!-- ── vermilion slash ───────────────────────────────────────────── -->
  <rect x="{W / 2 - 300}" y="{CY - 1}" width="600" height="2" fill="{VERM_L}" opacity="0">
    <animate attributeName="opacity" values="0;0.95;0;0;0"
             keyTimes="{kt(0, 0.55, 0.75, 0.9, 11.9)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    <animate attributeName="width" values="0;600" keyTimes="0;1" dur="0.35s" repeatCount="indefinite"/>
  </rect>

  <!-- ── letterbox ─────────────────────────────────────────────────── -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.20"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.20"/>

  <!-- ── title block ───────────────────────────────────────────────── -->
  <g clip-path="url(#opReveal)">
    <text x="{CX}" y="{CY - 104}" text-anchor="middle" font-family="{MONO}" font-size="12"
          letter-spacing="7" fill="#B9AFC0">SEALING CORPS</text>

    <text x="{CX}" y="{CY + 108}" text-anchor="middle" font-family="{BLACK}" font-size="64"
          letter-spacing="2" fill="url(#opName)">ANUJ PHULERA</text>

    <rect x="{CX - 210}" y="{CY + 130}" width="420" height="1.6" fill="url(#opRule)" opacity="0">
      <animate attributeName="opacity" values="0;0;1;1;0"
               keyTimes="{kt(0, 2.2, 2.5, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
      <animate attributeName="width" values="0;420" keyTimes="0;1" dur="0.9s" begin="2.2s" repeatCount="indefinite"/>
    </rect>

    <text x="{CX}" y="{CY + 166}" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.2" fill="{CREAM}" opacity="0">
      I don't chase attention.
      <animate attributeName="opacity" values="0;0;0.95;0.95;0"
               keyTimes="{kt(0, 2.6, 3.1, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    </text>
    <text x="{CX}" y="{CY + 192}" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.2" fill="{VERM_L}" opacity="0">
      I build things that command it.
      <animate attributeName="opacity" values="0;0;1;1;0"
               keyTimes="{kt(0, 2.9, 3.4, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    </text>
  </g>

  <!-- ── chapter stamp ─────────────────────────────────────────────── -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0"
             keyTimes="{kt(0, 3.6, 4.1, 11.0, 11.8)}" dur="{CYCLE}s" repeatCount="indefinite"/>
    <rect x="48" y="{H - BAR - 54}" width="252" height="30" fill="none" stroke="{VERM}" stroke-opacity="0.45"/>
    <text x="64" y="{H - BAR - 34}" font-family="{MONO}" font-size="10" letter-spacing="2.6" fill="{VERM_L}">
      CHAPTER 001 · THE SEAL
    </text>
  </g>

  <!-- ── record indicator ──────────────────────────────────────────── -->
  <g>
    <circle cx="{W - 132}" cy="{H - BAR / 2}" r="3.4" fill="{VERM_L}">
      <animate attributeName="opacity" values="1;0.15;1" dur="1.4s" repeatCount="indefinite"/>
    </circle>
    <text x="{W - 120}" y="{H - BAR / 2 + 3.6}" font-family="{MONO}" font-size="9.5"
          letter-spacing="2.6" fill="{ASH}">REC</text>
    <text x="{W - 52}" y="{H - BAR / 2 + 3.6}" font-family="{MONO}" font-size="9.5"
          letter-spacing="2.2" fill="{DIM}" text-anchor="end">00:12:00</text>
  </g>

  <!-- ── grain + scanlines over everything ─────────────────────────── -->
  <g>{''.join(grain)}</g>
  <g opacity="0.5">{scan}</g>
</svg>
'''

if __name__ == "__main__":
    (HERE / "opening.svg").write_text(svg, encoding="utf-8")
    print(f"wrote opening.svg  {len(svg):6d} bytes  {W}x{H}")

    if "--proof" in sys.argv:
        # static frame with every reveal forced open, for offline proofing
        p = svg
        p = p.replace('opacity="0">\n    <animate', 'opacity="1">\n    <animate')
        p = p.replace('opacity="0">\n      <animate', 'opacity="1">\n      <animate')
        p = p.replace('fill="{VERM_L}" opacity="0">', 'fill="{VERM_L}" opacity="1">')
        p = p.replace('width="0" height="{H}"', f'width="1180" height="{H}"')
        p = p.replace(f'stroke-dashoffset="{CIRC:.1f}"', 'stroke-dashoffset="0"')
        p = p.replace(f'stroke-dashoffset="{SPIRAL:.1f}"', 'stroke-dashoffset="0"')
        p = p.replace('fill="{CREAM}" opacity="0"', 'fill="{CREAM}" opacity="1"')
        p = p.replace('fill="{VERM_L}" opacity="0"', 'fill="{VERM_L}" opacity="1"')
        p = p.replace('width="420" height="1.6" fill="url(#opRule)" opacity="0"',
                      'width="420" height="1.6" fill="url(#opRule)" opacity="1"')
        (HERE / "_opening_proof.svg").write_text(p, encoding="utf-8")
        print("wrote _opening_proof.svg")
