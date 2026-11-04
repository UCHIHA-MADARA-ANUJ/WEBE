#!/usr/bin/env python3
"""Mitali Chincholikar — profile kit.

Her mark is an eclipse: a dark disc crossing a bright one, and the light that
survives at the rim. The opening is a title sequence, not a title card —
totality, then the queue climbing, then the end card.

Everything is SMIL. No JavaScript, no external fonts, no services.

Run:  python3 build_mitali.py            # writes every SVG
      python3 build_mitali.py --proof=N  # static frame of scene N
"""
import math
import pathlib
import random
import sys

random.seed(41)
HERE = pathlib.Path(__file__).parent
OUT = HERE / "mitali"
OUT.mkdir(exist_ok=True)

# ── palette ─────────────────────────────────────────────────────────────────
INK      = "#05040A"
PAPER    = "#0B0A10"
CARD     = "#0F0D14"
CHERRY   = "#D01731"
CHERRY_L = "#FF4D5E"
CORAL    = "#FF8A7A"
AQUA     = "#5FE3C0"
CELESTE  = "#A8DEF0"
ICE      = "#DCEFF6"
CREAM    = "#F4EEF2"
ASH      = "#8B8391"
DIM      = "#4E4857"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Work Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"

W, H = 1200, 560
BAR = 44
CYCLE = 18.0

SUN_CX, SUN_CY, SUN_R = 600, 214, 148
NAME_Y = 438

_PROOF = next((a for a in sys.argv if a.startswith("--proof")), None)
PROOF = _PROOF is not None
SCENE = int(_PROOF.split("=")[1]) if _PROOF and "=" in _PROOF else 1


# ── timeline ────────────────────────────────────────────────────────────────
def track(attr, pairs, extra=""):
    ps = []
    for t, v in pairs:
        t = max(0.0, min(CYCLE, float(t)))
        if ps and abs(ps[-1][0] - t) < 1e-6:
            ps[-1] = (t, v)
        else:
            ps.append((t, v))
    if ps[0][0] > 0:
        ps.insert(0, (0.0, ps[0][1]))
    if ps[-1][0] < CYCLE:
        ps.append((CYCLE, ps[-1][1]))
    return (f'<animate attributeName="{attr}" '
            f'values="{";".join(str(v) for _, v in ps)}" '
            f'keyTimes="{";".join(f"{t / CYCLE:.5f}" for t, _ in ps)}" '
            f'dur="{CYCLE}s" repeatCount="indefinite"{extra}/>')


def tr(attr, pairs, extra=""):
    return "" if PROOF else track(attr, pairs, extra)


def op(pairs):
    return "1" if PROOF else str(pairs[0][1])


def show(t_in, t_out, fade=0.14):
    if t_in <= 0.0001:
        return [(0, 1), (t_out, 1), (t_out + fade, 0)] if t_out < CYCLE else [(0, 1)]
    if t_out >= CYCLE:
        return [(0, 0), (t_in - fade, 0), (t_in, 1)]
    return [(0, 0), (t_in - fade, 0), (t_in, 1), (t_out, 1), (t_out + fade, 0)]


def scene(n, pairs):
    if PROOF:
        return "1" if SCENE in (0, n) else "0"
    return str(pairs[0][1])


def kf(seconds):
    return f"{max(0.0, min(CYCLE, seconds)) / CYCLE:.5f}"


# ── furniture ───────────────────────────────────────────────────────────────
def grain(w, h, n=70):
    return "".join(
        f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.uniform(0.3, 0.95):.1f}" fill="#FFFFFF" fill-opacity="0.05">'
        f'<animate attributeName="fill-opacity" values="0.015;0.055;0.025;0.06;0.015" '
        f'dur="{random.uniform(1.0, 2.4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(n)
    )


def scan(w, h, step=3):
    return "".join(
        f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#000000" stroke-opacity="0.17" stroke-width="1"/>'
        for y in range(0, h, step)
    )


def grid_defs(pid="mGrid"):
    return (f'<pattern id="{pid}" width="48" height="48" patternUnits="userSpaceOnUse">'
            f'<path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.014" stroke-width="1"/></pattern>')


CORONA_GRAD = f'''<linearGradient id="mCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CORAL}"/>
      <stop offset="0.30" stop-color="{CHERRY_L}"/>
      <stop offset="0.58" stop-color="{CELESTE}"/>
      <stop offset="0.80" stop-color="{AQUA}"/>
      <stop offset="1" stop-color="{CORAL}"/>
    </linearGradient>'''

HALO_GRAD = f'''<radialGradient id="mHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.34"/>
      <stop offset="0.44" stop-color="{CHERRY}" stop-opacity="0.11"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>'''


def eclipse(cx, cy, r, ring_w=2.0, halo=True, spin=False):
    """The mark: dark disc, bright rim."""
    parts = []
    if halo:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.1f}" fill="url(#mHalo)"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#040308"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#mCorona)" '
                 f'stroke-width="{ring_w}" stroke-opacity="0.95"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r - ring_w * 0.9:.1f}" fill="none" '
                 f'stroke="{CORAL}" stroke-width="0.7" stroke-opacity="0.30"/>')
    return "".join(parts)


# ══════════════════════════════════════════════════════════════════════════
# 1. THE OPENING
# ══════════════════════════════════════════════════════════════════════════
def build_opening():
    # ── starfield ───────────────────────────────────────────────────────
    stars = []
    for _ in range(84):
        sx = random.uniform(20, W - 20)
        sy = random.uniform(BAR + 10, H - BAR - 10)
        sr = random.uniform(0.4, 1.5)
        d = random.uniform(1.6, 4.2)
        o = random.uniform(0.18, 0.75)
        stars.append(
            f'<circle cx="{sx:.0f}" cy="{sy:.1f}" r="{sr:.1f}" fill="{random.choice([ICE, CELESTE, CREAM])}" '
            f'fill-opacity="0">'
            f'<animate attributeName="fill-opacity" values="0;{o:.2f};{o * 0.35:.2f};{o:.2f};0" '
            f'keyTimes="0;{.30 + 0:.2f};0.45;0.78;1" dur="{d:.1f}s" repeatCount="indefinite"/></circle>'
        )
    stars = "".join(stars)

    # ── corona rays ─────────────────────────────────────────────────────
    rays = []
    for i in range(84):
        ang = 2 * math.pi * i / 84 + random.uniform(-0.012, 0.012)
        r0 = SUN_R + 5
        r1 = SUN_R + random.uniform(24, 104)
        x1, y1 = SUN_CX + r0 * math.cos(ang), SUN_CY + r0 * math.sin(ang)
        x2, y2 = SUN_CX + r1 * math.cos(ang), SUN_CY + r1 * math.sin(ang)
        rays.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{random.choice([CORAL, CHERRY_L, CELESTE, AQUA, ICE])}" '
            f'stroke-opacity="{random.uniform(0.22, 0.72):.2f}" '
            f'stroke-width="{random.uniform(0.5, 1.9):.1f}" stroke-linecap="round"/>'
        )
    rays = "".join(rays)

    # ── the queue staircase (scene II) ──────────────────────────────────
    items = ["ADVANCED PYTHON", "C", "UI / UX", "SQL", "C++", "NODE.JS", "JAVA"]
    xs = 152
    y_bot, y_top = 452, 186
    pts = [(xs + i * ((1052 - 152) / 6), y_bot - i * ((y_bot - y_top) / 6))
           for i in range(len(items))]

    path_d = [f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for i in range(1, len(pts)):
        px, py = pts[i - 1]
        cx2, cy2 = pts[i]
        path_d.append(f"L {cx2:.1f},{py:.1f} L {cx2:.1f},{cy2:.1f}")
    path_d = " ".join(path_d)
    path_len = (pts[-1][0] - pts[0][0]) + (pts[0][1] - pts[-1][1])

    nodes = []
    for i, ((nx, ny), label) in enumerate(zip(pts, items)):
        t0 = 9.0 + i * 0.34
        ly = ny - 20
        col = [AQUA, CELESTE, CORAL][i % 3]
        nodes.append(
            f'<g opacity="{op([(0, 0)])}">' + tr("opacity", show(t0, 13.2, 0.16))
            + f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="11" fill="none" stroke="{col}" stroke-opacity="0.30">'
              f'<animate attributeName="r" values="9;15;9" dur="3.2s" begin="{i * 0.18:.2f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="stroke-opacity" values="0.34;0.05;0.34" dur="3.2s" '
              f'begin="{i * 0.18:.2f}s" repeatCount="indefinite"/></circle>'
            + f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4" fill="{col}"/>'
            + f'<text x="{nx:.1f}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="9" '
              f'letter-spacing="1.8" fill="{CREAM}" fill-opacity="0.9">{label}</text>'
            + f'<text x="{nx:.1f}" y="{ny + 26}" text-anchor="middle" '
              f'font-family="{MONO}" font-size="7" letter-spacing="1.6" fill="{DIM}">0{i + 1}</text>'
            + '</g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Mitali Chincholikar — the eclipse">
  <defs>
    {HALO_GRAD}
    {CORONA_GRAD}
    <radialGradient id="mSun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFE9DC"/>
      <stop offset="0.55" stop-color="{CORAL}"/>
      <stop offset="0.85" stop-color="{CHERRY_L}"/>
      <stop offset="1" stop-color="{CHERRY}"/>
    </radialGradient>
    <radialGradient id="mBigGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY_L}" stop-opacity="0.42"/>
      <stop offset="0.35" stop-color="{CHERRY}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="mName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#B6ABBE"/>
    </linearGradient>
    <linearGradient id="mRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CHERRY_L}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="mSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.45" stop-color="{CORAL}" stop-opacity="0.95"/>
      <stop offset="0.6" stop-color="{ICE}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="mStep" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{AQUA}" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="{CELESTE}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{CORAL}" stop-opacity="0.95"/>
    </linearGradient>
    {grid_defs()}
    <clipPath id="mWipe">
      <rect x="0" y="0" width="{'1240' if PROOF else '0'}" height="{H}">
        {tr("width", [(0, 0), (3.30, 0), (4.30, 1240), (17.0, 1240)])}
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#mGrid)"/>

  <!-- poster frame: a frozen render is still a finished composition -->
  <g opacity="{("0.20" if (not PROOF or SCENE == 0) else "0")}">
    {tr("opacity", [(0, 0.20), (0.95, 0.20), (1.55, 0)])}
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R}" fill="none" stroke="{CHERRY_L}" stroke-width="2"/>
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 10}" fill="none" stroke="{CHERRY}" stroke-opacity="0.4" stroke-width="0.8"/>
    <text x="{SUN_CX}" y="{SUN_CY - 186}" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="6.6" fill="{ASH}">PUNE · MAHARASHTRA · INDIA</text>
    <text x="{SUN_CX}" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="66"
          font-weight="300" letter-spacing="8" fill="{CREAM}">MITALI CHINCHOLIKAR</text>
    <rect x="330" y="{NAME_Y + 22}" width="540" height="1.2" fill="{CHERRY_L}" fill-opacity="0.6"/>
    <text x="{SUN_CX}" y="{NAME_Y + 54}" text-anchor="middle" font-family="{SANS}" font-size="18"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.66">
      I don't wait to be senior to build.
    </text>
  </g>

  <!-- ══ SCENE I · TOTALITY ═════════════════════════════════════════════ -->
  <g opacity="{scene(1, show(0.05, 8.10))}">
    {tr("opacity", show(0.05, 8.10))}

    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="330" fill="url(#mBigGlow)" opacity="0.34"/>

    <g opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (3.0, 0), (3.5, 1), (7.6, 1), (8.1, 0)])}
      {stars}
    </g>

    <!-- the sun -->
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R}" fill="url(#mSun)" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (0.35, 0), (1.35, 1), (18, 1)])}
    </circle>
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 2}" fill="none" stroke="{ICE}"
            stroke-opacity="0.55" stroke-width="1.4" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (0.5, 0), (1.6, 0.55), (3.0, 0.9), (3.2, 0), (7.9, 0)])}
    </circle>

    <!-- corona, only during totality -->
    <g opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (2.85, 0), (3.35, 1), (6.35, 1), (6.95, 0)])}
      {rays}
      <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 4}" fill="none" stroke="url(#mCorona)"
              stroke-width="3" stroke-opacity="0.9"/>
      <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 30}" fill="none" stroke="{CORAL}"
              stroke-opacity="0.12" stroke-width="10"/>
      <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 62}" fill="none" stroke="{CELESTE}"
              stroke-opacity="0.06" stroke-width="18"/>
    </g>

    <!-- the moon -->
    <g transform="translate({SUN_CX},{SUN_CY})">
      <g>
        <animateTransform attributeName="transform" type="translate"
                          values="-880 0;-880 0;-0.5 0;-0.5 0;880 0;880 0"
                          keyTimes="0;{kf(1.15)};{kf(3.05)};{kf(6.55)};{kf(8.05)};1"
                          dur="{CYCLE}s" repeatCount="indefinite"/>
        <circle r="{SUN_R + 2}" fill="#040308"/>
        <circle r="{SUN_R + 2}" fill="none" stroke="{CHERRY}" stroke-opacity="0.30" stroke-width="0.8"/>
        <circle r="{SUN_R + 2}" fill="none" stroke="{CHERRY_L}" stroke-opacity="0.12" stroke-width="5"/>
      </g>
    </g>

    <!-- diamond ring, at both contacts -->
    <g opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (2.86, 0), (3.00, 1), (3.24, 0),
                      (6.42, 0), (6.56, 0.9), (6.80, 0)])}
      <circle cx="{SUN_CX - SUN_R}" cy="{SUN_CY}" r="7" fill="{ICE}"/>
      <circle cx="{SUN_CX - SUN_R}" cy="{SUN_CY}" r="22" fill="{CORAL}" fill-opacity="0.25"/>
      <line x1="{SUN_CX - SUN_R - 70}" y1="{SUN_CY}" x2="{SUN_CX - SUN_R - 14}" y2="{SUN_CY}"
            stroke="{ICE}" stroke-width="1.4" stroke-opacity="0.8"/>
      <line x1="{SUN_CX - SUN_R + 14}" y1="{SUN_CY}" x2="{SUN_CX - SUN_R + 70}" y2="{SUN_CY}"
            stroke="{ICE}" stroke-width="1.4" stroke-opacity="0.8"/>
    </g>

    <!-- name -->
    <g clip-path="url(#mWipe)">
      <text x="{SUN_CX}" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="66"
            font-weight="300" letter-spacing="8" fill="url(#mName)">MITALI CHINCHOLIKAR</text>
    </g>

    <text x="{SUN_CX}" y="{SUN_CY - 186}" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="6.6" fill="{ASH}" opacity="{op(show(3.9, 7.9, 0.3))}">
      {tr("opacity", show(3.9, 7.9, 0.3))}PUNE · MAHARASHTRA · INDIA
    </text>

    <rect x="330" y="{NAME_Y + 24}" width="{'540' if PROOF else '0'}" height="1.2"
          fill="url(#mRule)" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (4.30, 0), (4.40, 1), (7.2, 1), (7.7, 0)])}
      {tr("width", [(0, 0), (4.30, 0), (5.35, 540), (18, 540)])}
    </rect>

    <text x="{SUN_CX}" y="{NAME_Y + 54}" text-anchor="middle" font-family="{SANS}" font-size="18"
          font-style="italic" font-weight="300" fill="{CREAM}" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (4.65, 0), (5.15, 0.98), (7.2, 0.98), (7.65, 0)])}
      I don't wait to be senior to build.
    </text>

    <!-- the light crossing the title -->
    <rect x="-160" y="{NAME_Y - 70}" width="150" height="92" fill="url(#mSweep)" opacity="0">
      {tr("opacity", [(0, 0), (6.60, 0), (6.70, 0.55), (7.05, 0.4), (7.25, 0)])}
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1520 0;1520 0"
                        keyTimes="0;{kf(6.60)};{kf(7.25)};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- ══ SCENE II · THE CLIMB ═══════════════════════════════════════════ -->
  <g opacity="{scene(2, show(8.30, 13.55))}">
    {tr("opacity", show(8.30, 13.55))}

    <circle cx="600" cy="286" r="300" fill="url(#mBigGlow)" opacity="0.16"/>
    <g opacity="0.5">
      <circle cx="600" cy="286" r="128" fill="#040308"/>
      <circle cx="600" cy="286" r="128" fill="none" stroke="url(#mCorona)" stroke-width="2.2" stroke-opacity="0.8"/>
      <circle cx="600" cy="286" r="128" fill="none" stroke="{CORAL}" stroke-width="9" stroke-opacity="0.10"/>
    </g>

    <text x="152" y="112" font-family="{MONO}" font-size="9" letter-spacing="5.4" fill="{ASH}">
      THE QUEUE · IN ORDER
    </text>
    <text x="1052" y="112" text-anchor="end" font-family="{MONO}" font-size="8.4" letter-spacing="2.6"
          fill="{DIM}">SEVEN THINGS I CANNOT DO YET</text>
    <line x1="152" y1="126" x2="1052" y2="126" stroke="{CHERRY}" stroke-opacity="0.18"/>

    <path d="{path_d}" fill="none" stroke="url(#mStep)" stroke-width="2" stroke-linejoin="round"
          stroke-dasharray="{path_len:.1f}" stroke-dashoffset="{'0' if PROOF else f'{path_len:.1f}'}">
      {tr("stroke-dashoffset", [(0, path_len), (8.85, path_len), (10.35, 0), (18, 0)])}
      {tr("opacity", [(0, 0), (8.55, 0), (8.85, 0.9), (13.1, 0.9), (13.55, 0)])}
    </path>

    <path d="{path_d}" fill="none" stroke="{CORAL}" stroke-width="7" stroke-linejoin="round"
          stroke-opacity="0.10" stroke-dasharray="{path_len:.1f}"
          stroke-dashoffset="{'0' if PROOF else f'{path_len:.1f}'}">
      {tr("stroke-dashoffset", [(0, path_len), (8.85, path_len), (10.35, 0), (18, 0)])}
    </path>

    {''.join(nodes)}

    <text x="{SUN_CX}" y="504" text-anchor="middle" font-family="{MONO}" font-size="8.4"
          letter-spacing="3.4" fill="{ASH}" fill-opacity="0.6" opacity="{op(show(10.6, 13.3, 0.3))}">
      {tr("opacity", show(10.6, 13.3, 0.3))}TOUCHED SO FAR · PYTHON · C · HTML · CSS · JS
    </text>
  </g>

  <!-- ══ SCENE III · THE ECLIPSE ════════════════════════════════════════ -->
  <g opacity="{scene(3, show(13.75, 17.35))}">
    {tr("opacity", show(13.75, 17.35))}

    <circle cx="{SUN_CX}" cy="196" r="200" fill="url(#mBigGlow)" opacity="0.28"/>

    <g transform="translate({SUN_CX},196)">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="40s" repeatCount="indefinite"/>
        <circle r="74" fill="#040308"/>
        <circle r="74" fill="none" stroke="url(#mCorona)" stroke-width="2.2" stroke-opacity="0.95"/>
        <circle r="86" fill="none" stroke="{CORAL}" stroke-width="0.7" stroke-opacity="0.25"/>
      </g>
    </g>
    <circle cx="{SUN_CX}" cy="196" r="120" fill="none" stroke="{CHERRY}" stroke-opacity="0.14" stroke-width="0.8"/>

    <text x="{SUN_CX}" y="318" text-anchor="middle" font-family="{MONO}" font-size="9"
          letter-spacing="6" fill="{ASH}">CHAPTER 001</text>

    <text x="{SUN_CX}" y="382" text-anchor="middle" font-family="{SANS}" font-size="52"
          font-weight="300" letter-spacing="8" fill="url(#mName)">THE ECLIPSE</text>

    <rect x="404" y="404" width="392" height="1.2" fill="url(#mRule)" opacity="0.9"/>

    <text x="{SUN_CX}" y="440" text-anchor="middle" font-family="{SANS}" font-size="17"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.9">
      Here to turn ambition into reality.
    </text>

    <text x="{SUN_CX}" y="468" text-anchor="middle" font-family="{MONO}" font-size="8.4"
          letter-spacing="3.4" fill="{DIM}">PUNE · MAHARASHTRA · INDIA</text>
  </g>

  <!-- ══ scene sweep ════════════════════════════════════════════════════ -->
  <g opacity="0">
    {tr("opacity", [(0, 0), (8.10, 0), (8.17, 1), (8.62, 1), (8.69, 0),
                    (13.45, 0), (13.52, 1), (13.97, 1), (14.04, 0)])}
    <rect x="-40" y="0" width="24" height="{H}" fill="url(#mSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="-120 0;-120 0;1240 0;1240 0;1240 0;1240 0"
                        keyTimes="0;{kf(8.10)};{kf(8.64)};{kf(13.45)};{kf(13.99)};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- ══ letterbox + HUD ════════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.22"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.22"/>

  <text x="28" y="27" font-family="{MONO}" font-size="8.5" letter-spacing="3.6" fill="{ASH}">MITALI CHINCHOLIKAR</text>
  <text x="1172" y="27" text-anchor="end" font-family="{MONO}" font-size="8.5" letter-spacing="3.2"
        fill="{ASH}" fill-opacity="0.7">CHAPTER 001 · THE ECLIPSE</text>

  <text x="28" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2"
        fill="{DIM}">PUNE · MAHARASHTRA · INDIA</text>

  <circle cx="{W - 150}" cy="{H - BAR + 25}" r="3" fill="{CHERRY_L}">
    <animate attributeName="opacity" values="1;0.12;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 138}" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="2.4" fill="{ASH}">REC</text>
  <text x="1172" y="{H - BAR + 28}" text-anchor="end" font-family="{MONO}" font-size="9"
        letter-spacing="1.6" fill="{ASH}">00:00:18</text>

  <rect x="0" y="{H - 3}" width="{'1200' if PROOF else '0'}" height="3" fill="url(#mRule)">
    {tr("width", [(0, 0), (CYCLE, 1200)])}
  </rect>

  <g>{grain(W, H, 66)}</g>
  <g opacity="0.42">{scan(W, H)}</g>

  <circle cx="{SUN_CX}" cy="280" r="0" fill="#000000">
    {tr("r", [(0, 0), (17.25, 0), (17.9, 800), (18, 800)])}
  </circle>
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
# 2. THE RECORD
# ══════════════════════════════════════════════════════════════════════════
def build_record():
    W2, H2 = 1000, 306
    rows = [
        ("PROGRAM", "CSE · YEAR 1"),
        ("NEXT TRACK", "AI / ML · FROM YEAR 2"),
        ("FOCUS", "WEB &amp; APP"),
        ("BUILDING", "TWO SITES, ONE COLLEGE PROJECT"),
        ("ORIGIN", "PUNE, MAHARASHTRA"),
        ("STATUS", "LEARNING IN PUBLIC"),
    ]
    body = []
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 33
        body.append(
            f'<text x="392" y="{y}" font-family="{MONO}" font-size="8.2" letter-spacing="3" '
            f'fill="{DIM}">{k}</text>'
            f'<text x="552" y="{y}" font-family="{MONO}" font-size="10.6" letter-spacing="1.6" '
            f'fill="{CREAM}" fill-opacity="0.92">{v}</text>'
            f'<line x1="380" y1="{y + 12}" x2="966" y2="{y + 12}" stroke="#FFFFFF" stroke-opacity="0.05"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="Mitali Chincholikar — the record">
  <defs>
    {grid_defs("rGrid")}
    {HALO_GRAD}
    {CORONA_GRAD}
    <radialGradient id="rGlow" cx="0.5" cy="0" r="1">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W2}" height="{H2}" fill="{INK}"/>
  <rect width="{W2}" height="{H2}" fill="url(#rGrid)"/>
  <rect width="{W2}" height="{H2}" fill="url(#rGlow)"/>

  <rect x="10" y="10" width="{W2 - 20}" height="{H2 - 20}" rx="7" fill="{PAPER}"
        stroke="#FFFFFF" stroke-opacity="0.07"/>
  <rect x="10" y="10" width="{W2 - 20}" height="2" rx="1" fill="{CHERRY}" fill-opacity="0.55"/>

  <text x="36" y="45" font-family="{MONO}" font-size="8.4" letter-spacing="4" fill="{ASH}">THE RECORD</text>
  <text x="{W2 - 36}" y="45" text-anchor="end" font-family="{MONO}" font-size="8.4"
        letter-spacing="3" fill="{DIM}">NO. 001</text>
  <line x1="36" y1="58" x2="{W2 - 36}" y2="58" stroke="{CHERRY}" stroke-opacity="0.22"/>

  <rect x="36" y="78" width="176" height="196" rx="5" fill="#08070D" stroke="#FFFFFF" stroke-opacity="0.06"/>
  {eclipse(124, 160, 46, 1.6)}
  <text x="124" y="248" text-anchor="middle" font-family="{MONO}" font-size="7.4"
        letter-spacing="2.6" fill="{DIM}">THE ECLIPSE</text>

  {''.join(body)}

  <text x="36" y="{H2 - 18}" font-family="{MONO}" font-size="7.4" letter-spacing="2.4" fill="{DIM}">
    DNYAN PRASAD GLOBAL UNIVERSITY · SCHOOL OF TECHNOLOGY AND RESEARCH
  </text>
  <circle cx="{W2 - 46}" cy="{H2 - 22}" r="2.8" fill="{AQUA}">
    <animate attributeName="opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
# 3. THE BENCH
# ══════════════════════════════════════════════════════════════════════════
def build_bench():
    W2, H2 = 1200, 372
    CWv, CHv = 574, 292

    def card(x, idx, name, tag, tag_c, line, status, art):
        return f'''
  <g>
    <rect x="{x}" y="10" width="{CWv}" height="{CHv}" rx="7" fill="{CARD}" stroke="#FFFFFF" stroke-opacity="0.07"/>
    <rect x="{x}" y="10" width="70" height="2" rx="1" fill="{tag_c}" fill-opacity="0.9">
      <animateTransform attributeName="transform" type="translate" values="-70 0;{CWv + 20} 0"
                        dur="5.2s" begin="{idx * 1.6}s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" values="0;0.6;0.25;0.5;0" dur="5.2s"
               begin="{idx * 1.6}s" repeatCount="indefinite"/>
    </rect>

    <text x="{x + CWv - 24}" y="72" text-anchor="end" font-family="{MONO}" font-size="52"
          fill="#FFFFFF" fill-opacity="0.035">{idx + 1:02d}</text>

    <text x="{x + 26}" y="42" font-family="{MONO}" font-size="8.2" letter-spacing="3"
          fill="{tag_c}" fill-opacity="0.85">{tag}</text>
    <text x="{x + 26}" y="82" font-family="{SANS}" font-size="27" font-weight="300"
          letter-spacing="3" fill="{CREAM}">{name}</text>
    <text x="{x + 26}" y="106" font-family="{SANS}" font-size="13.5" font-style="italic"
          font-weight="300" fill="{ASH}">{line}</text>

    <rect x="{x + 26}" y="132" width="{CWv - 52}" height="118" rx="4" fill="#08070D"
          stroke="#FFFFFF" stroke-opacity="0.05"/>
    {art(x + 26, 132, CWv - 52, 118, tag_c)}

    <line x1="{x + 26}" y1="{CHv - 42}" x2="{x + CWv - 26}" y2="{CHv - 42}"
          stroke="#FFFFFF" stroke-opacity="0.06"/>
    <text x="{x + 26}" y="{CHv - 20}" font-family="{MONO}" font-size="7.8" letter-spacing="2.2"
          fill="{tag_c}" fill-opacity="0.8">{status}</text>
  </g>'''

    def art_meditrace(x, y, w, h, a):
        g = [f'<text x="{x + 14}" y="{y + 22}" font-family="{MONO}" font-size="7.4" '
             f'letter-spacing="2.4" fill="{DIM}">NOT BUILT</text>']
        pts = []
        for k in range(49):
            t = k / 48
            yy = y + h * 0.58 - math.sin(t * 17) * h * 0.12 - (math.sin(t * 41) * h * 0.05)
            pts.append((x + 16 + t * (w - 32), yy))
        g.append('<path d="M ' + " L ".join("%.1f,%.1f" % p for p in pts) +
                 f'" fill="none" stroke="{a}" stroke-width="1.5" stroke-opacity="0.8" stroke-linecap="round"/>')
        for k in range(8):
            cx = x + 30 + k * (w - 60) / 7
            g.append(f'<circle cx="{cx:.0f}" cy="{y + h * 0.82}" r="1.8" fill="{a}" fill-opacity="0.35"/>')
        g.append(f'<line x1="{x + 16}" y1="{y + h * 0.82}" x2="{x + w - 16}" y2="{y + h * 0.82}" '
                 f'stroke="{a}" stroke-opacity="0.12"/>')
        return "".join(g)

    def art_askx(x, y, w, h, a):
        g = [f'<text x="{x + 14}" y="{y + 22}" font-family="{MONO}" font-size="7.4" '
             f'letter-spacing="2.4" fill="{DIM}">COLLEGE PROJECT</text>']
        g.append(f'<rect x="{x + 16}" y="{y + 32}" width="{w - 32}" height="20" rx="10" '
                 f'fill="{a}" fill-opacity="0.09" stroke="{a}" stroke-opacity="0.32"/>')
        g.append(f'<circle cx="{x + 32}" cy="{y + 42}" r="3.2" fill="none" stroke="{a}" stroke-opacity="0.7"/>')
        g.append(f'<line x1="{x + 34.5}" y1="{y + 44.5}" x2="{x + 38}" y2="{y + 48}" '
                 f'stroke="{a}" stroke-opacity="0.7"/>')
        g.append(f'<rect x="{x + 48}" y="{y + 38.5}" width="{w * 0.34:.0f}" height="6" rx="3" fill="{a}" fill-opacity="0.28"/>')
        for k in range(3):
            yy = y + 66 + k * 17
            g.append(f'<rect x="{x + 16}" y="{yy}" width="{w - 32}" height="12" rx="2.5" '
                     f'fill="{a}" fill-opacity="0.06" stroke="{a}" stroke-opacity="0.14"/>')
            g.append(f'<rect x="{x + 24}" y="{yy + 4.5}" width="{(w - 48) * (0.5 - k * 0.11):.0f}" '
                     f'height="3" rx="1.5" fill="{a}" fill-opacity="0.4"/>')
        return "".join(g)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="The bench: Meditrace and AskX">
  <defs>
    {grid_defs("bGrid")}
    <radialGradient id="bGlow" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.11"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W2}" height="{H2}" fill="{INK}"/>
  <rect width="{W2}" height="{H2}" fill="url(#bGrid)"/>
  <rect width="{W2}" height="{H2}" fill="url(#bGlow)"/>
  {card(10, 0, "MEDITRACE", "ON THE BENCH · NOT BUILT", AQUA,
        "the one she wants to be big enough to matter", "STATUS · DESIGNED, NOT WRITTEN", art_meditrace)}
  {card(616, 1, "ASKX", "BUILT · CORRECTIONS PENDING", CORAL,
        "a college project, built for students", "STATUS · LIVE, ROUGH", art_askx)}
  <text x="{W2 / 2}" y="{H2 - 5}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.4" fill="{ASH}" fill-opacity="0.6">TWO ON THE BENCH · NONE PADDING THE GRID</text>
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
# 4. THE QUEUE PANEL — same staircase, standing still
# ══════════════════════════════════════════════════════════════════════════
def build_queue():
    W2, H2 = 1000, 430
    items = ["ADVANCED PYTHON", "C", "UI / UX", "SQL", "C++", "NODE.JS", "JAVA"]
    xs, ys = 96, 900
    y_bot, y_top = 300, 118
    pts = [(xs + i * ((xs2 := (900 - 96) / 6)), y_bot - i * ((y_bot - y_top) / 6))
           for i in range(len(items))]

    d = [f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for i in range(1, len(pts)):
        px, py = pts[i - 1]
        cx2, cy2 = pts[i]
        d.append(f"L {cx2:.1f},{py:.1f} L {cx2:.1f},{cy2:.1f}")
    d = " ".join(d)
    ln = (pts[-1][0] - pts[0][0]) + (pts[0][1] - pts[-1][1])

    nodes = []
    for i, ((nx, ny), label) in enumerate(zip(pts, items)):
        col = [AQUA, CELESTE, CORAL][i % 3]
        up = i % 2 == 0
        ly = ny - 16 if up else ny + 24
        nodes.append(
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="10" fill="none" stroke="{col}" stroke-opacity="0.28">'
            f'<animate attributeName="r" values="9;14;9" dur="3.4s" begin="{i * 0.16:.2f}s" repeatCount="indefinite"/>'
            f'</circle>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="3.6" fill="{col}"/>'
            f'<text x="{nx:.1f}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="8.2" '
            f'letter-spacing="1.5" fill="{CREAM}" fill-opacity="0.88">{label}</text>'
            f'<text x="{nx:.1f}" y="{ny + (40 if up else 44)}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="6.8" letter-spacing="1.4" fill="{DIM}">0{i + 1}</text>'
        )

    also = ["SECURITY", "DESIGN", "STOCK MARKETS"]
    chips = "".join(
        f'<rect x="{196 + i * 168}" y="368" width="152" height="26" rx="13" fill="{CORAL}" '
        f'fill-opacity="0.07" stroke="{CORAL}" stroke-opacity="0.28"/>'
        f'<text x="{272 + i * 168}" y="385" text-anchor="middle" font-family="{MONO}" font-size="8.4" '
        f'letter-spacing="2.2" fill="{CORAL}" fill-opacity="0.85">{t}</text>'
        for i, t in enumerate(also)
    )
    dots = "".join(
        f'<circle cx="{232 + i * 26}" cy="66" r="3" fill="{AQUA}" fill-opacity="0.85">'
        f'<animate attributeName="opacity" values="0.9;0.25;0.9" dur="2.6s" begin="{i * 0.22:.1f}s" '
        f'repeatCount="indefinite"/></circle>'
        for i in range(5)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="Learning queue">
  <defs>
    {grid_defs("qGrid")}
    <radialGradient id="qGlow" cx="0.5" cy="0" r="1">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="qStep" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{AQUA}"/>
      <stop offset="0.5" stop-color="{CELESTE}"/>
      <stop offset="1" stop-color="{CORAL}"/>
    </linearGradient>
  </defs>
  <rect width="{W2}" height="{H2}" fill="{INK}"/>
  <rect width="{W2}" height="{H2}" fill="url(#qGrid)"/>
  <rect width="{W2}" height="{H2}" fill="url(#qGlow)"/>

  <rect x="10" y="10" width="{W2 - 20}" height="{H2 - 20}" rx="7" fill="{PAPER}"
        stroke="#FFFFFF" stroke-opacity="0.07"/>
  <rect x="10" y="10" width="{W2 - 20}" height="2" rx="1" fill="{AQUA}" fill-opacity="0.45"/>

  <text x="36" y="44" font-family="{MONO}" font-size="8.4" letter-spacing="4" fill="{ASH}">LEARNING QUEUE</text>
  <text x="{W2 - 36}" y="44" text-anchor="end" font-family="{MONO}" font-size="8.2" letter-spacing="2.4"
        fill="{DIM}">SEVEN THINGS I CANNOT DO YET</text>
  <line x1="36" y1="56" x2="{W2 - 36}" y2="56" stroke="#FFFFFF" stroke-opacity="0.07"/>

  <text x="36" y="70" font-family="{MONO}" font-size="7.6" letter-spacing="2.6" fill="{DIM}">TOUCHED</text>
  <text x="196" y="70" font-family="{MONO}" font-size="9.2" letter-spacing="2.2" fill="{CREAM}"
        fill-opacity="0.8">PYTHON · C · HTML · CSS · JS</text>
  {dots}

  <path d="{d}" fill="none" stroke="{CORAL}" stroke-width="8" stroke-linejoin="round"
        stroke-opacity="0.08"/>
  <path d="{d}" fill="none" stroke="url(#qStep)" stroke-width="2" stroke-linejoin="round"/>
  {''.join(nodes)}

  <line x1="36" y1="352" x2="{W2 - 36}" y2="352" stroke="{CHERRY}" stroke-opacity="0.16"/>
  <text x="36" y="385" font-family="{MONO}" font-size="7.8" letter-spacing="2.6" fill="{DIM}">ALSO · NOT CODE</text>
  {chips}
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
# 5. CREDITS
# ══════════════════════════════════════════════════════════════════════════
def build_credits():
    W2, H2, TRAVEL = 1200, 320, 58
    sections = [
        ("STARRING", ["MITALI CHINCHOLIKAR"]),
        ("ORIGIN", ["PUNE · MAHARASHTRA · INDIA"]),
        ("PROGRAM", ["CSE · FIRST YEAR", "AI / ML TRACK FROM YEAR 2"]),
        ("BELONGS TO", ["SWARANG CULTURAL CLUB · EVENT MANAGER",
                        "BADMINTON · TUG OF WAR"]),
        ("TOUCHED", ["PYTHON · C · HTML · CSS · JS"]),
        ("BUILT", ["TWO SITES", "ONE COLLEGE PROJECT"]),
        ("ON THE BENCH", ["MEDITRACE"]),
        ("MARK", ["THE ECLIPSE"]),
    ]
    body, y = [], 0.0
    for label, lines in sections:
        y += 32
        body.append(f'<text x="{W2 / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
                    f'font-size="8.6" letter-spacing="5.4" fill="{DIM}">{label}</text>')
        for line in lines:
            y += 22
            body.append(f'<text x="{W2 / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
                        f'font-size="12" letter-spacing="1.6" fill="{CREAM}" fill-opacity="0.88">{line}</text>')
        y += 18

    y += 26
    body.append(f'<line x1="{W2 / 2 - 70}" y1="{y:.1f}" x2="{W2 / 2 + 70}" y2="{y:.1f}" '
                f'stroke="{CHERRY}" stroke-opacity="0.5"/>')
    y += 24
    body.append(f'<text x="{W2 / 2}" y="{y:.1f}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="8.2" letter-spacing="3.4" fill="{ASH}">NONE OF THIS IS FINISHED</text>')

    total = y + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="End credits">
  <defs>
    <linearGradient id="cTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}" stop-opacity="1"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="cBot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity="1"/>
    </linearGradient>
    {grid_defs("cGrid")}
  </defs>
  <rect width="{W2}" height="{H2}" fill="{INK}"/>
  <rect width="{W2}" height="{H2}" fill="url(#cGrid)"/>

  <g>
    <animateTransform attributeName="transform" type="translate" values="0 {H2 + 20};0 {-total:.1f}"
                      dur="{TRAVEL}s" repeatCount="indefinite"/>
    {''.join(body)}
  </g>

  <rect x="0" y="0" width="{W2}" height="66" fill="url(#cTop)"/>
  <rect x="0" y="{H2 - 66}" width="{W2}" height="66" fill="url(#cBot)"/>

  <text x="28" y="27" font-family="{MONO}" font-size="8.4" letter-spacing="3.6" fill="{ASH}">END CREDITS</text>
  <text x="{W2 - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="8.4" letter-spacing="3.2"
        fill="{ASH}" fill-opacity="0.75">CHAPTER 001 · THE ECLIPSE</text>
  <line x1="28" y1="37" x2="{W2 - 28}" y2="37" stroke="{CHERRY}" stroke-opacity="0.22"/>

  <text x="28" y="{H2 - 14}" font-family="{MONO}" font-size="8.4" letter-spacing="3" fill="{DIM}">
    SILENT · {TRAVEL} SECONDS · LOOPS
  </text>
  <circle cx="{W2 - 110}" cy="{H2 - 18}" r="2.8" fill="{CHERRY_L}">
    <animate attributeName="opacity" values="1;0.12;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W2 - 98}" y="{H2 - 14}" font-family="{MONO}" font-size="8.4" letter-spacing="2.4" fill="{ASH}">END</text>

  <g>{grain(W2, H2, 56)}</g>
  <g opacity="0.4">{scan(W2, H2)}</g>
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
# 6. EMBLEM + DIVIDER
# ══════════════════════════════════════════════════════════════════════════
def build_emblem():
    S = 360
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}" fill="none" role="img" aria-label="The eclipse">
  <defs>
    {HALO_GRAD}
    {CORONA_GRAD}
    <radialGradient id="emSun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFFDFB"/>
      <stop offset="0.55" stop-color="#FFF0E6"/>
      <stop offset="0.85" stop-color="{CORAL}"/>
      <stop offset="1" stop-color="{CHERRY_L}"/>
    </radialGradient>
  </defs>
  <rect width="{S}" height="{S}" fill="{INK}"/>
  <circle cx="180" cy="180" r="180" fill="url(#mHalo)"/>

  <circle cx="180" cy="180" r="116" fill="url(#emSun)"/>

  <g transform="translate(180,180)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="34s" repeatCount="indefinite"/>
      <circle cx="10" r="110" fill="#040308"/>
    </g>
  </g>

  <circle cx="180" cy="180" r="116" fill="none" stroke="url(#mCorona)" stroke-width="1.8" stroke-opacity="0.95"/>
  <circle cx="180" cy="180" r="128" fill="none" stroke="{CORAL}" stroke-opacity="0.18" stroke-width="0.8">
    <animate attributeName="stroke-opacity" values="0.08;0.28;0.08" dur="6.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="180" cy="180" r="150" fill="none" stroke="{CHERRY}" stroke-opacity="0.10" stroke-width="0.7"/>

  <g opacity="0.5">{grain(S, S, 24)}</g>
</svg>
'''


def build_divider():
    W2, H2 = 1200, 64
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="">
  <defs>
    <linearGradient id="dRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.18" stop-color="{CHERRY}" stop-opacity="0.35"/>
      <stop offset="0.5" stop-color="{CHERRY_L}" stop-opacity="0.55"/>
      <stop offset="0.82" stop-color="{CHERRY}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    {CORONA_GRAD}
  </defs>
  <line x1="0" y1="32" x2="574" y2="32" stroke="url(#dRule)"/>
  <line x1="626" y1="32" x2="1200" y2="32" stroke="url(#dRule)"/>
  <g transform="translate(600,32)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="22s" repeatCount="indefinite"/>
      <circle r="14" fill="#040308"/>
      <circle r="14" fill="none" stroke="url(#mCorona)" stroke-width="1.3" stroke-opacity="0.9"/>
    </g>
  </g>
  <circle cx="600" cy="32" r="19" fill="none" stroke="{CHERRY}" stroke-opacity="0.18" stroke-width="0.6"/>
</svg>
'''


# ── run ─────────────────────────────────────────────────────────────────────
BUILDERS = {
    "opening.svg": build_opening,
    "record.svg": build_record,
    "bench.svg": build_bench,
    "queue.svg": build_queue,
    "credits.svg": build_credits,
    "emblem.svg": build_emblem,
    "divider.svg": build_divider,
}

if __name__ == "__main__":
    if PROOF:
        svg = BUILDERS["opening.svg"]()
        (OUT / f"_proof_{SCENE}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote _proof_{SCENE}.svg  {len(svg):6d} b")
    else:
        total = 0
        for name, fn in BUILDERS.items():
            svg = fn()
            (OUT / name).write_text(svg, encoding="utf-8")
            total += len(svg)
            print(f"wrote {name:14s} {len(svg):7d} b")
        print(f"total {total} bytes")
