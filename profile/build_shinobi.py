#!/usr/bin/env python3
"""The shinobi identity - Uzumaki spiral and sealing formula.

Deliberately NOT the Sharingan. This is a different clan language:
a vermilion spiral, a seal ring with tick marks, kunai, chakra motes.

Run: python3 build_shinobi.py
Out: banner.svg emblem.svg divider.svg typing.svg registry.svg stats.svg
"""
import math
import pathlib
import random

random.seed(11)

# ── palette ─────────────────────────────────────────────────────────────────
INK    = "#07060A"
PAPER  = "#0C0A10"
VERM   = "#C1272D"   # Uzumaki vermilion
VERM_D = "#7A1219"
VERM_L = "#E8453F"
CREAM  = "#F2E8D5"
SAND   = "#C9BBA3"
ASH    = "#8A8090"
DIM    = "#5A5264"
CHAKRA = "#4FB3D9"   # chakra blue
CHAKRA_D = "#1E5F75"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"

HERE = pathlib.Path(__file__).parent


# ── geometry ────────────────────────────────────────────────────────────────
def spiral(cx, cy, r0, r1, turns, steps=300, phase=0.0):
    """Archimedean spiral as an open polyline."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        th = phase + 2 * math.pi * turns * t
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return "M " + " L ".join("%.1f,%.1f" % p for p in pts)


def kunai(cx, cy, s=1.0, fill=CREAM, opacity=1.0, rot=0.0):
    """Kunai pointing up: diamond blade, wrapped grip, ring pommel."""
    return (
        f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s})" opacity="{opacity}">'
        f'<path d="M 0,-34 L 7,-10 L 4,2 L -4,2 L -7,-10 Z" fill="{fill}"/>'
        f'<rect x="-3" y="2" width="6" height="26" rx="1.6" fill="{fill}" fill-opacity="0.85"/>'
        f'<circle cx="0" cy="32" r="5.5" fill="none" stroke="{fill}" stroke-width="2.6"/>'
        f'</g>'
    )


def chakra_motes(n=26, w=1200, h=340, colour=CHAKRA):
    out = []
    for _ in range(n):
        x = random.uniform(10, w - 10)
        r = random.uniform(0.7, 2.0)
        dur = random.uniform(8, 17)
        begin = random.uniform(0, 14)
        drift = random.uniform(-40, 40)
        col = colour if random.random() > 0.3 else CREAM
        out.append(
            f'<circle cx="{x:.1f}" cy="{h + 8}" r="{r:.1f}" fill="{col}" opacity="0">'
            f'<animate attributeName="cy" values="{h + 8};-24" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{x:.1f};{x + drift:.1f}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.8;0.45;0" keyTimes="0;0.2;0.68;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "".join(out)


def seal_ring(cx, cy, R, ticks=48, colour=VERM, spin="60s", op=0.5):
    """A talisman ring: circles plus tick marks, rotating slowly.

    Drawn in LOCAL space (origin at the centre) and positioned by an outer
    translate, so the inner rotation group spins about its own zero and never
    fights an absolute-coordinate transform.
    """
    t = []
    for i in range(ticks):
        a = 2 * math.pi * i / ticks
        long = (i % 4 == 0)
        r1 = R * (0.88 if long else 0.93)
        r2 = R * 0.995
        t.append(
            f'<line x1="{r1 * math.cos(a):.2f}" y1="{r1 * math.sin(a):.2f}" '
            f'x2="{r2 * math.cos(a):.2f}" y2="{r2 * math.sin(a):.2f}" '
            f'stroke="{colour}" stroke-width="{1.4 if long else 0.7}" stroke-opacity="{op if long else op * 0.55:.2f}"/>'
        )
    return (
        f'<g transform="translate({cx},{cy})">'
        f'<g opacity="{min(1.0, op * 2.1):.2f}">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="{spin}" repeatCount="indefinite"/>'
        f'<circle cx="0" cy="0" r="{R * 0.999:.1f}" fill="none" stroke="{colour}" stroke-width="1" stroke-opacity="0.55"/>'
        f'<circle cx="0" cy="0" r="{R * 0.80:.1f}" fill="none" stroke="{colour}" stroke-width="0.8" stroke-opacity="0.28"/>'
        + "".join(t) +
        '</g></g>'
    )


def emblem(cx, cy, R, colour=VERM, dur="24s", turns=2.6, width=None, op=1.0, glow=True):
    """The Uzumaki spiral, slowly turning. translate outer, rotate inner."""
    sw = width if width is not None else max(1.2, R * 0.13)
    d = spiral(0, 0, R * 0.17, R * 0.82, turns)
    g = (f'<circle cx="{cx}" cy="{cy}" r="{R * 1.35:.1f}" fill="url(#chakraGlow)" opacity="0.55"/>' if glow else "")
    return f'''{g}
  <g transform="translate({cx},{cy})" opacity="{op}">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="{dur}" repeatCount="indefinite"/>
      <path d="{d}" fill="none" stroke="{colour}" stroke-width="{sw:.2f}" stroke-linecap="round"/>
    </g>
  </g>
  <circle cx="{cx}" cy="{cy}" r="{R * 1.02:.1f}" fill="none" stroke="{colour}" stroke-width="1" stroke-opacity="0.30"/>'''


DEFS = f'''
  <defs>
    <radialGradient id="chakraGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.42"/>
      <stop offset="0.45" stop-color="{VERM}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="paperGlow" cx="0.78" cy="0.46" r="0.64">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.20"/>
      <stop offset="0.5" stop-color="{VERM_D}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blueWash" cx="0.08" cy="0.98" r="0.55">
      <stop offset="0" stop-color="{CHAKRA}" stop-opacity="0.11"/>
      <stop offset="1" stop-color="{CHAKRA}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ruleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.9"/>
      <stop offset="0.5" stop-color="{CHAKRA}" stop-opacity="0.45"/>
      <stop offset="1" stop-color="{VERM}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="nameGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFF9EE"/>
      <stop offset="0.6" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="#C4B49B"/>
    </linearGradient>
    <pattern id="gridFine" width="46" height="46" patternUnits="userSpaceOnUse">
      <path d="M46 0H0V46" stroke="#FFFFFF" stroke-opacity="0.020" stroke-width="1"/>
    </pattern>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#121017"/>
      <stop offset="0.55" stop-color="#0A080D"/>
      <stop offset="1" stop-color="#100C12"/>
    </linearGradient>
    <pattern id="grain" width="3" height="3" patternUnits="userSpaceOnUse">
      <circle cx="0.5" cy="0.5" r="0.45" fill="#FFFFFF" fill-opacity="0.030"/>
      <circle cx="2.1" cy="1.7" r="0.4" fill="#FFFFFF" fill-opacity="0.018"/>
    </pattern>
  </defs>'''


# ── banner ──────────────────────────────────────────────────────────────────
W, H = 1200, 340
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera">
{DEFS}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#gridFine)"/>
  <rect width="{W}" height="{H}" fill="url(#paperGlow)"/>
  <rect width="{W}" height="{H}" fill="url(#blueWash)"/>

  {seal_ring(966, 168, 132, ticks=52, op=0.42, spin="70s")}
  {emblem(966, 168, 96, turns=2.7, width=13, dur="26s")}

  {chakra_motes(26, W, H)}
  {kunai(1140, 246, s=0.62, opacity=0.16, rot=18)}
  {kunai(846, 84, s=0.44, opacity=0.12, rot=-24)}

  <rect x="0" y="0" width="3" height="{H}" fill="{VERM}" fill-opacity="0.8"/>

  <text x="72" y="88" font-family="{MONO}" font-size="11.5" letter-spacing="4.6" fill="{ASH}">SEALING CORPS · INTERFACE ENGINEER</text>

  <text x="70" y="164" font-family="{BLACK}" font-size="57" letter-spacing="1.1" fill="url(#nameGrad)" filter="url(#softGlow)">ANUJ PHULERA</text>

  <rect x="72" y="190" width="452" height="1.5" fill="url(#ruleGrad)"/>

  <text x="72" y="228" font-family="{MONO}" font-size="13.5" letter-spacing="1.1" fill="{CREAM}" opacity="0.94">I don't chase attention.</text>
  <text x="72" y="251" font-family="{MONO}" font-size="13.5" letter-spacing="1.1" fill="{VERM_L}">I build things that command it.</text>

  <text x="72" y="288" font-family="{MONO}" font-size="10" letter-spacing="2.5" fill="{DIM}">DEEP FIELD · VERDE · NIRMAAN · RESONATE</text>

  <text x="72" y="316" font-family="{MONO}" font-size="8.5" letter-spacing="3" fill="{CHAKRA_D}">JAIPUR · INDIA</text>
</svg>
'''


# ── emblem (standalone) ─────────────────────────────────────────────────────
E = 360
emblem_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{E}" height="{E}" viewBox="0 0 {E} {E}" fill="none" role="img" aria-label="Uzumaki spiral">
{DEFS}
  {seal_ring(E / 2, E / 2, 128, ticks=44, op=0.30, spin="80s")}
  {emblem(E / 2, E / 2, 92, turns=2.7, width=12.5, dur="26s")}
</svg>
'''


# ── divider ─────────────────────────────────────────────────────────────────
DW, DH = 1200, 64
divider = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}" fill="none" role="img" aria-label="divider">
{DEFS}
  <line x1="30" y1="32" x2="{DW / 2 - 34:.0f}" y2="32" stroke="{VERM}" stroke-opacity="0.50" stroke-width="1.2"/>
  <line x1="{DW / 2 + 34:.0f}" y1="32" x2="{DW - 30}" y2="32" stroke="{VERM}" stroke-opacity="0.50" stroke-width="1.2"/>
  <line x1="30" y1="32" x2="{DW / 2 - 34:.0f}" y2="32" stroke="{CHAKRA}" stroke-opacity="0.14" stroke-width="3"/>
  <line x1="{DW / 2 + 34:.0f}" y1="32" x2="{DW - 30}" y2="32" stroke="{CHAKRA}" stroke-opacity="0.14" stroke-width="3"/>
  <circle cx="{DW / 2 - 40:.0f}" cy="32" r="1.8" fill="{VERM}"/>
  <circle cx="{DW / 2 + 40:.0f}" cy="32" r="1.8" fill="{VERM}"/>
  {emblem(DW / 2, 32, 15, turns=2.2, width=2.4, dur="18s", glow=False)}
</svg>
'''


# ── typing ──────────────────────────────────────────────────────────────────
TW, TH = 760, 50
TEXT = "I don't chase attention. I build things that command it."
adv = 13.6 * 0.60
tw = len(TEXT) * adv
typing = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" fill="none" role="img" aria-label="{TEXT}">
  <defs>
    <clipPath id="reveal"><rect x="0" y="0" width="0" height="{TH}">
      <animate attributeName="width" from="0" to="{tw + 6:.0f}" dur="2.6s" begin="0.4s" fill="freeze"/>
    </rect></clipPath>
  </defs>
  <text x="{TW / 2 - tw / 2:.0f}" y="33" font-family="{MONO}" font-size="13.6" letter-spacing="0.9"
        fill="{CREAM}" clip-path="url(#reveal)">{TEXT.replace("'", "&#39;")}</text>
  <rect x="{TW / 2 - tw / 2:.0f}" y="18" width="7" height="18" fill="{VERM_L}" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.95;1;1" dur="1s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


# ── registry card ───────────────────────────────────────────────────────────
RW, RH = 860, 300
rows = [
    ("ORIGIN",     "JAIPUR, INDIA",           CREAM),
    ("VILLAGE",    "INDEPENDENT",             CREAM),
    ("SPECIALITY", "INTERFACE SYSTEMS",       VERM_L),
    ("NATURE",     "TYPE · REACT · ESP32",    CREAM),
    ("STATUS",     "ACTIVE",                  "#7BE38B"),
]
row_svg = []
y = 168
for label, value, col in rows:
    row_svg.append(f'<text x="248" y="{y}" font-family="{MONO}" font-size="10.5" fill="{ASH}">{label}</text>')
    row_svg.append(f'<text x="400" y="{y}" font-family="{MONO}" font-size="10.5" fill="{col}">{value}</text>')
    row_svg.append(f'<line x1="248" y1="{y + 8}" x2="{RW - 40}" y2="{y + 8}" stroke="{DIM}" stroke-opacity="0.22" stroke-width="0.8"/>')
    y += 24

registry = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{RW}" height="{RH}" viewBox="0 0 {RW} {RH}" fill="none" role="img" aria-label="Shinobi registration">
{DEFS}
  <rect width="{RW}" height="{RH}" rx="10" fill="url(#cardGrad)"/>
  <rect width="{RW}" height="{RH}" rx="10" fill="url(#grain)"/>
  <rect x="0.75" y="0.75" width="{RW - 1.5}" height="{RH - 1.5}" rx="9.5" fill="none" stroke="{VERM}" stroke-opacity="0.34" stroke-width="1.5"/>
  <rect x="6.75" y="6.75" width="{RW - 13.5}" height="{RH - 13.5}" rx="6" fill="none" stroke="{VERM}" stroke-opacity="0.10" stroke-width="1"/>
  <rect x="0" y="0" width="5" height="{RH}" fill="{VERM}" fill-opacity="0.6"/>

  <text x="34" y="38" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{ASH}">SHINOBI REGISTRATION · SEALED</text>
  <text x="{RW - 34}" y="38" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{VERM_L}" text-anchor="end">NO. 001</text>
  <line x1="34" y1="52" x2="{RW - 34}" y2="52" stroke="{VERM}" stroke-opacity="0.28"/>

  <rect x="34" y="72" width="176" height="176" rx="6" fill="#0A080D" stroke="{VERM}" stroke-opacity="0.32"/>
  {seal_ring(122, 160, 68, ticks=28, op=0.24, spin="60s")}
  {emblem(122, 160, 52, turns=2.6, width=7.4, dur="22s")}

  <text x="248" y="88" font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{ASH}">DESIGNATION</text>
  <text x="246" y="126" font-family="{BLACK}" font-size="34" letter-spacing="0.8" fill="{CREAM}">ANUJ PHULERA</text>
  <line x1="248" y1="142" x2="{RW - 40}" y2="142" stroke="{VERM}" stroke-opacity="0.35"/>

  {''.join(row_svg)}

  <text x="248" y="288" font-family="{MONO}" font-size="9" letter-spacing="2.4" fill="{DIM}">SEAL INTACT · NOT FOR SALE</text>
</svg>
'''


# ── stats ───────────────────────────────────────────────────────────────────
SW_, SH_ = 1000, 396
BARS = [
    ("INTERFACE SYSTEMS", 96, VERM_L),
    ("BEHAVIOURAL ENGINE", 92, "#D93A34"),
    ("FULL-STACK", 88, "#E4552F"),
    ("AI / LLM PIPELINES", 84, "#EC7A2E"),
    ("DESIGN / MOTION", 90, "#F0993A"),
    ("HARDWARE / IoT", 78, "#E9B04A"),
]
BX, BW = 268, 470
Y0, GAP = 138, 40


def bar(i, label, val, col):
    y = Y0 + i * GAP
    w = BW * val / 100.0
    d = 0.35 + i * 0.13
    return f'''
  <g>
    <text x="62" y="{y + 5}" font-family="{MONO}" font-size="10.5" letter-spacing="2.1" fill="{ASH}">{label}</text>
    <rect x="{BX}" y="{y - 7}" width="{BW}" height="9" rx="4.5" fill="#FFFFFF" fill-opacity="0.05"/>
    <rect x="{BX}" y="{y - 7}" width="0" height="9" rx="4.5" fill="{col}" fill-opacity="0.92">
      <animate attributeName="width" from="0" to="{w:.0f}" dur="1.2s" begin="{d:.2f}s" fill="freeze"
               calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1"/>
    </rect>
    <text x="{BX + BW + 18}" y="{y + 5}" font-family="{MONO}" font-size="10.5" fill="{CREAM}" opacity="0">
      {val}<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{d + 0.85:.2f}s" fill="freeze"/>
    </text>
  </g>'''


stats = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SW_}" height="{SH_}" viewBox="0 0 {SW_} {SH_}" fill="none" role="img" aria-label="Attribute sheet">
{DEFS}
  <rect width="{SW_}" height="{SH_}" rx="10" fill="url(#cardGrad)"/>
  <rect width="{SW_}" height="{SH_}" rx="10" fill="url(#grain)"/>
  <rect x="0.75" y="0.75" width="{SW_ - 1.5}" height="{SH_ - 1.5}" rx="9.5" fill="none" stroke="{VERM}" stroke-opacity="0.32" stroke-width="1.5"/>
  <rect x="0" y="0" width="5" height="{SH_}" fill="{VERM}" fill-opacity="0.55"/>

  <text x="34" y="40" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{ASH}">ATTRIBUTE SHEET · SEALING CORPS</text>
  <text x="{SW_ - 34}" y="40" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{VERM_L}" text-anchor="end">UNIT 001</text>
  <line x1="34" y1="56" x2="{SW_ - 34}" y2="56" stroke="{VERM}" stroke-opacity="0.26"/>

  {seal_ring(888, 206, 74, ticks=30, op=0.22, spin="64s")}
  {emblem(888, 206, 54, turns=2.6, width=7.6, dur="23s")}
  <text x="888" y="318" font-family="{BLACK}" font-size="16" letter-spacing="2.6" fill="{CREAM}" text-anchor="middle">JONIN</text>
  <text x="888" y="336" font-family="{MONO}" font-size="8.5" letter-spacing="2.2" fill="{DIM}" text-anchor="middle">TWENTY TOOLS · ONE OBSESSION</text>

  {''.join(bar(i, *b) for i, b in enumerate(BARS))}

  <line x1="34" y1="{Y0 + len(BARS) * GAP + 4}" x2="{SW_ - 34}" y2="{Y0 + len(BARS) * GAP + 4}" stroke="{VERM}" stroke-opacity="0.18"/>
  <text x="34" y="{Y0 + len(BARS) * GAP + 30}" font-family="{MONO}" font-size="9" letter-spacing="2.6" fill="{DIM}">01 · INTERFACE ENGINEER · JAIPUR</text>
  <text x="{SW_ - 34}" y="{Y0 + len(BARS) * GAP + 30}" font-family="{MONO}" font-size="9" letter-spacing="2.6" fill="{DIM}" text-anchor="end">STATUS ACTIVE</text>
</svg>
'''


if __name__ == "__main__":
    for name, content in [
        ("banner.svg", banner),
        ("emblem.svg", emblem_svg),
        ("divider.svg", divider),
        ("typing.svg", typing),
        ("registry.svg", registry),
        ("stats.svg", stats),
    ]:
        (HERE / name).write_text(content, encoding="utf-8")
        print(f"wrote {name:14s} {len(content):6d} bytes")
