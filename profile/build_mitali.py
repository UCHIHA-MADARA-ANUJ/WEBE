#!/usr/bin/env python3
"""Mitali Chincholikar — profile kit.

Same grammar as the other kit (letterbox, grain, mono caps, a title sequence),
none of the same words. Her mark is an eclipse: the dark thing passing over
the bright thing, and the light that survives at the edge.

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
INK    = "#06060A"
PAPER  = "#0B0A10"
CARD   = "#0F0D13"
CHERRY = "#D01731"      # cherry red
CHERRY_L = "#FF4D5E"    # light coral
CORAL  = "#FF8A7A"      # light coral, softer
AQUA   = "#5FE3C0"      # aquamarine
CELESTE = "#A8DEF0"     # celeste
ICE    = "#DCEFF6"      # iceberg
CREAM  = "#F4EEF2"
ASH    = "#8B8391"
DIM    = "#504A59"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Work Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"

W, H = 1200, 560
BAR = 44
CYCLE = 16.0

SUN_CX, SUN_CY, SUN_R = 600, 206, 126
NAME_Y = 424

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


def eclipse(cx, cy, r, ring_w=2.0, glow=True, moon=True):
    """The mark. Bright corona, dark disc sitting inside it."""
    circ = 2 * math.pi * r
    parts = []
    if glow:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.1f}" fill="url(#mHalo)" opacity="0.55"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#050508"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#mCorona)" '
                 f'stroke-width="{ring_w}" stroke-opacity="0.95"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r - ring_w * 0.9:.1f}" fill="none" '
                 f'stroke="{CORAL}" stroke-width="0.7" stroke-opacity="0.30"/>')
    return "".join(parts)


# ══════════════════════════════════════════════════════════════════════════
# 1. THE OPENING
# ══════════════════════════════════════════════════════════════════════════
def build_opening():
    corona_c = 2 * math.pi * SUN_R
    hal_c = 2 * math.pi * (SUN_R * 1.55)

    # moon path: sweeps in, sits in totality, sweeps out
    moon_move = (
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="-940 0;-940 0;0 0;0 0;940 0;940 0" '
        f'keyTimes="0;{1.10 / CYCLE:.5f};{3.05 / CYCLE:.5f};{6.30 / CYCLE:.5f};'
        f'{7.85 / CYCLE:.5f};1" dur="{CYCLE}s" repeatCount="indefinite"/>'
    ) if not PROOF else ""

    # the queue lines in scene II
    rows = [
        ("01", "ADVANCED PYTHON", AQUA),
        ("02", "C", CELESTE),
        ("03", "UI / UX", CORAL),
        ("04", "SQL", AQUA),
        ("05", "C++", CELESTE),
        ("06", "NODE.JS", CORAL),
        ("07", "JAVA", AQUA),
    ]
    q = []
    for i, (n, label, c) in enumerate(rows):
        y = 240 + i * 30
        t0 = 8.05 + i * 0.20
        q.append(
            f'<g opacity="{op([(0, 0)])}">' + tr("opacity", show(t0, 11.55, 0.18))
            + f'<text x="356" y="{y}" font-family="{MONO}" font-size="9" letter-spacing="2" '
              f'fill="{DIM}">{n}</text>'
            + f'<circle cx="404" cy="{y - 4}" r="2.6" fill="{c}" fill-opacity="0.9"/>'
            + f'<text x="420" y="{y}" font-family="{MONO}" font-size="11.5" letter-spacing="2.2" '
              f'fill="{CREAM}" fill-opacity="0.9">{label}</text>'
            + f'<line x1="404" y1="{y + 10}" x2="{404 + 40 + i * 22}" y2="{y + 10}" '
              f'stroke="{c}" stroke-opacity="0.22"/>'
            + '</g>'
        )
    queue = "".join(q)

    found = "".join(
        f'<g opacity="1"><text x="{356 + i * 118}" y="196" font-family="{MONO}" font-size="10.5" '
        f'letter-spacing="2" fill="{CREAM}" fill-opacity="0.72">{t}</text></g>'
        for i, t in enumerate(["PYTHON", "C", "HTML", "CSS", "JS"])
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Mitali Chincholikar — opening">
  <defs>
    <radialGradient id="mHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.30"/>
      <stop offset="0.42" stop-color="{CHERRY}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="mSun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFF3EE" stop-opacity="1"/>
      <stop offset="0.60" stop-color="{CORAL}" stop-opacity="0.98"/>
      <stop offset="0.93" stop-color="{CHERRY_L}" stop-opacity="0.96"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0.9"/>
    </radialGradient>
    <linearGradient id="mCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CORAL}"/>
      <stop offset="0.35" stop-color="{CHERRY_L}"/>
      <stop offset="0.62" stop-color="{CELESTE}"/>
      <stop offset="0.82" stop-color="{AQUA}"/>
      <stop offset="1" stop-color="{CORAL}"/>
    </linearGradient>
    <linearGradient id="mName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#B9AEBE"/>
    </linearGradient>
    <linearGradient id="mRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CHERRY_L}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="mSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CORAL}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    {grid_defs()}
    <clipPath id="mWipe">
      <rect x="0" y="0" width="{'1240' if PROOF else '0'}" height="{H}">
        {tr("width", [(0, 0), (3.15, 0), (4.05, 1240), (15.2, 1240)])}
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#mGrid)"/>
  <rect width="{W}" height="{H}" fill="url(#mHalo)" opacity="0.7"/>

  <!-- poster frame: a frozen render is still a complete title card -->
  <g opacity="0.13">
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R}" fill="#050508"/>
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R}" fill="none" stroke="{CHERRY_L}" stroke-width="1.6"/>
    <text x="600" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="70"
          font-weight="300" letter-spacing="9" fill="{CREAM}">MITALI CHINCHOLIKAR</text>
    <rect x="330" y="{NAME_Y + 22}" width="540" height="1.2" fill="{CHERRY_L}" fill-opacity="0.6"/>
    <text x="600" y="{NAME_Y + 60}" text-anchor="middle" font-family="{SANS}" font-size="19"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.62">
      I don't wait to be senior to build.
    </text>
  </g>

  <!-- ══ SCENE I · ECLIPSE ══════════════════════════════════════════════ -->
  <g opacity="{scene(1, show(0.10, 7.30))}">
    {tr("opacity", show(0.10, 7.30))}

    <g opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (0.25, 0), (1.30, 1), (7.0, 1), (7.3, 0)])}
      <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R}" fill="url(#mSun)"/>
      <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R * 1.55:.1f}" fill="none"
              stroke="{CHERRY}" stroke-opacity="0.18" stroke-width="0.8"
              stroke-dasharray="{hal_c:.1f}" stroke-dashoffset="{'0' if PROOF else f'{hal_c:.1f}'}">
        {tr("stroke-dashoffset", [(0, hal_c), (0.4, hal_c), (2.4, 0), (16, 0)])}
      </circle>
    </g>

    <!-- corona: drawn, then left burning at the rim -->
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 3}" fill="none" stroke="url(#mCorona)"
            stroke-width="2.4" stroke-opacity="0.9" stroke-dasharray="{corona_c:.1f}"
            stroke-dashoffset="{'0' if PROOF else f'{corona_c:.1f}'}">
      {tr("stroke-dashoffset", [(0, corona_c), (0.35, corona_c), (2.10, 0), (16, 0)])}
    </circle>
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 14}" fill="none" stroke="{CORAL}"
            stroke-opacity="0.16" stroke-width="0.8"/>

    <!-- the moon: it is the dark disc that makes the picture -->
    <g transform="translate({SUN_CX},{SUN_CY})">
      <g>{moon_move}
        <circle r="{SUN_R - 0.6}" fill="#040407"/>
        <circle r="{SUN_R - 0.6}" fill="none" stroke="{CHERRY}" stroke-opacity="0.25" stroke-width="0.6"/>
      </g>
    </g>

    <!-- totality: the thin ring that survives -->
    <circle cx="{SUN_CX}" cy="{SUN_CY}" r="{SUN_R + 2.4}" fill="none" stroke="{CORAL}"
            stroke-width="1.1" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (2.95, 0), (3.30, 0.95), (6.10, 0.75), (6.55, 0)])}
    </circle>

    <text x="600" y="{SUN_CY + 46}" text-anchor="middle" font-family="{MONO}" font-size="10"
          letter-spacing="7" fill="{ICE}" fill-opacity="0.55" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (3.10, 0), (3.55, 1), (6.2, 1), (6.6, 0)])}THE ECLIPSE
    </text>

    <g clip-path="url(#mWipe)">
      <text x="600" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="70"
            font-weight="300" letter-spacing="9" fill="url(#mName)">MITALI CHINCHOLIKAR</text>
    </g>

    <text x="600" y="168" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="5.4" fill="{ASH}" opacity="{op(show(3.5, 7.2, 0.3))}">
      {tr("opacity", show(3.5, 7.2, 0.3))}PUNE · CSE · FIRST YEAR
    </text>

    <rect x="330" y="{NAME_Y + 22}" width="{'540' if PROOF else '0'}" height="1.2"
          fill="url(#mRule)" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (4.05, 0), (4.15, 1), (6.7, 1), (7.15, 0)])}
      {tr("width", [(0, 0), (4.05, 0), (4.95, 540), (16, 540)])}
    </rect>

    <text x="600" y="{NAME_Y + 60}" text-anchor="middle" font-family="{SANS}" font-size="19"
          font-style="italic" font-weight="300" fill="{CREAM}" opacity="{op([(0, 0)])}">
      {tr("opacity", [(0, 0), (4.35, 0), (4.85, 0.98), (6.7, 0.98), (7.15, 0)])}
      I don't wait to be senior to build.
    </text>
  </g>

  <!-- ══ SCENE II · THE QUEUE ═══════════════════════════════════════════ -->
  <g opacity="{scene(2, show(7.55, 12.35))}">
    {tr("opacity", show(7.55, 12.35))}

    <rect x="316" y="130" width="568" height="322" rx="6" fill="{CARD}" stroke="#FFFFFF" stroke-opacity="0.07"/>
    <rect x="316" y="130" width="568" height="24" rx="6" fill="#FFFFFF" fill-opacity="0.03"/>
    <line x1="316" y1="154" x2="884" y2="154" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <circle cx="330" cy="142" r="2.4" fill="{CHERRY_L}" fill-opacity="0.6"/>
    <circle cx="339" cy="142" r="2.4" fill="{AQUA}" fill-opacity="0.6"/>
    <circle cx="348" cy="142" r="2.4" fill="{CELESTE}" fill-opacity="0.6"/>
    <text x="858" y="145.5" text-anchor="end" font-family="{MONO}" font-size="7.6"
          letter-spacing="2" fill="{DIM}">LEARNING QUEUE</text>

    <text x="336" y="178" font-family="{MONO}" font-size="7.6" letter-spacing="2.6"
          fill="{DIM}">TOUCHED</text>
    {found}

    <line x1="336" y1="212" x2="864" y2="212" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <text x="336" y="226" font-family="{MONO}" font-size="7.6" letter-spacing="2.6"
          fill="{DIM}">NEXT · IN ORDER</text>

    {queue}

  </g>

  <!-- ══ SCENE III · END CARD ═══════════════════════════════════════════ -->
  <g opacity="{scene(3, show(12.9, 15.4))}">
    {tr("opacity", show(12.9, 15.4))}

    {eclipse(600, 176, 58, 1.8, glow=True)}

    <text x="600" y="300" text-anchor="middle" font-family="{MONO}" font-size="9"
          letter-spacing="6" fill="{ASH}">CHAPTER 001</text>

    <text x="600" y="382" text-anchor="middle" font-family="{SANS}" font-size="54"
          font-weight="300" letter-spacing="7" fill="url(#mName)">THE ECLIPSE</text>

    <rect x="404" y="404" width="392" height="1.2" fill="url(#mRule)" opacity="0.9"/>

    <text x="600" y="438" text-anchor="middle" font-family="{SANS}" font-size="17"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.9">
      Here to turn ambition into reality.
    </text>

    <text x="600" y="466" text-anchor="middle" font-family="{MONO}" font-size="8.6"
          letter-spacing="3.4" fill="{DIM}">PUNE · MAHARASHTRA · INDIA</text>
  </g>

  <!-- ══ scene sweep ════════════════════════════════════════════════════ -->
  <g opacity="0">
    {tr("opacity", [(0, 0), (7.30, 0), (7.36, 1), (7.86, 1), (7.92, 0),
                    (12.10, 0), (12.16, 1), (12.66, 1), (12.72, 0)])}
    <rect x="-40" y="0" width="22" height="{H}" fill="url(#mSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="-120 0;-120 0;1240 0;1240 0;1240 0;1240 0"
                        keyTimes="0;{7.30 / CYCLE:.5f};{7.84 / CYCLE:.5f};{12.10 / CYCLE:.5f};{12.64 / CYCLE:.5f};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- ══ letterbox + HUD ════════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.20"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{CHERRY}" fill-opacity="0.20"/>

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
        letter-spacing="1.6" fill="{ASH}">00:00:16</text>

  <rect x="0" y="{H - 3}" width="{'1200' if PROOF else '0'}" height="3" fill="url(#mRule)">
    {tr("width", [(0, 0), (CYCLE, 1200)])}
  </rect>

  <g>{grain(W, H, 64)}</g>
  <g opacity="0.42">{scan(W, H)}</g>

  <circle cx="600" cy="280" r="0" fill="#000000">
    {tr("r", [(0, 0), (15.35, 0), (15.95, 780), (16, 780)])}
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
        )
        body.append(
            f'<line x1="380" y1="{y + 12}" x2="966" y2="{y + 12}" stroke="#FFFFFF" stroke-opacity="0.05"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" fill="none" role="img" aria-label="Mitali Chincholikar — the record">
  <defs>
    {grid_defs("rGrid")}
    <radialGradient id="mHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.30"/>
      <stop offset="0.42" stop-color="{CHERRY}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="mCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CORAL}"/>
      <stop offset="0.35" stop-color="{CHERRY_L}"/>
      <stop offset="0.62" stop-color="{CELESTE}"/>
      <stop offset="0.82" stop-color="{AQUA}"/>
      <stop offset="1" stop-color="{CORAL}"/>
    </linearGradient>
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

  <rect x="36" y="78" width="176" height="196" rx="5" fill="#0A0910" stroke="#FFFFFF" stroke-opacity="0.06"/>
  {eclipse(124, 160, 46, 1.6, glow=True)}
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
# 3. THE BENCH — two projects, both labelled honestly
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

    <rect x="{x + 26}" y="132" width="{CWv - 52}" height="118" rx="4" fill="#0A0910"
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
# 4. THE QUEUE
# ══════════════════════════════════════════════════════════════════════════
def build_queue():
    W2, H2 = 1000, 420
    nexts = ["ADVANCED PYTHON", "C", "UI / UX", "SQL", "C++", "NODE.JS", "JAVA"]
    also = ["SECURITY", "DESIGN", "STOCK MARKETS"]
    accent = [AQUA, CELESTE, CORAL, AQUA, CELESTE, CORAL, AQUA]

    rows = []
    for i, (n, a) in enumerate(zip(nexts, accent)):
        y = 128 + i * 30
        rows.append(
            f'<text x="44" y="{y}" font-family="{MONO}" font-size="8.4" letter-spacing="1.6" fill="{DIM}">0{i + 1}</text>'
            f'<rect x="82" y="{y - 9}" width="12" height="12" rx="2" fill="none" stroke="{a}" stroke-opacity="0.5"/>'
            f'<text x="108" y="{y}" font-family="{MONO}" font-size="11" letter-spacing="2.2" '
            f'fill="{CREAM}" fill-opacity="0.9">{n}</text>'
            f'<line x1="300" y1="{y - 4}" x2="{300 + 160 + i * 46}" y2="{y - 4}" stroke="{a}" stroke-opacity="0.18"/>'
        )

    also_svg = "".join(
        f'<rect x="{212 + i * 168}" y="352" width="152" height="26" rx="13" fill="{CORAL}" '
        f'fill-opacity="0.07" stroke="{CORAL}" stroke-opacity="0.28"/>'
        f'<text x="{288 + i * 168}" y="369" text-anchor="middle" font-family="{MONO}" font-size="8.4" '
        f'letter-spacing="2.2" fill="{CORAL}" fill-opacity="0.85">{t}</text>'
        for i, t in enumerate(also)
    )

    exposed = "".join(
        f'<circle cx="{150 + i * 24}" cy="86" r="3" fill="{AQUA}" fill-opacity="0.85">'
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
  </defs>
  <rect width="{W2}" height="{H2}" fill="{INK}"/>
  <rect width="{W2}" height="{H2}" fill="url(#qGrid)"/>
  <rect width="{W2}" height="{H2}" fill="url(#qGlow)"/>

  <rect x="10" y="10" width="{W2 - 20}" height="{H2 - 20}" rx="7" fill="{PAPER}"
        stroke="#FFFFFF" stroke-opacity="0.07"/>
  <rect x="10" y="10" width="{W2 - 20}" height="2" rx="1" fill="{AQUA}" fill-opacity="0.45"/>

  <text x="44" y="45" font-family="{MONO}" font-size="8.4" letter-spacing="4" fill="{ASH}">LEARNING QUEUE</text>
  <text x="{W2 - 44}" y="45" text-anchor="end" font-family="{MONO}" font-size="8.4" letter-spacing="2.6"
        fill="{DIM}">NOT SKILLS. A LIST OF WHAT'S NEXT.</text>
  <line x1="44" y1="58" x2="{W2 - 44}" y2="58" stroke="#FFFFFF" stroke-opacity="0.07"/>

  <text x="44" y="90" font-family="{MONO}" font-size="7.8" letter-spacing="2.8" fill="{DIM}">TOUCHED</text>
  <text x="284" y="90" font-family="{MONO}" font-size="9.4" letter-spacing="2.4" fill="{CREAM}"
        fill-opacity="0.8">PYTHON · C · HTML · CSS · JS</text>
  {exposed}

  <line x1="44" y1="108" x2="{W2 - 44}" y2="108" stroke="#FFFFFF" stroke-opacity="0.06"/>

  {''.join(rows)}

  <line x1="44" y1="338" x2="{W2 - 44}" y2="338" stroke="{CHERRY}" stroke-opacity="0.16"/>
  <text x="44" y="369" font-family="{MONO}" font-size="7.8" letter-spacing="2.8" fill="{DIM}">ALSO · NOT CODE</text>
  {also_svg}
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
        ("CHAPTER 001", ["THE ECLIPSE"]),
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
    <radialGradient id="mHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.26"/>
      <stop offset="0.55" stop-color="{CHERRY}" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="mCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CORAL}"/>
      <stop offset="0.35" stop-color="{CHERRY_L}"/>
      <stop offset="0.62" stop-color="{CELESTE}"/>
      <stop offset="0.82" stop-color="{AQUA}"/>
      <stop offset="1" stop-color="{CORAL}"/>
    </linearGradient>
    <radialGradient id="emSun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFF6F2" stop-opacity="1"/>
      <stop offset="0.62" stop-color="{CORAL}" stop-opacity="0.98"/>
      <stop offset="1" stop-color="{CHERRY_L}" stop-opacity="0.95"/>
    </radialGradient>
  </defs>
  <rect width="{S}" height="{S}" fill="{INK}"/>
  <circle cx="180" cy="180" r="176" fill="url(#mHalo)"/>

  <circle cx="180" cy="180" r="112" fill="url(#emSun)"/>

  <g transform="translate(180,180)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="34s" repeatCount="indefinite"/>
      <circle cx="7" r="108" fill="#050508"/>
      <circle cx="7" r="108" fill="none" stroke="{CHERRY}" stroke-opacity="0.35" stroke-width="0.8"/>
    </g>
  </g>

  <circle cx="180" cy="180" r="112" fill="none" stroke="url(#mCorona)" stroke-width="1.6" stroke-opacity="0.95"/>
  <circle cx="180" cy="180" r="124" fill="none" stroke="{CORAL}" stroke-opacity="0.18" stroke-width="0.8">
    <animate attributeName="stroke-opacity" values="0.08;0.26;0.08" dur="6.5s" repeatCount="indefinite"/>
  </circle>

  <g opacity="0.5">
    {grain(S, S, 24)}
  </g>
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
    <linearGradient id="dRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CORAL}"/>
      <stop offset="0.5" stop-color="{CHERRY_L}"/>
      <stop offset="1" stop-color="{AQUA}"/>
    </linearGradient>
  </defs>
  <line x1="0" y1="32" x2="574" y2="32" stroke="url(#dRule)"/>
  <line x1="626" y1="32" x2="1200" y2="32" stroke="url(#dRule)"/>
  <g transform="translate(600,32)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="22s" repeatCount="indefinite"/>
      <circle r="14" fill="#050508"/>
      <circle r="14" fill="none" stroke="url(#dRing)" stroke-width="1.3" stroke-opacity="0.9"/>
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
    total = 0
    for name, fn in BUILDERS.items():
        svg = fn()
        if PROOF and name == "opening.svg":
            (OUT / f"_proof_{SCENE}.svg").write_text(svg, encoding="utf-8")
            print(f"wrote _proof_{SCENE}.svg  {len(svg):6d} b")
            continue
        if PROOF:
            continue
        (OUT / name).write_text(svg, encoding="utf-8")
        total += len(svg)
        print(f"wrote {name:14s} {len(svg):7d} b")
    if not PROOF:
        print(f"total {total} bytes")
