#!/usr/bin/env python3
"""Both openings. One architecture, engineered for depth rather than noise.

DESIGN RULES
  · the mark is a tapered ribbon, not a uniform stroke — a spiral or a corona
    built from geometry that narrows, so it reads as drawn rather than plotted
  · no random-length hairlines. Every spike is a shaped triangle
  · the void is never flat black — it has a gradient, an inner rim glow and a
    lens flare crossing it
  · type is large and spaced; on GitHub the font is whatever the system has,
    so hierarchy has to come from size and tracking, never from the family
  · deep blacks, high contrast, saturated light. Muddiness is the enemy

LAYERS
  1  poster   always painted, never animates, never leaves
  2  scrim    dark cloth that drops over it
  3  film     the sequence, played on the cloth

Run: python3 build_film.py
"""
import math
import pathlib
import random

HERE = pathlib.Path(__file__).parent

W, H = 1200, 760
BAR = 44
CX = 600
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BLACK = "'Arial Black', 'Arial Bold', Impact, 'Helvetica Neue', sans-serif"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"


# ── machinery ───────────────────────────────────────────────────────────────
def track(attr, pairs, cycle, extra=""):
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


def grain(w, h, n=64):
    return "".join(
        f'<circle cx="{random.uniform(0, w):.0f}" cy="{random.uniform(0, h):.0f}" '
        f'r="{random.uniform(0.3, 0.9):.1f}" fill="#FFFFFF" fill-opacity="0.045">'
        f'<animate attributeName="fill-opacity" values="0.015;0.055;0.025;0.06;0.015" '
        f'dur="{random.uniform(1.1, 2.6):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(n)
    )


def scan(w, h, step=3):
    return "".join(
        f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#000000" stroke-opacity="0.15" '
        f'stroke-width="1"/>' for y in range(0, h, step)
    )


def tapered_spiral(cx, cy, r0, r1, turns, w0, w1, steps=260):
    """A spiral drawn as a filled ribbon that narrows to a point."""
    outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        wdt = (w0 + (w1 - w0) * t) / 2.0
        ca, sa = math.cos(th), math.sin(th)
        outer.append((cx + (r + wdt) * ca, cy + (r + wdt) * sa))
        inner.append((cx + (r - wdt) * ca, cy + (r - wdt) * sa))
    d = "M " + " L ".join("%.2f,%.2f" % p for p in outer)
    d += " L " + " L ".join("%.2f,%.2f" % p for p in reversed(inner))
    return d + " Z"


def spiral_centreline(cx, cy, r0, r1, turns, steps=300):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = 2 * math.pi * turns * t
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts)


WARM_PALE = {"#E8F6FC", "#A8DEF0", "#F6F0F4"}


def corona_spikes(cx, cy, r_in, r_out, n, colors, seed=7, weights=None, tilt=0.0):
    """Tapered blades, not hairlines. Each one a filled triangle with a curve.

    Blades pointing down are pulled short so the corona never scribbles over
    the name, and colours are weighted so one family dominates the ring.
    """
    rng = random.Random(seed)
    out = []
    for i in range(n):
        ang = 2 * math.pi * i / n - math.pi / 2
        ang += rng.uniform(-0.008, 0.008)
        length = r_out * rng.uniform(0.22, 0.62)
        length *= 1.0 - 0.80 * max(0.0, math.sin(ang)) ** 1.25
        half = rng.uniform(0.012, 0.034)
        col = (rng.choices(colors, weights=weights, k=1)[0]
               if weights else rng.choice(colors))
        o = rng.uniform(0.14, 0.44)
        if col in WARM_PALE:
            o *= 0.55
        a0, a1 = ang - half, ang + half
        tip_off = rng.uniform(-0.05, 0.05)
        p0 = (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0))
        p1 = (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1))
        pm = (cx + (r_in + length * 0.45) * math.cos(ang + tip_off * 0.4),
              cy + (r_in + length * 0.45) * math.sin(ang + tip_off * 0.4))
        p2 = (cx + (r_in + length) * math.cos(ang + tip_off),
              cy + (r_in + length) * math.sin(ang + tip_off))
        d = ("M %.2f,%.2f Q %.2f,%.2f %.2f,%.2f Q %.2f,%.2f %.2f,%.2f Z"
             % (p0[0], p0[1], pm[0], pm[1], p2[0], p2[1],
                pm[0], pm[1], p1[0], p1[1]))
        out.append(
            f'<path d="{d}" fill="{col}" fill-opacity="{o:.2f}">'
            f'<animate attributeName="fill-opacity" '
            f'values="{o:.2f};{o * 0.35:.2f};{o:.2f}" dur="{rng.uniform(2.8, 6.4):.1f}s" '
            f'begin="{rng.uniform(0, 3):.1f}s" repeatCount="indefinite"/></path>')
    return "".join(out)


def anamorphic(cy, w, spread=560, color="#FFFFFF", op=0.5):
    """The horizontal streak that makes a frame look shot rather than drawn."""
    return (f'<rect x="{(1200 - w) / 2}" y="{cy - 1.2}" width="{w}" height="2.4" '
            f'fill="url(#flareH)" opacity="{op}"/>'
            f'<rect x="{(1200 - w * 0.55) / 2}" y="{cy - 3.5}" width="{w * 0.55}" '
            f'height="7" fill="url(#flareH)" opacity="{op * 0.45}"/>'
            f'<circle cx="{CX}" cy="{cy}" r="{spread * 0.055:.0f}" fill="url(#flareCore)" '
            f'opacity="{op * 0.9}"/>')


def brackets(inset=14, arm=22, color="#FFFFFF", op=0.16):
    """Four corner marks. The cheapest way to make a frame look framed."""
    x0, y0 = inset, BAR + inset
    x1, y1 = W - inset, H - BAR - inset
    return "".join([
        f'<path d="M {x0},{y0+arm} L {x0},{y0} L {x0+arm},{y0}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"/>',
        f'<path d="M {x1-arm},{y0} L {x1},{y0} L {x1},{y0+arm}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"/>',
        f'<path d="M {x0},{y1-arm} L {x0},{y1} L {x0+arm},{y1}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"/>',
        f'<path d="M {x1-arm},{y1} L {x1},{y1} L {x1},{y1-arm}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"/>',
    ])


def light_arcs(cx, cy, radii, color, op=0.34):
    """Long-exposure trails — arcs that never quite close."""
    out = []
    for r, start, sweep, o in radii:
        end = start + sweep
        large = 1 if sweep > 180 else 0
        sx = cx + r * math.cos(math.radians(start))
        sy = cy + r * math.sin(math.radians(start))
        ex = cx + r * math.cos(math.radians(end))
        ey = cy + r * math.sin(math.radians(end))
        out.append(
            f'<path d="M {sx:.1f},{sy:.1f} A {r},{r} 0 {large} 1 {ex:.1f},{ey:.1f}" '
            f'fill="none" stroke="{color}" stroke-opacity="{o*op:.3f}" stroke-width="1.1" '
            f'stroke-linecap="round"/>')
    return "".join(out)


def vignette(w, h):
    return f'<rect width="{w}" height="{h}" fill="url(#vign)"/>'


def hud(left_top, right_top, left_bot, mid_bot, right_bot, rec, ash, dim):
    return f'''
  <rect x="0" y="0" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{H - BAR}" width="{W}" height="{BAR}" fill="#000000"/>
  <rect x="0" y="{BAR}" width="{W}" height="1" fill="{rec}" fill-opacity="0.30"/>
  <rect x="0" y="{H - BAR - 1}" width="{W}" height="1" fill="{rec}" fill-opacity="0.30"/>
  <text x="28" y="27" font-family="{MONO}" font-size="8.5" letter-spacing="3.8" fill="{ash}">{left_top}</text>
  <text x="{W - 28}" y="27" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.4" fill="{ash}" fill-opacity="0.72">{right_top}</text>
  <text x="28" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5" letter-spacing="3.2"
        fill="{dim}">{left_bot}</text>
  <text x="{CX}" y="{H - BAR + 28}" text-anchor="middle" font-family="{MONO}" font-size="8.5"
        letter-spacing="3.2" fill="{dim}" fill-opacity="0.88">{mid_bot}</text>
  <circle cx="{W - 118}" cy="{H - BAR + 25}" r="3" fill="{rec}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 106}" y="{H - BAR + 28}" font-family="{MONO}" font-size="8.5"
        letter-spacing="2.4" fill="{ash}">REC</text>
  <text x="{W - 28}" y="{H - BAR + 28}" text-anchor="end" font-family="{MONO}" font-size="8.5"
        letter-spacing="1.8" fill="{ash}" fill-opacity="0.8">{right_bot}</text>
'''


def shared_defs(prefix, sky_hi, ink, rec, ice):
    return f'''
    <radialGradient id="{prefix}Sky" cx="0.5" cy="0.40" r="0.70">
      <stop offset="0" stop-color="{sky_hi}"/>
      <stop offset="0.48" stop-color="{ink}"/>
      <stop offset="1" stop-color="#000000"/>
    </radialGradient>
    <radialGradient id="{prefix}Void" cx="0.42" cy="0.36" r="0.72">
      <stop offset="0" stop-color="#120A14"/>
      <stop offset="0.55" stop-color="#07050B"/>
      <stop offset="1" stop-color="#010003"/>
    </radialGradient>
    <linearGradient id="flareH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{rec}" stop-opacity="0"/>
      <stop offset="0.30" stop-color="{ice}" stop-opacity="0.10"/>
      <stop offset="0.5" stop-color="{ice}" stop-opacity="0.85"/>
      <stop offset="0.70" stop-color="{ice}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{rec}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="flareCore" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ice}" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="{rec}" stop-opacity="0.14"/>
      <stop offset="1" stop-color="{rec}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vign" cx="0.5" cy="0.46" r="0.78">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.62" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>
    <pattern id="{prefix}Grid" width="44" height="44" patternUnits="userSpaceOnUse">
      <path d="M44 0H0V44" stroke="#FFFFFF" stroke-opacity="0.012" stroke-width="1"/>
    </pattern>
    <clipPath id="{prefix}Frame">
      <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}"/>
    </clipPath>'''


# ══════════════════════════════════════════════════════════════════════════
#  ANUJ · THE SEAL
# ══════════════════════════════════════════════════════════════════════════
def build_anuj():
    INK, CREAM, ASH, DIM = "#07060A", "#F2E8D5", "#9A90A4", "#5E5669"
    VERM, VERM_L, VERM_D, CHAKRA = "#C1272D", "#F2544B", "#7A1219", "#4FB3D9"

    CYCLE = 26.0
    MARK_CY, R = 316, 134
    NAME_Y, RULE_Y, CHIP_Y = 528, 560, 636

    # local space — the group already translates to (CX, MARK_CY)
    ribbon = tapered_spiral(0, 0, 10, R - 16, 2.7, 13.0, 1.2)
    core_line = spiral_centreline(0, 0, 10, R - 16, 2.7)

    ticks = []
    for i in range(96):
        ang = 2 * math.pi * i / 96 - math.pi / 2
        major = i % 8 == 0
        r0 = R + 16
        r1 = R + (34 if major else 24)
        ticks.append(
            f'<line x1="{r0*math.cos(ang):.1f}" y1="{r0*math.sin(ang):.1f}" '
            f'x2="{r1*math.cos(ang):.1f}" y2="{r1*math.sin(ang):.1f}" '
            f'stroke="{VERM_L if major else VERM}" stroke-opacity="{0.6 if major else 0.22}" '
            f'stroke-width="{1.4 if major else 0.7}"/>')
    ticks = "".join(ticks)

    PROJ = [("VERDE PORTFOLIO", VERM_L), ("VERDE APP", VERM_L),
            ("NIRMAAN APP", VERM_L), ("NIRMAN PORTFOLIO", VERM_L),
            ("SKILL-VERSE", VERM_L), ("RESONATE", VERM_L),
            ("RAKSHABANDHAN", VERM_L), ("VERDE PREVIOUS", VERM_L)]
    NUM = CHAKRA
    CWD, GAPD = 130, 10
    x0 = CX - (len(PROJ) * CWD + (len(PROJ) - 1) * GAPD) / 2

    def chips(t0=None):
        out = []
        for i, (name, col) in enumerate(PROJ):
            cx = x0 + i * (CWD + GAPD)
            begin = f' begin="{t0 + i * 0.10:.2f}s"' if t0 is not None else ""
            out.append(
                f'<g>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="{CWD}" height="34" rx="2" '
                f'fill="{col}" fill-opacity="0.05" stroke="{col}" stroke-opacity="0.26"/>'
                f'<rect x="{cx:.1f}" y="{CHIP_Y}" width="2.2" height="34" fill="{col}">'
                f'<animate attributeName="fill-opacity" values="0.55;1;0.55" dur="4.4s"{begin} repeatCount="indefinite"/></rect>'
                f'<text x="{cx + 14:.1f}" y="{CHIP_Y + 21}" font-family="{MONO}" font-size="7.4" '
                f'letter-spacing="0.8" fill="{CREAM}" fill-opacity="0.88">{name}</text>'
                f'<text x="{cx + CWD - 9:.1f}" y="{CHIP_Y + 21}" text-anchor="end" font-family="{MONO}" '
                f'font-size="6.4" fill="{NUM}" fill-opacity="0.62">0{i+1}</text>'
                f'</g>')
        return "".join(out)

    mark = f'''
    <circle cx="{CX}" cy="{MARK_CY}" r="{R + 118}" fill="url(#saHalo)"/>
    <g>
      {light_arcs(CX, MARK_CY, [(R + 62, 200, 108, 0.9), (R + 92, 24, 92, 0.6),
                                (R + 150, 140, 64, 0.35)], VERM_L)}
      <animateTransform attributeName="transform" type="rotate" from="0 {CX} {MARK_CY}"
                        to="360 {CX} {MARK_CY}" dur="170s" repeatCount="indefinite"/>
    </g>
    <g clip-path="url(#saFlareClip)">
      {anamorphic(MARK_CY, 780, color=VERM_L, op=0.28)}
    </g>
    <g transform="translate({CX},{MARK_CY})">
      <g opacity="0.85">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="240s" repeatCount="indefinite"/>
        {ticks}
      </g>
      <circle r="{R + 4}" fill="url(#saRimGlow)" opacity="0.85"/>
      <circle r="{R}" fill="url(#saVoid)"/>
      <circle r="{R + 1.5}" fill="none" stroke="url(#saRing)" stroke-width="2.4"/>
      <circle r="{R - 7}" fill="none" stroke="{VERM_L}" stroke-opacity="0.13" stroke-width="5"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                          dur="90s" repeatCount="indefinite"/>
        <path d="{ribbon}" fill="url(#saRibbon)"/>
        <path d="{core_line}" fill="none" stroke="{CREAM}" stroke-opacity="0.14" stroke-width="0.9"/>
      </g>
      <circle r="6.5" fill="#FFFDF6">
        <animate attributeName="r" values="5.5;8;5.5" dur="4.2s" repeatCount="indefinite"/>
      </circle>
      <circle r="20" fill="{VERM_L}" fill-opacity="0.14"/>
    </g>'''

    poster = f'''
  <!-- ══ LAYER 1 · THE POSTER ═══════════════════════════════════════════ -->
  <g>
    {mark}

    <text x="{CX}" y="96" text-anchor="middle" font-family="{MONO}" font-size="9.5"
          letter-spacing="8" fill="{ASH}">CHAPTER 001</text>

    <text x="{CX}" y="{NAME_Y}" text-anchor="middle" font-family="{BLACK}" font-size="88"
          letter-spacing="3" fill="url(#saName)">ANUJ PHULERA</text>

    <rect x="{CX - 268}" y="{RULE_Y}" width="536" height="1.4" fill="url(#saRule)"/>

    <text x="{CX}" y="{RULE_Y + 34}" text-anchor="middle" font-family="{MONO}" font-size="15.5"
          letter-spacing="0.6" fill="{CREAM}" fill-opacity="0.94">I don't chase attention.</text>
    <text x="{CX}" y="{RULE_Y + 59}" text-anchor="middle" font-family="{MONO}" font-size="15.5"
          letter-spacing="0.6" fill="{VERM_L}">I build things that command it.</text>

    {chips()}

    <text x="{CX}" y="{CHIP_Y + 50}" text-anchor="middle" font-family="{MONO}" font-size="8"
          letter-spacing="4" fill="{DIM}">EIGHT SEALS · ONE HAND</text>

  </g>'''

    film = f'''
  <!-- ══ THE FILM · accents only, never a scrim ══════════════════════════
       Every frame stays composed: the mark, the name, the rule, the claim and
       the eight chips are present from t=0 to t=26. The timeline adds light,
       never removes the picture. -->

  <!-- ignition: a ring of light escaping the mark -->
  <g transform="translate({CX},{MARK_CY})" opacity="0">
    {track("opacity", [(0, 0), (0.9, 0), (1.15, 0.95), (2.3, 0)], CYCLE)}
    <circle r="{R}" fill="none" stroke="{VERM_L}" stroke-width="3"
            stroke-dasharray="{2*math.pi*R:.1f}">
      {track("r", [(0, R * 0.35), (1.15, R), (2.3, R + 180)], CYCLE)}
      {track("stroke-width", [(0, 14), (1.15, 4), (2.3, 0.6)], CYCLE)}
      {track("stroke-dasharray", [(0, "2 6"), (2.3, "0.4 22")], CYCLE)}
    </circle>
  </g>

  <!-- the rim breathes brighter than the poster's baseline -->
  <g transform="translate({CX},{MARK_CY})" opacity="0">
    {track("opacity", [(0, 0), (1.0, 0), (1.6, 1), (3.4, 0.55), (5.0, 0.9),
                       (7.0, 0.4), (9.0, 0.85), (21.0, 0.5), (22.0, 0.2), (CYCLE, 0.0)], CYCLE)}
    <circle r="{R + 5}" fill="none" stroke="url(#saRing)" stroke-width="5" stroke-opacity="0.45"/>
    <circle r="{R + 16}" fill="none" stroke="{VERM_L}" stroke-width="16" stroke-opacity="0.10"/>
  </g>

  <!-- the spiral re-traces itself, once, as if re-inked -->
  <g transform="translate({CX},{MARK_CY})">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                        dur="90s" repeatCount="indefinite"/>
      <path d="{ribbon}" fill="none" stroke="#FFB4A6" stroke-width="2.4"
            stroke-opacity="0" stroke-linecap="round"
            stroke-dasharray="{2*math.pi*(R-16)*2.7:.0f}">
        {track("stroke-opacity", [(0, 0), (2.6, 0), (2.9, 0.85), (5.2, 0.0), (CYCLE, 0)], CYCLE)}
      </path>
    </g>
  </g>

  <!-- the core ignites, then settles -->
  <circle cx="{CX}" cy="{MARK_CY}" r="6.5" fill="#FFFDF6" opacity="0">
    {track("opacity", [(0, 0), (1.1, 0), (1.6, 1), (2.6, 0.35), (CYCLE, 0)], CYCLE)}
    {track("r", [(0, 0), (1.1, 0), (1.5, 30), (1.9, 9), (2.6, 0), (CYCLE, 0)], CYCLE)}
  </circle>

  <!-- a light crosses the name once per loop -->
  <ellipse cx="-210" cy="{NAME_Y - 40}" rx="160" ry="104" fill="url(#saSweep)">
    <animateTransform attributeName="transform" type="translate"
                      values="0 0;0 0;1720 0;1720 0" keyTimes="0;0.34;0.52;1"
                      dur="{CYCLE}s" repeatCount="indefinite"/>
  </ellipse>

  <!-- the rule strikes, left to right, at t=9 -->
  <rect x="{CX - 268}" y="{RULE_Y - 1.2}" width="536" height="3.4" fill="url(#saRule)" opacity="0">
    {track("opacity", [(0, 0), (8.9, 0), (9.0, 0.9), (9.6, 0), (CYCLE, 0)], CYCLE)}
    <animateTransform attributeName="transform" type="scale"
                      values="0 1;0 1;1 1;1 1"
                      keyTimes="0;{kf(8.9, CYCLE)};{kf(9.6, CYCLE)};1"
                      dur="{CYCLE}s" repeatCount="indefinite" additive="sum"
                      transform-origin="{CX} {RULE_Y}"/>
  </rect>

  <!-- the stamp -->
  <g opacity="0">
    {track("opacity", [(0, 0), (12.6, 0), (13.1, 1), (20.6, 1), (21.4, 0)], CYCLE)}
    <rect x="46" y="{H - BAR - 86}" width="276" height="32" fill="none" stroke="{VERM}" stroke-opacity="0.55"/>
    <text x="62" y="{H - BAR - 65}" font-family="{MONO}" font-size="9.5" letter-spacing="2.8"
          fill="{VERM_L}">CHAPTER 001 · THE SEAL</text>
  </g>
'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — the seal">
  <defs>
    {shared_defs("sa", "#1A0A10", INK, VERM, CREAM)}
    <radialGradient id="saHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.34"/>
      <stop offset="0.38" stop-color="{VERM_D}" stop-opacity="0.22"/>
      <stop offset="0.70" stop-color="{VERM}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="saRimGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0.84" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.97" stop-color="{VERM_L}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{VERM_L}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="saRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF8A7A"/>
      <stop offset="0.28" stop-color="{VERM_L}"/>
      <stop offset="0.52" stop-color="{VERM}"/>
      <stop offset="0.74" stop-color="{VERM_L}"/>
      <stop offset="0.88" stop-color="{CHAKRA}"/>
      <stop offset="1" stop-color="#FF8A7A"/>
    </linearGradient>
    <linearGradient id="saRibbon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF7C6E"/>
      <stop offset="0.35" stop-color="{VERM_L}"/>
      <stop offset="0.70" stop-color="{VERM}"/>
      <stop offset="1" stop-color="#FF9C8E"/>
    </linearGradient>
    <linearGradient id="saName" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.48" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#A99C82"/>
    </linearGradient>
    <linearGradient id="saRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.16" stop-color="{VERM_L}" stop-opacity="0.9"/>
      <stop offset="0.5" stop-color="{CREAM}" stop-opacity="0.95"/>
      <stop offset="0.84" stop-color="{VERM_L}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="saSweep" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{CREAM}" stop-opacity="0.22"/>
      <stop offset="0.40" stop-color="{VERM_L}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{VERM_L}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="saSweep2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFD8CE" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="saFlareClip">
      <circle cx="{CX}" cy="{MARK_CY}" r="{R + 116}"/>
    </clipPath>
    <clipPath id="saWipe">
      <rect x="0" y="0" width="0" height="{H}">
        {track("width", [(0, 0), (7.4, 0), (8.6, 1250), (21.6, 1250), (21.6, 0)], CYCLE)}
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="#000000"/>
  <g clip-path="url(#saFrame)">
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#saSky)"/>
    <rect x="0" y="{BAR}" width="{W}" height="{H - BAR * 2}" fill="url(#saGrid)"/>
{poster}
{film}
    {vignette(W, H)}
    {brackets(14, 22, CREAM, 0.22)}
  </g>
{hud("SEALING CORPS", "CHAPTER 001 · THE SEAL", "GURUGRAM · HARYANA · INDIA",
     "GENIN · CLASS 10 · INTERFACE SYSTEMS", "00:00:26", VERM_L, ASH, DIM)}
  <g>{grain(W, H, 60)}</g>
  <g opacity="0.38">{scan(W, H)}</g>
</svg>
'''


if __name__ == "__main__":
    a = build_anuj()
    (HERE / "opening.svg").write_text(a, encoding="utf-8")
    print(f"opening.svg  {len(a):7d} b")
