#!/usr/bin/env python3
"""The opening title sequence — director's cut.

Twenty-four seconds, three acts, one seal. Everything is SMIL, so it plays
inside GitHub's <img> sandbox without a single line of JavaScript.

    ACT I    THE MARK    0.0 –  8.1   a slash, sparks, the name arrives
    ACT II   THE EIGHT   8.1 – 16.9   the seal ring and its eight nodes
    ACT III  THE SEAL   16.9 – 23.0   end card, iris out to black

The whole thing is one 24 s timeline. Every animation is a single
`dur="24s" repeatCount="indefinite"` track built from (second, value) pairs,
so nothing drifts out of phase and nothing loops early.

Run:  python3 build_opening.py          # writes opening.svg
      python3 build_opening.py --proof  # writes a static frame (everything open)
"""
import math
import pathlib
import random
import sys

random.seed(23)

HERE = pathlib.Path(__file__).parent

INK    = "#07060A"
CREAM  = "#F2E8D5"
SAND   = "#C9BBA3"
ASH    = "#8A8090"
DIM    = "#4A4353"
VERM   = "#C1272D"
VERM_L = "#E8453F"
CHAKRA = "#4FB3D9"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

W, H = 1200, 560
BAR = 46                       # letterbox thickness
CYCLE = 24.0                   # seconds per loop

CX = 600
NAME_Y = 298                   # baseline of the act I title
RING_Y = 258                   # centre of the act II seal
RING_R = 152

_PROOF_ARG = next((a for a in sys.argv if a.startswith("--proof")), None)
PROOF = _PROOF_ARG is not None      # freeze every track at its open state
ONLY = int(_PROOF_ARG.split("=")[1]) if _PROOF_ARG and "=" in _PROOF_ARG else 1


# ── timeline helpers ────────────────────────────────────────────────────────
def track(attr, pairs, extra=""):
    """One full-cycle SMIL track from (second, value) pairs."""
    ps = []
    for t, v in pairs:
        t = max(0.0, min(CYCLE, float(t)))
        if ps and abs(ps[-1][0] - t) < 1e-6:
            ps[-1] = (t, v)          # later value wins on a duplicate keyTime
        else:
            ps.append((t, v))
    if ps[0][0] > 0:
        ps.insert(0, (0.0, ps[0][1]))
    if ps[-1][0] < CYCLE:
        ps.append((CYCLE, ps[-1][1]))
    vals = ";".join(str(v) for _, v in ps)
    kts = ";".join(f"{t / CYCLE:.5f}" for t, _ in ps)
    return (f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kts}" '
            f'dur="{CYCLE}s" repeatCount="indefinite"{extra}/>')


def tr(attr, pairs, extra=""):
    return "" if PROOF else track(attr, pairs, extra)


def op(pairs):
    """Initial opacity attribute value."""
    return "1" if PROOF else str(pairs[0][1])


def act(n, pairs):
    """Opacity for an act group; in proof mode only the requested act is lit."""
    if PROOF:
        return "1" if ONLY in (0, n) else "0"
    return str(pairs[0][1])


def show(t_in, t_out, fade=0.12):
    """Opacity pairs for a single visible window."""
    if t_in <= 0.0001:
        return [(0, 1)] if t_out >= CYCLE else [(0, 1), (t_out, 1), (t_out + fade, 0)]
    if t_out >= CYCLE:
        return [(0, 0), (t_in - fade, 0), (t_in, 1)]
    return [(0, 0), (t_in - fade, 0), (t_in, 1), (t_out, 1), (t_out + fade, 0)]


def spiral_len(r0, r1, turns, steps=420):
    total, prev = 0.0, None
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        p = (r * math.cos(th), r * math.sin(th))
        if prev:
            total += math.hypot(p[0] - prev[0], p[1] - prev[1])
        prev = p
    return total


def spiral_d(r0, r1, turns, steps=380):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        pts.append((r * math.cos(th), r * math.sin(th)))
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts)


# ── geometry ────────────────────────────────────────────────────────────────
RING_C = 2 * math.pi * RING_R
RING2_C = 2 * math.pi * (RING_R * 0.78)
SPIRAL_L = spiral_len(22, 112, 2.4)
SPIRAL_D = spiral_d(22, 112, 2.4)
SLASH_L = math.hypot(1320, 236)

NODES = [  # (label, accent, clock angle in degrees, 270 = top)
    ("SKILL-VERSE",     "#7C6BF0", 270),
    ("RESONATE",        "#E0563F", 315),
    ("RAKSHABANDHAN",   "#E8A33D", 0),
    ("VERDE PREVIOUS",  "#6E8B7A", 45),
    ("NIRMAN PORTFOLIO", "#C1272D", 90),
    ("NIRMAAN APP",     "#00E08A", 135),
    ("VERDE APP",       "#4FB3D9", 180),
    ("VERDE PORTFOLIO", "#5BD69B", 225),
]

# static film grain
grain = "".join(
    f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, H):.0f}" '
    f'r="{random.uniform(0.35, 1.05):.1f}" fill="#FFFFFF" fill-opacity="0.05">'
    f'<animate attributeName="fill-opacity" values="0.02;0.06;0.03;0.07;0.02" '
    f'dur="{random.uniform(0.9, 2.2):.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(78)
)

# drifting dust in the ring scene
dust = "".join(
    f'<circle cx="{random.uniform(40, 1160):.0f}" cy="{random.uniform(60, 500):.0f}" '
    f'r="{random.uniform(0.5, 1.4):.1f}" fill="{random.choice([CREAM, CHAKRA, VERM_L])}" '
    f'fill-opacity="0">'
    f'<animate attributeName="fill-opacity" '
    f'values="0;{random.uniform(0.10, 0.30):.2f};0" dur="{random.uniform(2.6, 5.4):.1f}s" '
    f'begin="{random.uniform(0, 5):.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(32)
)

# sparks thrown off the slash
sparks = []
for _ in range(36):
    ang = random.uniform(-0.55, 0.55) + (random.choice([0, math.pi]))
    dist = random.uniform(70, 430)
    dx, dy = math.cos(ang) * dist, math.sin(ang) * dist * 0.42
    t0 = random.uniform(0.24, 0.34)
    spark_col = random.choice([VERM_L, VERM_L, CREAM, "#FFB199"])
    sparks.append(
        f'<g transform="translate({CX},{NAME_Y - 18})"><g opacity="{op([(0, 0.95)])}">'
        + tr("opacity", [(0, 0.95), (t0, 0.95), (t0 + 0.55, 0)])
        + f'<animateTransform attributeName="transform" type="translate" '
          f'values="0 0;0 0;{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f}" '
          f'keyTimes="0;{t0 / CYCLE:.5f};{(t0 + 0.55) / CYCLE:.5f};1" '
          f'dur="{CYCLE}s" repeatCount="indefinite"/>'
        + f'<circle r="{random.uniform(0.8, 2.0):.1f}" fill="{spark_col}"/></g></g>'
    )
sparks = "".join(sparks)

# speed lines behind the slash
speed = []
for _ in range(14):
    y = random.uniform(BAR + 24, H - BAR - 24)
    x = random.uniform(-120, 900)
    ln = random.uniform(120, 420)
    opa = random.uniform(0.10, 0.34)
    speed.append(
        f'<rect x="{x:.0f}" y="{y:.1f}" width="{ln:.0f}" height="1" fill="{CREAM}" '
        f'opacity="{op([(0, 0)])}">'
        + tr("opacity", [(0, 0), (0.20, 0), (0.30, opa), (0.62, 0)])
        + "</rect>"
    )
speed = "".join(speed)

# seal-ring ticks
ticks = "".join(
    f'<line x1="{RING_R + 8:.1f}" y1="0" x2="{RING_R + (16 if i % 4 == 0 else 12):.1f}" y2="0" '
    f'stroke="{VERM_L if i % 4 == 0 else VERM}" stroke-opacity="{0.55 if i % 4 == 0 else 0.28}" '
    f'stroke-width="{1.2 if i % 4 == 0 else 0.8}"/>'
    for i, _ in enumerate(range(56))
)

# the eight nodes
node_svg = []
for i, (label, accent, deg) in enumerate(NODES):
    rad = math.radians(deg)
    nx, ny = CX + RING_R * math.cos(rad), RING_Y + RING_R * math.sin(rad)
    lx, ly = CX + 190 * math.cos(rad), RING_Y + 190 * math.sin(rad)
    c = math.cos(rad)
    anchor = "start" if c > 0.25 else ("end" if c < -0.25 else "middle")
    t0 = 11.55 + i * 0.17
    node_svg.append(
        f'<g opacity="{op([(0, 0)])}">'
        + tr("opacity", show(t0, 16.4, 0.30))
        + f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="9" fill="none" stroke="{accent}" stroke-opacity="0.30">'
          f'<animate attributeName="r" values="8;13;8" dur="3.4s" begin="{i * 0.2:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="stroke-opacity" values="0.32;0.06;0.32" dur="3.4s" begin="{i * 0.2:.1f}s" repeatCount="indefinite"/>'
          f'</circle>'
        + f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="3.4" fill="{accent}"/>'
        + f'<line x1="{nx + 6 * c:.1f}" y1="{ny:.1f}" x2="{lx - 8 * c:.1f}" y2="{ly:.1f}" '
          f'stroke="{accent}" stroke-opacity="0.34" stroke-width="0.8"/>'
        + f'<text x="{lx:.1f}" y="{ly + 3:.1f}" text-anchor="{anchor}" font-family="{MONO}" '
          f'font-size="8.4" letter-spacing="1.5" fill="{CREAM}" fill-opacity="0.82">{label}</text>'
        + "</g>"
    )
node_svg = "".join(node_svg)

# timecode: one label per second, only one of them visible at a time
timecode = []
for i in range(1 if PROOF else 24):
    pairs = [(0, 0), (i, 1 if i == 0 else 0), (i + 0.02, 1), (i + 0.96, 1), (i + 1.0, 0)]
    timecode.append(
        f'<text x="1172" y="{H - BAR + 30}" text-anchor="end" font-family="{MONO}" '
        f'font-size="9" letter-spacing="1.8" fill="{ASH}" opacity="{op(pairs)}">'
        + tr("opacity", pairs)
        + f"00:00:{i:02d}</text>"
    )
timecode = "".join(timecode)


# ── the film ────────────────────────────────────────────────────────────────
def build():
    flash = "" if PROOF else (
        f'<rect width="{W}" height="{H}" fill="{CREAM}" opacity="0">'
        + track("opacity", [(0, 0), (0.26, 0), (0.31, 0.42), (0.48, 0)])
        + "</rect>"
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — title sequence">
  <defs>
    <radialGradient id="opGlow" cx="0.5" cy="0.45" r="0.55">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.17"/>
      <stop offset="0.55" stop-color="{VERM}" stop-opacity="0.045"/>
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
    <linearGradient id="opSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.45" stop-color="{VERM_L}" stop-opacity="1"/>
      <stop offset="0.55" stop-color="#FFD3C4" stop-opacity="1"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="opBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ASH}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{VERM_L}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{ASH}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="opReveal">
      <rect x="0" y="0" width="{'1200' if PROOF else '0'}" height="{H}">
        {tr("width", [(0, 0), (0.58, 0), (1.12, 1210), (23.2, 1210)])}
      </rect>
    </clipPath>
    <pattern id="opGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.016" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#opGrid)"/>
  <rect width="{W}" height="{H}" fill="url(#opGlow)"/>

  <!-- poster frame: keeps a frozen render (mobile, reduced motion) from being a black hole -->
  <g opacity="0.09">
    <circle cx="{CX}" cy="{RING_Y}" r="{RING_R}" fill="none" stroke="{VERM}" stroke-width="1.4"/>
    <path d="M {CX - 96:.1f},{RING_Y} a 96,96 0 1 1 96,96" fill="none" stroke="{VERM_L}" stroke-width="2"/>
  </g>
  <g opacity="0.2">
    {tr("opacity", [(0, 0.2), (6.2, 0.2), (7.2, 0)])}
    <text x="{CX}" y="176" text-anchor="middle" font-family="{MONO}" font-size="10.5"
          letter-spacing="6.4" fill="#B9AFC0" fill-opacity="0.7">INTERFACE SYSTEMS · GURUGRAM, INDIA</text>
    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="94"
          letter-spacing="5" fill="{CREAM}">ANUJ PHULERA</text>
    <rect x="{CX - 230}" y="330" width="460" height="1.6" fill="{VERM_L}" fill-opacity="0.6"/>
    <text x="{CX}" y="368" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.3" fill="{CREAM}" fill-opacity="0.55">I don't chase attention.</text>
    <text x="{CX}" y="394" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.3" fill="{VERM_L}" fill-opacity="0.55">I build things that command it.</text>
  </g>

  <!-- ══ ACT I · THE MARK ══════════════════════════════════════════════ -->
  <g opacity="{act(1, show(0.12, 8.10))}">
    {tr("opacity", show(0.12, 8.10))}

    {'' if PROOF else speed}

    <!-- diagonal slash -->
    <line x1="-60" y1="{NAME_Y + 122}" x2="1260" y2="{NAME_Y - 114}" stroke="url(#opSweep)"
          stroke-width="3" stroke-linecap="round" stroke-dasharray="{SLASH_L:.1f}"
          stroke-dashoffset="{'0' if PROOF else f'{SLASH_L:.1f}'}" opacity="{op([(0, 0)])}">
      {tr("stroke-dashoffset", [(0, SLASH_L), (0.22, SLASH_L), (0.40, 0), (24, 0)])}
      {tr("opacity", [(0, 0), (0.20, 0), (0.24, 1), (0.60, 0.9), (0.86, 0)])}
    </line>

    <!-- impact flash -->
    {flash}

    {sparks}

    <!-- the name, wiped in -->
    <g clip-path="url(#opReveal)">
      <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="94"
            letter-spacing="5" fill="url(#opName)">ANUJ PHULERA</text>
    </g>

    <text x="{CX}" y="176" text-anchor="middle" font-family="{MONO}" font-size="10.5"
          letter-spacing="6.4" fill="#B9AFC0" opacity="{op(show(0.70, 8.05, 0.3))}">
      {tr("opacity", show(0.70, 8.05, 0.3))}INTERFACE SYSTEMS · GURUGRAM, INDIA
    </text>

    <rect x="{CX - 230}" y="330" width="{'460' if PROOF else '0'}" height="1.6" fill="url(#opRule)" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (1.24, 0), (1.30, 1), (7.6, 1), (8.0, 0)])}
      {tr("width", [(0, 0), (1.24, 0), (2.02, 460), (24, 460)])}
    </rect>

    <text x="{CX}" y="368" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.3" fill="{CREAM}" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (1.46, 0), (1.82, 0.95), (7.5, 0.95), (7.95, 0)])}
      I don't chase attention.
    </text>
    <text x="{CX}" y="394" text-anchor="middle" font-family="{MONO}" font-size="14"
          letter-spacing="1.3" fill="{VERM_L}" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (1.70, 0), (2.06, 1), (7.5, 1), (7.95, 0)])}
      I build things that command it.
    </text>

    <!-- a glint crosses the title late in the act -->
    <rect x="-140" y="{NAME_Y - 96}" width="120" height="128" fill="url(#opSweep)" opacity="0">
      {tr("opacity", [(0, 0), (6.55, 0), (6.62, 0.5), (6.95, 0.35), (7.10, 0)])}
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1500 0;1500 0"
                        keyTimes="0;{6.55 / CYCLE:.5f};{7.10 / CYCLE:.5f};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>

    <g opacity="{op(show(3.0, 8.0, 0.25))}">
      {tr("opacity", show(3.0, 8.0, 0.25))}
      <rect x="46" y="{H - BAR - 62}" width="252" height="28" fill="none" stroke="{VERM}" stroke-opacity="0.45"/>
      <text x="62" y="{H - BAR - 43}" font-family="{MONO}" font-size="9.5" letter-spacing="2.6" fill="{VERM_L}">
        CHAPTER 001 · THE SEAL
      </text>
    </g>

    <text x="1154" y="{H - BAR - 43}" text-anchor="end" font-family="{MONO}" font-size="9"
          letter-spacing="2.6" fill="{DIM}" opacity="{op(show(3.0, 8.0, 0.25))}">
      {tr("opacity", show(3.0, 8.0, 0.25))}ACT I / III
    </text>
  </g>

  <!-- ══ ACT II · THE EIGHT ════════════════════════════════════════════ -->
  <g opacity="{act(2, show(8.55, 16.95, 0.16))}">
    {tr("opacity", show(8.55, 16.95, 0.16))}

    {dust}

    <!-- tick ring -->
    <g transform="translate({CX},{RING_Y})" opacity="{op([(0, 0.85)])}">
      {tr("opacity", [(0, 0.85), (10.9, 0.85), (16.7, 0)])}
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="260s" repeatCount="indefinite"/>
        {ticks}
      </g>
    </g>

    <!-- outer ring draws -->
    <circle cx="{CX}" cy="{RING_Y}" r="{RING_R}" fill="none" stroke="{VERM}" stroke-opacity="0.62"
            stroke-width="1.7" stroke-dasharray="{RING_C:.1f}"
            stroke-dashoffset="{'0' if PROOF else f'{RING_C:.1f}'}">
      {tr("stroke-dashoffset", [(0, RING_C), (8.70, RING_C), (11.30, 0), (24, 0)])}
    </circle>
    <circle cx="{CX}" cy="{RING_Y}" r="{RING_R * 0.78:.1f}" fill="none" stroke="{VERM}" stroke-opacity="0.24"
            stroke-width="0.9" stroke-dasharray="{RING2_C:.1f}"
            stroke-dashoffset="{'0' if PROOF else f'{RING2_C:.1f}'}">
      {tr("stroke-dashoffset", [(0, RING2_C), (9.25, RING2_C), (11.75, 0), (24, 0)])}
    </circle>

    <!-- the spiral -->
    <g transform="translate({CX},{RING_Y})">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="80s" repeatCount="indefinite"/>
        <path d="{SPIRAL_D}" fill="none" stroke="{VERM_L}" stroke-opacity="0.9" stroke-width="5.4"
              stroke-linecap="round" stroke-dasharray="{SPIRAL_L:.1f}"
              stroke-dashoffset="{'0' if PROOF else f'{SPIRAL_L:.1f}'}">
          {tr("stroke-dashoffset", [(0, SPIRAL_L), (10.45, SPIRAL_L), (13.05, 0), (24, 0)])}
        </path>
        <path d="{SPIRAL_D}" fill="none" stroke="{CREAM}" stroke-opacity="0.30" stroke-width="1.1"
              stroke-linecap="round" stroke-dasharray="{SPIRAL_L:.1f}"
              stroke-dashoffset="{'0' if PROOF else f'{SPIRAL_L:.1f}'}">
          {tr("stroke-dashoffset", [(0, SPIRAL_L), (10.9, SPIRAL_L), (13.5, 0), (24, 0)])}
        </path>
      </g>
    </g>

    {node_svg}

    <text x="{CX}" y="498" text-anchor="middle" font-family="{MONO}" font-size="10"
          letter-spacing="5" fill="{ASH}" opacity="{op(show(12.6, 16.8, 0.3))}">
      {tr("opacity", show(12.6, 16.8, 0.3))}EIGHT SEALS · ONE HAND
    </text>

    <text x="1154" y="{H - BAR - 43}" text-anchor="end" font-family="{MONO}" font-size="9"
          letter-spacing="2.6" fill="{DIM}" opacity="{op(show(9.2, 16.8, 0.25))}">
      {tr("opacity", show(9.2, 16.8, 0.25))}ACT II / III
    </text>
  </g>

  <!-- ══ ACT III · THE SEAL ════════════════════════════════════════════ -->
  <g opacity="{act(3, show(17.35, 23.3, 0.2))}">
    {tr("opacity", show(17.35, 23.3, 0.2))}

    <g transform="translate({CX},236)" opacity="0.16">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="26s" repeatCount="indefinite"/>
        <path d="{spiral_d(10, 104, 2.6)}" fill="none" stroke="{VERM_L}" stroke-width="7" stroke-linecap="round"/>
      </g>
    </g>

    <text x="{CX}" y="142" text-anchor="middle" font-family="{MONO}" font-size="10"
          letter-spacing="7" fill="{ASH}">CHAPTER 001</text>

    <text x="{CX}" y="240" text-anchor="middle" font-family="{BLACK}" font-size="84"
          letter-spacing="6" fill="url(#opName)">THE SEAL</text>

    <rect x="{CX - 210}" y="268" width="420" height="1.4" fill="url(#opRule)" opacity="0.9"/>

    <text x="{CX}" y="304" text-anchor="middle" font-family="{MONO}" font-size="12"
          letter-spacing="3.2" fill="{CREAM}" fill-opacity="0.92">INTERFACE ENGINEER · GURUGRAM, INDIA</text>

    <text x="{CX}" y="332" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="3.4" fill="{DIM}">FIFTEEN · CLASS 10 · EIGHT PROJECTS · ONE ENGINE</text>

    <text x="{CX}" y="424" text-anchor="middle" font-family="{MONO}" font-size="9"
          letter-spacing="4.6" fill="{VERM_L}" opacity="0.7">SEALING CORPS</text>

    <text x="1154" y="{H - BAR - 43}" text-anchor="end" font-family="{MONO}" font-size="9"
          letter-spacing="2.6" fill="{DIM}">ACT III / III</text>
  </g>

  <!-- ══ scene-change sweeps ═══════════════════════════════════════════ -->
  <g opacity="0">
    {tr("opacity", [(0, 0), (7.92, 0), (7.98, 1), (8.48, 1), (8.55, 0),
                    (16.72, 0), (16.78, 1), (17.28, 1), (17.35, 0)])}
    <rect x="-40" y="0" width="26" height="{H}" fill="url(#opSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="-120 0;-120 0;1240 0;1240 0;1240 0;1240 0"
                        keyTimes="0;{(7.92) / CYCLE:.5f};{(8.46) / CYCLE:.5f};{(16.72) / CYCLE:.5f};{(17.26) / CYCLE:.5f};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>
    <rect x="-40" y="0" width="3" height="{H}" fill="{CREAM}" opacity="0.7">
      <animateTransform attributeName="transform" type="translate"
                        values="-120 0;-120 0;1240 0;1240 0;1240 0;1240 0"
                        keyTimes="0;{(7.92) / CYCLE:.5f};{(8.46) / CYCLE:.5f};{(16.72) / CYCLE:.5f};{(17.26) / CYCLE:.5f};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- ══ letterbox + HUD ═══════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.18"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{VERM}" fill-opacity="0.18"/>

  <text x="28" y="28" font-family="{MONO}" font-size="8.5" letter-spacing="3.4" fill="{ASH}">SEALING CORPS</text>
  <text x="1172" y="28" text-anchor="end" font-family="{MONO}" font-size="8.5" letter-spacing="3.4" fill="{ASH}" fill-opacity="0.8">
    CHAPTER 001 · THE SEAL
  </text>

  <text x="28" y="{H - BAR + 29}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2" fill="{DIM}">
    GURUGRAM · HARYANA · INDIA
  </text>

  <circle cx="{W - 208}" cy="{H - BAR + 26}" r="3.2" fill="{VERM_L}">
    <animate attributeName="opacity" values="1;0.12;1" dur="1.4s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 196}" y="{H - BAR + 29}" font-family="{MONO}" font-size="8.5" letter-spacing="2.4" fill="{ASH}">REC</text>
  {timecode}

  <rect x="0" y="{H - 3}" width="{'1200' if PROOF else '0'}" height="3" fill="url(#opBar)">
    {tr("width", [(0, 0), (CYCLE, 1200)])}
  </rect>

  <!-- ══ grain, scanlines, iris ════════════════════════════════════════ -->
  <g>{grain}</g>
  <g opacity="0.45">
    {"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#000000" stroke-opacity="0.18" stroke-width="1"/>' for y in range(0, H, 3))}
  </g>
  <circle cx="{CX}" cy="280" r="{'0' if PROOF else '0'}" fill="#000000">
    {tr("r", [(0, 0), (23.35, 0), (23.95, 780), (24, 780)])}
  </circle>
</svg>
'''


if __name__ == "__main__":
    if PROOF:
        svg = build()
        (HERE / f"_opening_proof_{ONLY}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote _opening_proof_{ONLY}.svg")
    else:
        svg = build()
        (HERE / "opening.svg").write_text(svg, encoding="utf-8")
        print(f"wrote opening.svg  {len(svg):6d} bytes  {W}x{H}  cycle={CYCLE}s")
