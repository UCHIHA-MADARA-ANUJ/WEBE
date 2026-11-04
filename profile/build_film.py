#!/usr/bin/env python3
"""Both openings. One architecture.

    LAYER 1  THE POSTER   always painted, never animates, never leaves
    LAYER 2  THE SCRIM    the dark cloth that drops over it
    LAYER 3  THE FILM     the sequence, drawn on the cloth

At t=0 the scrim is up (transparent) so you see the poster. The scrim drops,
the film plays, the scrim lifts, the poster is back. The loop never lands on
a black frame, and a renderer that ignores SMIL entirely still shows the
poster — because the film is a layer on top of it, not a replacement.

Run:  python3 build_film.py
Out:  opening.svg  and  mitali/opening.svg
"""
import math
import pathlib
import random

HERE = pathlib.Path(__file__).parent
OUT = HERE / "mitali"
OUT.mkdir(exist_ok=True)

W, H = 1200, 700
BAR = 44
CX = 600
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"
SANS = "'Work Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif"


# ══════════════════════════════════════════════════════════════════════════
#  shared machinery
# ══════════════════════════════════════════════════════════════════════════
def track(attr, pairs, cycle, extra=""):
    """A full-cycle SMIL track from (second, value) pairs."""
    ps = []
    for t, v in pairs:
        t = max(0.0, min(cycle, float(t)))
        if ps and abs(ps[-1][0] - t) < 1e-9:
            ps[-1] = (t, v)
        else:
            ps.append((t, v))
    if ps[0][0] > 0:
        ps.insert(0, (0.0, ps[0][1]))
    if ps[-1][0] < cycle:
        ps.append((cycle, ps[-1][1]))
    return (f'<animate attributeName="{attr}" '
            f'values="{";".join(str(v) for _, v in ps)}" '
            f'keyTimes="{";".join(f"{t / cycle:.5f}" for t, _ in ps)}" '
            f'dur="{cycle}s" repeatCount="indefinite"{extra}/>')


def kf(t, cycle):
    return f"{max(0.0, min(cycle, t)) / cycle:.5f}"


def grain(w, h, n=56):
    return "".join(
        f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.uniform(0.3, 0.95):.1f}" fill="#FFFFFF" fill-opacity="0.05">'
        f'<animate attributeName="fill-opacity" values="0.02;0.06;0.03;0.065;0.02" '
        f'dur="{random.uniform(1.0, 2.4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(n)
    )


def scan(w, h, step=3):
    return "".join(
        f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#000000" stroke-opacity="0.16" '
        f'stroke-width="1"/>' for y in range(0, h, step)
    )


def spiral_d(r0, r1, turns, steps=300):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        pts.append((r * math.cos(th), r * math.sin(th)))
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts)


def spiral_len(r0, r1, turns, steps=600):
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


def hud(left_top, right_top, left_bot, mid_bot, right_bot, rec_color, ink, ash, dim, w=W, h=H, bar=BAR):
    return f'''
  <rect x="0" y="0" width="{w}" height="{bar}" fill="#000000"/>
  <rect x="0" y="{h - bar}" width="{w}" height="{bar}" fill="#000000"/>
  <rect x="0" y="{bar}" width="{w}" height="1" fill="{rec_color}" fill-opacity="0.26"/>
  <rect x="0" y="{h - bar - 1}" width="{w}" height="1" fill="{rec_color}" fill-opacity="0.26"/>
  <text x="28" y="27" font-family="{MONO}" font-size="8.5" letter-spacing="3.6" fill="{ash}">{left_top}</text>
  <text x="{w - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{ash}" fill-opacity="0.7">{right_top}</text>
  <text x="28" y="{h - bar + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2"
        fill="{dim}">{left_bot}</text>
  <text x="{w // 2}" y="{h - bar + 28}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{dim}" fill-opacity="0.85">{mid_bot}</text>
  <circle cx="{w - 118}" cy="{h - bar + 25}" r="3" fill="{rec_color}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{w - 106}" y="{h - bar + 28}" font-family="{MONO}" font-size="8.5"
        letter-spacing="2.4" fill="{ash}">REC</text>
  <text x="{w - 28}" y="{h - bar + 28}" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="1.8" fill="{ash}" fill-opacity="0.8">{right_bot}</text>
'''


# ══════════════════════════════════════════════════════════════════════════
#  ANUJ — the seal
# ══════════════════════════════════════════════════════════════════════════
def build_anuj():
    INK, CREAM, ASH, DIM = "#07060A", "#F2E8D5", "#93899B", "#5C5466"
    VERM, VERM_L, CHAKRA = "#C1272D", "#E8453F", "#4FB3D9"

    CYCLE = 26.0
    RING_CY, RING_R, NAME_Y, CHIP_Y = 268, 142, 486, 596

    # ticks
    ticks = []
    for i in range(72):
        ang = 2 * math.pi * i / 72 - math.pi / 2
        major = i % 6 == 0
        r0, r1 = RING_R + 10, RING_R + (26 if major else 17)
        ticks.append(
            f'<line x1="{r0*math.cos(ang):.1f}" y1="{r0*math.sin(ang):.1f}" '
            f'x2="{r1*math.cos(ang):.1f}" y2="{r1*math.sin(ang):.1f}" '
            f'stroke="{VERM_L if major else VERM}" stroke-opacity="{0.55 if major else 0.26}" '
            f'stroke-width="{1.2 if major else 0.8}"/>')
    ticks = "".join(ticks)

    PROJ = [("VERDE PORTFOLIO", "#5BD69B"), ("VERDE APP", "#4FB3D9"),
            ("NIRMAAN APP", "#00E08A"), ("NIRMAN PORTFOLIO", "#C1272D"),
            ("SKILL-VERSE", "#7C6BF0"), ("RESONATE", "#E0563F"),
            ("RAKSHABANDHAN", "#E8A33D"), ("VERDE PREVIOUS", "#6E8B7A")]
    CW_, GAP_ = 132, 8
    x0 = CX - (len(PROJ) * CW_ + (len(PROJ) - 1) * GAP_) / 2

    def chips(t0=None):
        out = []
        for i, (name, col) in enumerate(PROJ):
            cx = x0 + i * (CW_ + GAP_)
            anim = ""
            begin = ""
            if t0 is not None:
                begin = f' begin="{t0 + i * 0.11:.2f}s"'
            out.append(
                f'<g>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="28" rx="3" '
                f'fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.32"/>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="1.4" fill="{col}" fill-opacity="0.8">'
                f'<animate attributeName="fill-opacity" values="0.35;0.9;0.35" dur="4.2s"{begin} '
                f'repeatCount="indefinite"/></rect>'
                f'<circle cx="{cx + 11:.1f}" cy="{CHIP_Y + 14}" r="2.4" fill="{col}">'
                f'<animate attributeName="fill-opacity" values="0.3;1;0.3" dur="3.6s"{begin} repeatCount="indefinite"/>'
                f'</circle>'
                f'<text x="{cx + 20:.1f}" y="{CHIP_Y + 17.5}" font-family="{MONO}" font-size="6.6" '
                f'letter-spacing="0.7" fill="{CREAM}" fill-opacity="0.85">{name}</text>'
                f'</g>')
        return "".join(out)

    spiral = spiral_d(9, RING_R - 20, 2.6)
    SP_LEN = spiral_len(9, RING_R - 20, 2.6, steps=500)
    RING_C = 2 * math.pi * RING_R

    poster = f'''
  <!-- ══ LAYER 1 · THE POSTER — never animates away ══════════════════════ -->
  <g>
    <circle cx="{CX}" cy="{RING_CY}" r="300" fill="url(#sgGlow)" opacity="0.34"/>

    <g transform="translate({CX},{RING_CY})">
      <g opacity="0.9">{ticks}
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="200s" repeatCount="indefinite"/>
      </g>
      <circle r="{RING_R}" fill="none" stroke="url(#sgRing)" stroke-width="2.2"/>
      <circle r="{RING_R - 8}" fill="none" stroke="{VERM}" stroke-opacity="0.22" stroke-width="0.8"/>
      <g>
        <path d="{spiral}" fill="none" stroke="{VERM_L}" stroke-opacity="0.92"
              stroke-width="7.5" stroke-linecap="round"/>
        <path d="{spiral}" fill="none" stroke="{CREAM}" stroke-opacity="0.18"
              stroke-width="1.2" stroke-linecap="round"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="80s" repeatCount="indefinite"/>
      </g>
      <circle r="7" fill="{CREAM}" fill-opacity="0.9">
        <animate attributeName="r" values="6;9;6" dur="3.8s" repeatCount="indefinite"/>
      </circle>
      <circle r="18" fill="{VERM_L}" fill-opacity="0.16"/>
    </g>

    <text x="{CX}" y="86" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{ASH}">CHAPTER 001</text>
    <text x="{CX}" y="106" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{VERM_L}" fill-opacity="0.75">THE SEAL</text>

    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="74"
          letter-spacing="5" fill="url(#sgName)">ANUJ PHULERA</text>
    <rect x="{CX - 250}" y="{NAME_Y + 28}" width="500" height="1.3" fill="url(#sgRule)"/>
    <text x="{CX}" y="{NAME_Y + 62}" text-anchor="middle" font-family="{MONO}" font-size="15"
          letter-spacing="1.4" fill="{CREAM}" fill-opacity="0.92">I don't chase attention.</text>
    <text x="{CX}" y="{NAME_Y + 86}" text-anchor="middle" font-family="{MONO}" font-size="15"
          letter-spacing="1.4" fill="{VERM_L}">I build things that command it.</text>

    {chips()}

    <text x="{CX}" y="{CHIP_Y + 48}" text-anchor="middle" font-family="{MONO}" font-size="8"
          letter-spacing="3.6" fill="{DIM}">EIGHT SEALS · ONE HAND</text>

    <rect x="-230" y="{NAME_Y - 78}" width="230" height="106" fill="url(#sgSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1660 0;1660 0" keyTimes="0;0.30;0.64;1"
                        dur="14s" repeatCount="indefinite"/>
    </rect>
  </g>'''

    # ── the film ─────────────────────────────────────────────────────────
    def scrim():
        return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="{INK}" opacity="0">'
                + track("opacity", [(0, 0), (0.45, 0), (1.05, 1), (21.4, 1), (22.2, 0)],
                        CYCLE) + '</rect>')

    def fade_in(t0, t1, peak=1.0):
        return (f'opacity="0">' + track("opacity", [(0, 0), (t0, 0), (t0 + 0.3, peak),
                                                    (t1, peak), (t1 + 0.35, 0)], CYCLE))

    film = f'''
  <!-- ══ LAYER 2 · THE SCRIM ═════════════════════════════════════════════ -->
  {scrim()}

  <!-- ══ LAYER 3 · THE FILM ══════════════════════════════════════════════ -->

  <!-- the ring draws itself -->
  <g transform="translate({CX},{RING_CY})" {fade_in(1.0, 21.2, 1)}'''
    film = film.replace('{fade_in(1.0, 21.2, 1)}',
                        'opacity="0">' + track("opacity", [(0, 0), (1.0, 0),
                                                           (1.35, 1), (21.2, 1), (21.6, 0)], CYCLE)) + f'''
    <circle r="{RING_R}" fill="none" stroke="url(#sgRing)" stroke-width="2.6"
            stroke-dasharray="{RING_C:.1f}"
            stroke-dashoffset="{RING_C:.1f}">
      {track("stroke-dashoffset", [(0, RING_C), (1.2, RING_C), (4.2, 0), (CYCLE, 0)], CYCLE)}
    </circle>
    <circle r="{RING_R - 8}" fill="none" stroke="{VERM}" stroke-opacity="0.30" stroke-width="0.9"
            stroke-dasharray="{2*math.pi*(RING_R-8):.1f}"
            stroke-dashoffset="{2*math.pi*(RING_R-8):.1f}">
      {track("stroke-dashoffset", [(0, 2*math.pi*(RING_R-8)), (1.9, 2*math.pi*(RING_R-8)),
                                    (4.9, 0), (CYCLE, 0)], CYCLE)}
    </circle>

    <!-- the spiral traces -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="80s" repeatCount="indefinite"/>
      <path d="{spiral}" fill="none" stroke="{VERM_L}" stroke-opacity="0.95" stroke-width="8"
            stroke-linecap="round" stroke-dasharray="{SP_LEN:.1f}"
            stroke-dashoffset="{SP_LEN:.1f}">
        {track("stroke-dashoffset", [(0, SP_LEN), (4.0, SP_LEN), (6.6, 0), (CYCLE, 0)], CYCLE)}
        {track("stroke-opacity", [(0, 0.95), (4.0, 0.95), (6.6, 0.95), (21.4, 0.95), (22.2, 0)], CYCLE)}
      </path>
      <path d="{spiral}" fill="none" stroke="{CREAM}" stroke-opacity="0.35" stroke-width="1.4"
            stroke-linecap="round" stroke-dasharray="{SP_LEN:.1f}"
            stroke-dashoffset="{SP_LEN:.1f}">
        {track("stroke-dashoffset", [(0, SP_LEN), (4.6, SP_LEN), (7.4, 0), (CYCLE, 0)], CYCLE)}
      </path>
    </g>
    <circle r="9" fill="{CREAM}">
      {track("r", [(0, 0), (6.5, 0), (6.9, 18), (7.6, 9), (CYCLE, 9)], CYCLE)}
      {track("fill-opacity", [(0, 0), (6.5, 0), (6.9, 1), (21.4, 1), (22.0, 0)], CYCLE)}
    </circle>
  </g>

  <!-- the slash -->
  <rect x="0" y="{NAME_Y - 22}" width="1200" height="2" fill="url(#sgSweep)" opacity="0">
    {track("opacity", [(0, 0), (7.4, 0), (7.5, 1), (7.85, 1), (8.3, 0)], CYCLE)}
    {track("height", [(0, 1), (7.4, 1), (7.5, 6), (7.9, 2), (CYCLE, 2)], CYCLE)}
  </rect>

  <!-- the name, wiped in -->
  <g clip-path="url(#sgWipe)">
    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="74"
          letter-spacing="5" fill="url(#sgName)">{"" }
      <animate attributeName="opacity" values="0;0;1;1;0;0"
               keyTimes="0;{kf(7.2, CYCLE)};{kf(7.5, CYCLE)};{kf(21.2, CYCLE)};{kf(21.7, CYCLE)};1"
               dur="{CYCLE}s" repeatCount="indefinite"/>ANUJ PHULERA</text>
  </g>

  <rect x="{CX - 250}" y="{NAME_Y + 28}" width="500" height="1.3" fill="url(#sgRule)" opacity="0">
    {track("opacity", [(0, 0), (8.6, 0), (8.75, 1), (21.0, 1), (21.5, 0)], CYCLE)}
    {track("width", [(0, 0), (8.6, 0), (9.6, 500), (CYCLE, 500)], CYCLE)}
  </rect>

  <text x="{CX}" y="{NAME_Y + 62}" text-anchor="middle" font-family="{MONO}" font-size="15"
        letter-spacing="1.4" fill="{CREAM}" opacity="0">
    {track("opacity", [(0, 0), (9.1, 0), (9.5, 0.95), (21.0, 0.95), (21.5, 0)], CYCLE)}
    I don't chase attention.</text>
  <text x="{CX}" y="{NAME_Y + 86}" text-anchor="middle" font-family="{MONO}" font-size="15"
        letter-spacing="1.4" fill="{VERM_L}" opacity="0">
    {track("opacity", [(0, 0), (9.5, 0), (9.9, 1), (21.0, 1), (21.5, 0)], CYCLE)}
    I build things that command it.</text>

  <!-- the eight, cascading -->
  <g>{chips(10.6)}</g>

  <!-- the stamp -->
  <g opacity="0">
    {track("opacity", [(0, 0), (12.0, 0), (12.4, 1), (20.6, 1), (21.2, 0)], CYCLE)}
    <rect x="46" y="{H - BAR - 78}" width="268" height="30" fill="none" stroke="{VERM}" stroke-opacity="0.5"/>
    <text x="62" y="{H - BAR - 58}" font-family="{MONO}" font-size="9.5" letter-spacing="2.6"
          fill="{VERM_L}">CHAPTER 001 · THE SEAL</text>
  </g>
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — the seal">
  <defs>
    <radialGradient id="sgGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.20"/>
      <stop offset="0.40" stop-color="{VERM}" stop-opacity="0.08"/>
      <stop offset="0.72" stop-color="{VERM}" stop-opacity="0.025"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sgSky" cx="0.5" cy="0.40" r="0.66">
      <stop offset="0" stop-color="#160A0E"/>
      <stop offset="0.55" stop-color="#0B0709"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <linearGradient id="sgRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{VERM_L}"/><stop offset="0.35" stop-color="{VERM}"/>
      <stop offset="0.62" stop-color="{VERM_L}"/><stop offset="0.82" stop-color="{CHAKRA}"/>
      <stop offset="1" stop-color="{VERM_L}"/>
    </linearGradient>
    <linearGradient id="sgName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFDF6"/><stop offset="0.55" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#B3A78E"/>
    </linearGradient>
    <linearGradient id="sgRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.22" stop-color="{VERM_L}" stop-opacity="0.8"/>
      <stop offset="0.5" stop-color="{CREAM}" stop-opacity="0.85"/>
      <stop offset="0.78" stop-color="{VERM_L}" stop-opacity="0.8"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sgSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM_L}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CREAM}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{VERM_L}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="sgGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.014" stroke-width="1"/>
    </pattern>
    <clipPath id="sgFrame"><rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}"/></clipPath>
    <clipPath id="sgWipe">
      <rect x="0" y="0" width="0" height="{H}">
        {track("width", [(0, 0), (7.2, 0), (8.3, 1240), (21.6, 1240), (21.6, 0)], CYCLE)}
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g clip-path="url(#sgFrame)">
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}" fill="url(#sgSky)"/>
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}" fill="url(#sgGrid)"/>
{poster}
{film}
  </g>
{hud("SEALING CORPS", "CHAPTER 001 · THE SEAL", "GURUGRAM · HARYANA · INDIA",
     "GENIN · CLASS 10 · INTERFACE SYSTEMS", "00:00:26", VERM_L, INK, ASH, DIM)}
  <g>{grain(W, H, 52)}</g>
  <g opacity="0.40">{scan(W, H)}</g>
</svg>
'''


# ══════════════════════════════════════════════════════════════════════════
#  MITALI — the eclipse
# ══════════════════════════════════════════════════════════════════════════
def build_mitali():
    INK, CREAM, ASH, DIM = "#05040A", "#F4EEF2", "#9C93A6", "#5A5265"
    CHERRY, CHERRY_L, CORAL = "#D01731", "#FF4D5E", "#FF8A7A"
    AQUA, CELESTE, ICE = "#5FE3C0", "#A8DEF0", "#DCEFF6"

    CYCLE = 26.0
    EYE_CY, EYE_R, NAME_Y, CHIP_Y = 288, 148, 494, 600

    # corona: bright, colourful, alive
    rays = []
    for i in range(108):
        ang = 2 * math.pi * i / 108 + random.uniform(-0.010, 0.010)
        r0 = EYE_R + 5
        r1 = EYE_R + random.uniform(22, 118)
        x1, y1 = CX + r0 * math.cos(ang), EYE_CY + r0 * math.sin(ang)
        x2, y2 = CX + r1 * math.cos(ang), EYE_CY + r1 * math.sin(ang)
        col = random.choice([CORAL, CHERRY_L, CORAL, CELESTE, AQUA, ICE])
        o = random.uniform(0.26, 0.82)
        d = random.uniform(2.6, 6.0)
        lo = o * random.uniform(0.35, 0.6)
        rays.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-opacity="{o:.2f}" stroke-width="{random.uniform(0.5,1.9):.1f}" '
            f'stroke-linecap="round">'
            f'<animate attributeName="stroke-opacity" values="{o:.2f};{lo:.2f};{o:.2f}" '
            f'dur="{d:.1f}s" begin="{random.uniform(0,3):.1f}s" repeatCount="indefinite"/></line>')
    rays = "".join(rays)

    stars = []
    for _ in range(76):
        sx, sy = random.uniform(16, W - 16), random.uniform(BAR + 8, H - BAR - 8)
        if math.hypot(sx - CX, sy - EYE_CY) < EYE_R + 130:
            continue
        o = random.uniform(0.14, 0.6)
        stars.append(
            f'<circle cx="{sx:.0f}" cy="{sy:.1f}" r="{random.uniform(0.4,1.4):.1f}" '
            f'fill="{random.choice([ICE, CELESTE, CREAM])}" fill-opacity="{o:.2f}">'
            f'<animate attributeName="fill-opacity" values="{o:.2f};{o*0.15:.2f};{o:.2f}" '
            f'dur="{random.uniform(2.0,5.5):.1f}s" begin="{random.uniform(0,4):.1f}s" '
            f'repeatCount="indefinite"/></circle>')
    stars = "".join(stars)

    ITEMS = ["ADVANCED PYTHON", "C", "UI / UX", "SQL", "C++", "NODE.JS", "JAVA"]
    COLS = [AQUA, CELESTE, CORAL, AQUA, CELESTE, CORAL, AQUA]
    CW_, GAP_ = 138, 8
    x0 = CX - (len(ITEMS) * CW_ + (len(ITEMS) - 1) * GAP_) / 2

    def chips(t0=None):
        out = []
        for i, (label, col) in enumerate(zip(ITEMS, COLS)):
            cx = x0 + i * (CW_ + GAP_)
            begin = f' begin="{t0 + i * 0.12:.2f}s"' if t0 is not None else ""
            out.append(
                f'<g>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="28" rx="3" '
                f'fill="{col}" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.30"/>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CW_}" height="1.4" fill="{col}" fill-opacity="0.8">'
                f'<animate attributeName="fill-opacity" values="0.35;0.9;0.35" dur="4.4s"{begin} '
                f'repeatCount="indefinite"/></rect>'
                f'<circle cx="{cx + 11:.1f}" cy="{CHIP_Y + 14}" r="2.4" fill="{col}">'
                f'<animate attributeName="fill-opacity" values="0.3;1;0.3" dur="3.5s"{begin} repeatCount="indefinite"/>'
                f'</circle>'
                f'<text x="{cx + 20:.1f}" y="{CHIP_Y + 17.5}" font-family="{MONO}" font-size="6.8" '
                f'letter-spacing="0.7" fill="{CREAM}" fill-opacity="0.86">{label}</text>'
                f'<text x="{cx + 128:.1f}" y="{CHIP_Y + 17.5}" text-anchor="end" font-family="{MONO}" '
                f'font-size="6.4" fill="{DIM}">0{i+1}</text>'
                f'</g>')
        return "".join(out)

    poster = f'''
  <!-- ══ LAYER 1 · THE POSTER ═══════════════════════════════════════════ -->
  <g>
    <circle cx="{CX}" cy="{EYE_CY}" r="300" fill="url(#ecHalo)" opacity="0.42"/>
    {stars}

    {rays}
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 26}" fill="none" stroke="{CORAL}"
            stroke-opacity="0.10" stroke-width="16"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 56}" fill="none" stroke="{CELESTE}"
            stroke-opacity="0.055" stroke-width="26"/>

    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="{CORAL}" fill-opacity="0.14"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="#030207"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="none" stroke="url(#ecCorona)" stroke-width="3.2"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R - 4}" fill="none" stroke="{ICE}"
            stroke-opacity="0.55" stroke-width="0.9"/>

    <g transform="translate({CX},{EYE_CY})">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="-360"
                          dur="120s" repeatCount="indefinite"/>
        <circle cx="{EYE_R + 20}" r="11" fill="{ICE}" fill-opacity="0.28"/>
        <circle cx="{EYE_R + 20}" r="11" fill="none" stroke="{ICE}" stroke-opacity="0.45" stroke-width="0.8"/>
      </g>
    </g>

    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 100}" fill="none" stroke="{CHERRY}"
            stroke-opacity="0.13" stroke-width="0.8" stroke-dasharray="2 9">
      <animateTransform attributeName="transform" type="rotate" from="0 {CX} {EYE_CY}"
                        to="360 {CX} {EYE_CY}" dur="220s" repeatCount="indefinite"/>
    </circle>

    <text x="{CX}" y="86" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{ASH}">CHAPTER 001</text>
    <text x="{CX}" y="106" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="7" fill="{CELESTE}" fill-opacity="0.6">THE ECLIPSE</text>

    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="72"
          font-weight="300" letter-spacing="8" fill="url(#ecName)">MITALI CHINCHOLIKAR</text>
    <rect x="{CX - 280}" y="{NAME_Y + 30}" width="560" height="1.3" fill="url(#ecRule)"/>
    <text x="{CX}" y="{NAME_Y + 68}" text-anchor="middle" font-family="{SANS}" font-size="19"
          font-style="italic" font-weight="300" fill="{CREAM}" fill-opacity="0.92">
      I don't wait to be senior to build.</text>

    {chips()}
    <text x="{CX}" y="{CHIP_Y + 50}" text-anchor="middle" font-family="{MONO}" font-size="8"
          letter-spacing="3.6" fill="{DIM}">SEVEN ON THE QUEUE · NONE OF THEM LEARNED YET</text>

    <rect x="-210" y="{NAME_Y - 76}" width="200" height="106" fill="url(#ecSweep)">
      <animateTransform attributeName="transform" type="translate"
                        values="0 0;0 0;1640 0;1640 0" keyTimes="0;0.28;0.62;1"
                        dur="13s" repeatCount="indefinite"/>
    </rect>
  </g>'''

    film = f'''
  <!-- ══ LAYER 2 · THE SCRIM ═════════════════════════════════════════════ -->
  <rect x="0" y="0" width="{W}" height="{H}" fill="{INK}" opacity="0">
    {track("opacity", [(0, 0), (0.45, 0), (1.05, 1), (21.0, 1), (21.8, 0)], CYCLE)}
  </rect>

  <!-- ══ LAYER 3 · THE FILM ══════════════════════════════════════════════ -->

  <!-- the sun burns up -->
  <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R}" fill="url(#ecSun)" opacity="0">
    {track("opacity", [(0, 0), (1.0, 0), (1.6, 1), (3.2, 1), (4.4, 0.15), (20.8, 0.15), (21.4, 0)], CYCLE)}
    {track("r", [(0, EYE_R * 0.5), (1.6, EYE_R), (CYCLE, EYE_R)], CYCLE)}
  </circle>
  <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 40}" fill="{CORAL}" fill-opacity="0.10" opacity="0">
    {track("opacity", [(0, 0), (1.2, 0), (1.8, 1), (20.8, 1), (21.4, 0)], CYCLE)}
    {track("r", [(0, EYE_R), (1.8, EYE_R + 90), (5.0, EYE_R + 40), (CYCLE, EYE_R + 40)], CYCLE)}
  </circle>

  <!-- the moon crosses: totality -->
  <g transform="translate({CX},{EYE_CY})" opacity="0">
    {track("opacity", [(0, 0), (2.6, 0), (2.8, 1), (20.9, 1), (21.4, 0)], CYCLE)}
    <g>
      <animateTransform attributeName="transform" type="translate"
                        values="-820 0;-820 0;0 0;0 0;820 0;820 0"
                        keyTimes="0;{kf(1.3, CYCLE)};{kf(3.1, CYCLE)};{kf(6.6, CYCLE)};{kf(8.0, CYCLE)};1"
                        dur="{CYCLE}s" repeatCount="indefinite"/>
      <circle r="{EYE_R + 2}" fill="#020106"/>
      <circle r="{EYE_R + 2}" fill="none" stroke="{CHERRY}" stroke-opacity="0.35" stroke-width="0.9"/>
    </g>
  </g>

  <!-- corona flare at totality -->
  <g opacity="0">
    {track("opacity", [(0, 0), (2.9, 0), (3.15, 1), (4.4, 0.85), (20.9, 0.85), (21.4, 0)], CYCLE)}
    {rays}
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 3}" fill="none" stroke="url(#ecCorona)" stroke-width="3.4"/>
    <circle cx="{CX}" cy="{EYE_CY}" r="{EYE_R + 30}" fill="none" stroke="{CORAL}"
            stroke-opacity="0.10" stroke-width="18"/>
  </g>

  <!-- diamond ring, both contacts -->
  <g opacity="0">
    {track("opacity", [(0, 0), (2.86, 0), (3.00, 1), (3.22, 0), (6.44, 0), (6.58, 0.9), (6.80, 0)], CYCLE)}
    <circle cx="{CX - EYE_R}" cy="{EYE_CY}" r="8" fill="{ICE}"/>
    <circle cx="{CX - EYE_R}" cy="{EYE_CY}" r="26" fill="{CORAL}" fill-opacity="0.22"/>
    <line x1="{CX - EYE_R - 90}" y1="{EYE_CY}" x2="{CX - EYE_R - 16}" y2="{EYE_CY}"
          stroke="{ICE}" stroke-width="1.6" stroke-opacity="0.85"/>
    <line x1="{CX - EYE_R + 16}" y1="{EYE_CY}" x2="{CX - EYE_R + 90}" y2="{EYE_CY}"
          stroke="{ICE}" stroke-width="1.6" stroke-opacity="0.85"/>
  </g>

  <!-- corridor light sweep -->
  <rect x="-60" y="{BAR}" width="40" height="{H - BAR*2}" fill="url(#ecSweep)" opacity="0">
    {track("opacity", [(0, 0), (8.2, 0), (8.3, 0.9), (9.0, 0.9), (9.1, 0)], CYCLE)}
    <animateTransform attributeName="transform" type="translate"
                      values="0 0;0 0;1260 0;1260 0" keyTimes="0;{kf(8.2, CYCLE)};{kf(9.1, CYCLE)};1"
                      dur="{CYCLE}s" repeatCount="indefinite"/>
  </rect>

  <!-- the name, wiped in -->
  <g clip-path="url(#ecWipe)">
    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{SANS}" font-size="72"
          font-weight="300" letter-spacing="8" fill="url(#ecName)">
      <animate attributeName="opacity" values="0;0;1;1;0;0"
               keyTimes="0;{kf(8.4, CYCLE)};{kf(8.7, CYCLE)};{kf(20.8, CYCLE)};{kf(21.3, CYCLE)};1"
               dur="{CYCLE}s" repeatCount="indefinite"/>MITALI CHINCHOLIKAR</text>
  </g>

  <rect x="{CX - 280}" y="{NAME_Y + 30}" width="560" height="1.3" fill="url(#ecRule)" opacity="0">
    {track("opacity", [(0, 0), (9.3, 0), (9.45, 1), (20.6, 1), (21.1, 0)], CYCLE)}
    {track("width", [(0, 0), (9.3, 0), (10.3, 560), (CYCLE, 560)], CYCLE)}
  </rect>

  <text x="{CX}" y="{NAME_Y + 68}" text-anchor="middle" font-family="{SANS}" font-size="19"
        font-style="italic" font-weight="300" fill="{CREAM}" opacity="0">
    {track("opacity", [(0, 0), (9.8, 0), (10.3, 1), (20.6, 1), (21.1, 0)], CYCLE)}
    I don't wait to be senior to build.</text>

  <!-- the queue, cascading -->
  <g>{chips(11.2)}</g>

  <!-- the stamp -->
  <g opacity="0">
    {track("opacity", [(0, 0), (13.0, 0), (13.4, 1), (20.4, 1), (21.0, 0)], CYCLE)}
    <rect x="46" y="{H - BAR - 78}" width="268" height="30" fill="none" stroke="{CHERRY}" stroke-opacity="0.55"/>
    <text x="62" y="{H - BAR - 58}" font-family="{MONO}" font-size="9.5" letter-spacing="2.6"
          fill="{CHERRY_L}">CHAPTER 001 · THE ECLIPSE</text>
  </g>
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Mitali Chincholikar — the eclipse">
  <defs>
    <radialGradient id="ecHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0.26"/>
      <stop offset="0.34" stop-color="{CHERRY}" stop-opacity="0.11"/>
      <stop offset="0.68" stop-color="{CHERRY}" stop-opacity="0.035"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="ecSky" cx="0.5" cy="0.42" r="0.62">
      <stop offset="0" stop-color="#180B16"/>
      <stop offset="0.55" stop-color="#0A0610"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <radialGradient id="ecSun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.42" stop-color="{ICE}"/>
      <stop offset="0.72" stop-color="{CORAL}"/>
      <stop offset="0.92" stop-color="{CHERRY_L}"/>
      <stop offset="1" stop-color="{CHERRY}"/>
    </radialGradient>
    <linearGradient id="ecCorona" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ICE}"/><stop offset="0.22" stop-color="{CORAL}"/>
      <stop offset="0.44" stop-color="{CHERRY_L}"/><stop offset="0.62" stop-color="{CORAL}"/>
      <stop offset="0.80" stop-color="{CELESTE}"/><stop offset="1" stop-color="{ICE}"/>
    </linearGradient>
    <linearGradient id="ecName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.52" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#AFA4B8"/>
    </linearGradient>
    <linearGradient id="ecRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CHERRY}" stop-opacity="0"/>
      <stop offset="0.2" stop-color="{CHERRY_L}" stop-opacity="0.7"/>
      <stop offset="0.5" stop-color="{ICE}" stop-opacity="0.9"/>
      <stop offset="0.8" stop-color="{CHERRY_L}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{CHERRY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ecSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CORAL}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{ICE}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="ecGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" stroke="#FFFFFF" stroke-opacity="0.013" stroke-width="1"/>
    </pattern>
    <clipPath id="ecFrame"><rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}"/></clipPath>
    <clipPath id="ecWipe">
      <rect x="0" y="0" width="0" height="{H}">
        {track("width", [(0, 0), (8.4, 0), (9.5, 1240), (21.2, 1240), (21.2, 0)], CYCLE)}
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g clip-path="url(#ecFrame)">
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}" fill="url(#ecSky)"/>
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR*2}" fill="url(#ecGrid)"/>
{poster}
{film}
  </g>
{hud("MITALI CHINCHOLIKAR", "CHAPTER 001 · THE ECLIPSE", "PUNE · MAHARASHTRA · INDIA",
     "CSE · FIRST YEAR · AI / ML FROM YEAR 2", "00:00:26", CHERRY_L, INK, ASH, DIM)}
  <g>{grain(W, H, 52)}</g>
  <g opacity="0.40">{scan(W, H)}</g>
</svg>
'''


if __name__ == "__main__":
    a = build_anuj()
    (HERE / "opening.svg").write_text(a, encoding="utf-8")
    print(f"opening.svg        {len(a):7d} b")

    m = build_mitali()
    (OUT / "opening.svg").write_text(m, encoding="utf-8")
    print(f"mitali/opening.svg {len(m):7d} b")
