#!/usr/bin/env python3
"""Showcase grid: eight miniature UI mockups, one per project.

Instead of describing each repo in a sentence, draw it. Each card is a small
browser window with an abstract but project-specific interface inside, tinted
with that project's own accent colour.

Run: python3 build_showcase.py
Out: projects.svg
"""
import math
import pathlib

HERE = pathlib.Path(__file__).parent

INK    = "#07060A"
CARD   = "#0E0B11"
CARD2  = "#120F16"
CREAM  = "#F2E8D5"
ASH    = "#8A8090"
DIM    = "#4A4353"
VERM   = "#C1272D"
CHAKRA = "#4FB3D9"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# ── layout ──────────────────────────────────────────────────────────────────
COLS, ROWS = 4, 2
CW, CH = 280, 196
GX, GY = 20, 20
PAD = 10
W = COLS * CW + (COLS - 1) * GX + PAD * 2          # 1180
H = ROWS * CH + (ROWS - 1) * GY + PAD * 2 + 26     # 438 (26 for the caption)


def chrome(x, y, w, accent):
    """Browser top bar: three dots plus an address pill."""
    dots = "".join(
        f'<circle cx="{x + 14 + i * 9}" cy="{y + 11}" r="2.4" fill="{accent}" fill-opacity="0.55"/>'
        for i in range(3)
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="22" fill="#FFFFFF" fill-opacity="0.032"/>'
        f'<line x1="{x}" y1="{y + 22}" x2="{x + w}" y2="{y + 22}" stroke="#FFFFFF" stroke-opacity="0.06"/>'
        + dots +
        f'<rect x="{x + 44}" y="{y + 6}" width="{w - 58}" height="10" rx="5" fill="#FFFFFF" fill-opacity="0.04"/>'
    )


# ── per-project art ─────────────────────────────────────────────────────────
def art_verde_portfolio(x, y, w, h, a):
    """Circuit + 3D wireframe terrain."""
    g = []
    for i in range(5):
        yy = y + h * (0.28 + i * 0.13)
        amp = 10 - i * 1.4
        pts = []
        for k in range(25):
            t = k / 24
            pts.append((x + 14 + t * (w * 0.55),
                        yy + math.sin(t * 6.2 + i) * amp * 0.5))
        g.append(f'<path d="M ' + " L ".join("%.1f,%.1f" % p for p in pts) +
                 f'" fill="none" stroke="{a}" stroke-width="0.9" stroke-opacity="{0.5 - i * 0.07:.2f}"/>')
    g.append(f'<rect x="{x + w * 0.66}" y="{y + h * 0.26}" width="{w * 0.24}" height="{h * 0.42}" rx="3" '
             f'fill="none" stroke="{a}" stroke-opacity="0.45"/>')
    g.append(f'<circle cx="{x + w * 0.78}" cy="{y + h * 0.47}" r="{h * 0.13}" fill="{a}" fill-opacity="0.14"/>')
    for i in range(3):
        g.append(f'<rect x="{x + 14}" y="{y + h * 0.68 + i * 9}" width="{w * (0.5 - i * 0.09):.0f}" height="3" rx="1.5" fill="{a}" fill-opacity="0.30"/>')
    return "".join(g)


def art_verde_app(x, y, w, h, a):
    """Sensor tiles with sparklines and a ring gauge."""
    g = []
    for i in range(4):
        cx = x + 14 + (i % 2) * (w * 0.30)
        cy = y + h * 0.24 + (i // 2) * (h * 0.30)
        tw, th = w * 0.26, h * 0.24
        g.append(f'<rect x="{cx}" y="{cy}" width="{tw}" height="{th}" rx="3" fill="{a}" fill-opacity="0.07" stroke="{a}" stroke-opacity="0.25"/>')
        pts = [(cx + 4 + k * ((tw - 8) / 8), cy + th * 0.72 - math.sin(k * 1.1 + i) * th * 0.20) for k in range(9)]
        g.append('<path d="M ' + " L ".join("%.1f,%.1f" % p for p in pts) + f'" fill="none" stroke="{a}" stroke-width="1" stroke-opacity="0.8"/>')
        g.append(f'<rect x="{cx + 4}" y="{cy + 5}" width="{tw * 0.4}" height="2.5" rx="1.2" fill="{a}" fill-opacity="0.35"/>')
    ccx, ccy, r = x + w * 0.80, y + h * 0.55, h * 0.24
    g.append(f'<circle cx="{ccx}" cy="{ccy}" r="{r}" fill="none" stroke="{a}" stroke-opacity="0.16" stroke-width="6"/>')
    arc = f"M {ccx},{ccy - r} A {r},{r} 0 1 1 {ccx - r * 0.71:.1f},{ccy + r * 0.71:.1f}"
    g.append(f'<path d="{arc}" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-opacity="0.85"/>')
    return "".join(g)


def art_nirmaan_app(x, y, w, h, a):
    """Map with pins, plus a booking list."""
    g = [f'<rect x="{x + 12}" y="{y + h * 0.20}" width="{w * 0.52}" height="{h * 0.62}" rx="3" fill="{a}" fill-opacity="0.06" stroke="{a}" stroke-opacity="0.22"/>']
    for i in range(4):
        yy = y + h * (0.30 + i * 0.13)
        g.append(f'<line x1="{x + 12}" y1="{yy}" x2="{x + 12 + w * 0.52}" y2="{yy + 6}" stroke="{a}" stroke-opacity="0.12"/>')
    for px, py in ((0.34, 0.36), (0.52, 0.55), (0.24, 0.66)):
        g.append(f'<circle cx="{x + w * px}" cy="{y + h * py}" r="3.2" fill="{a}" fill-opacity="0.9"/>')
        g.append(f'<circle cx="{x + w * px}" cy="{y + h * py}" r="6.5" fill="none" stroke="{a}" stroke-opacity="0.28"/>')
    for i in range(3):
        g.append(f'<rect x="{x + w * 0.70}" y="{y + h * 0.22 + i * 15}" width="{w * 0.22}" height="10" rx="2" fill="{a}" fill-opacity="0.10" stroke="{a}" stroke-opacity="0.20"/>')
    return "".join(g)


def art_nirmaan_portfolio(x, y, w, h, a):
    """Cinematic stacked acts."""
    g = []
    for i in range(5):
        bw = w * (0.72 - i * 0.08)
        g.append(f'<rect x="{x + 14}" y="{y + h * 0.20 + i * (h * 0.13):.1f}" width="{bw:.0f}" height="{h * 0.085:.0f}" rx="2" fill="{a}" fill-opacity="{0.26 - i * 0.04:.2f}"/>')
    g.append(f'<rect x="{x + w * 0.74}" y="{y + h * 0.20}" width="{w * 0.16}" height="{h * 0.53}" rx="2" fill="none" stroke="{a}" stroke-opacity="0.4"/>')
    g.append(f'<circle cx="{x + w * 0.82}" cy="{y + h * 0.46}" r="{h * 0.10}" fill="{a}" fill-opacity="0.30"/>')
    g.append(f'<circle cx="{x + w * 0.82}" cy="{y + h * 0.46}" r="{h * 0.17}" fill="none" stroke="{a}" stroke-opacity="0.25"/>')
    return "".join(g)


def art_skillverse(x, y, w, h, a):
    """Bar chart plus a rising line."""
    g = []
    for i in range(6):
        bh = h * (0.16 + 0.075 * ((i * 5) % 6))
        g.append(f'<rect x="{x + 14 + i * (w * 0.055)}" y="{y + h * 0.74 - bh:.1f}" width="{w * 0.035:.0f}" height="{bh:.1f}" rx="1.5" fill="{a}" fill-opacity="{0.35 + i * 0.06:.2f}"/>')
    pts = [(x + 14 + k * (w * 0.30 / 8), y + h * 0.50 - k * h * 0.028) for k in range(9)]
    g.append('<path d="M ' + " L ".join("%.1f,%.1f" % p for p in pts) + f'" fill="none" stroke="{a}" stroke-width="1.4" stroke-opacity="0.85"/>')
    g.append(f'<rect x="{x + w * 0.56}" y="{y + h * 0.24}" width="{w * 0.33}" height="{h * 0.20}" rx="3" fill="{a}" fill-opacity="0.14" stroke="{a}" stroke-opacity="0.38"/>')
    g.append(f'<rect x="{x + w * 0.56}" y="{y + h * 0.50}" width="{w * 0.33}" height="{h * 0.24}" rx="3" fill="{a}" fill-opacity="0.14" stroke="{a}" stroke-opacity="0.38"/>')
    return "".join(g)


def art_resonate(x, y, w, h, a):
    """Waveform / shader field."""
    g = []
    for row in range(3):
        pts = []
        for k in range(41):
            t = k / 40
            amp = (h * 0.07) * (1 - row * 0.22)
            pts.append((x + 12 + t * (w - 24),
                        y + h * (0.36 + row * 0.16) + math.sin(t * 11 + row * 2) * amp))
        g.append('<path d="M ' + " L ".join("%.1f,%.1f" % p for p in pts) +
                 f'" fill="none" stroke="{a}" stroke-width="{1.5 - row * 0.3:.1f}" stroke-opacity="{0.75 - row * 0.2:.2f}"/>')
    g.append(f'<circle cx="{x + w / 2}" cy="{y + h * 0.60}" r="{h * 0.22}" fill="none" stroke="{a}" stroke-opacity="0.16"/>')
    return "".join(g)


def art_rakshabandhan(x, y, w, h, a):
    """Two cities, one thread."""
    g = []
    lx, rx = x + w * 0.20, x + w * 0.80
    cy = y + h * 0.50
    g.append(f'<path d="M {lx},{cy} C {x + w * 0.35},{cy - h * 0.30} {x + w * 0.65},{cy + h * 0.30} {rx},{cy}" '
             f'fill="none" stroke="{a}" stroke-width="1.6" stroke-opacity="0.8"/>')
    for cx in (lx, rx):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{a}" fill-opacity="0.95"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{a}" stroke-opacity="0.30"/>')
    for i, (px, py) in enumerate(((0.34, 0.32), (0.50, 0.24), (0.66, 0.34), (0.42, 0.68), (0.58, 0.70))):
        g.append(f'<circle cx="{x + w * px}" cy="{y + h * py}" r="1.6" fill="{a}" fill-opacity="0.5"/>')
    g.append(f'<text x="{x + w / 2}" y="{y + h * 0.83}" font-family="{MONO}" font-size="7" letter-spacing="1.6" fill="{a}" fill-opacity="0.55" text-anchor="middle">1,450 KM</text>')
    return "".join(g)


def art_verde_prev(x, y, w, h, a):
    """Older layout: boot log + block hero."""
    g = [f'<rect x="{x + 12}" y="{y + h * 0.20}" width="{w * 0.44}" height="{h * 0.60}" rx="3" fill="{a}" fill-opacity="0.07" stroke="{a}" stroke-opacity="0.22"/>']
    for i in range(6):
        g.append(f'<rect x="{x + 18}" y="{y + h * 0.26 + i * 9}" width="{w * (0.30 - (i % 3) * 0.05):.0f}" height="2.6" rx="1.3" fill="{a}" fill-opacity="0.38"/>')
    g.append(f'<rect x="{x + w * 0.60}" y="{y + h * 0.24}" width="{w * 0.28}" height="{h * 0.22}" rx="2" fill="{a}" fill-opacity="0.26"/>')
    g.append(f'<rect x="{x + w * 0.60}" y="{y + h * 0.52}" width="{w * 0.28}" height="{h * 0.28}" rx="2" fill="{a}" fill-opacity="0.10" stroke="{a}" stroke-opacity="0.42"/>')
    return "".join(g)


PROJECTS = [
    ("VERDE PORTFOLIO", "VERDE-PORTFOLIO", "#5BD69B", art_verde_portfolio),
    ("VERDE APP",       "VERDE-APP",       "#4FB3D9", art_verde_app),
    ("NIRMAAN APP",     "NIRMAAN-APP",     "#00E08A", art_nirmaan_app),
    ("NIRMAN PORTFOLIO","NIRMAN-PORTFOLIO","#C1272D", art_nirmaan_portfolio),
    ("SKILL-VERSE",     "SKILL-VERSE",     "#7C6BF0", art_skillverse),
    ("RESONATE",        "RESONATE",        "#E0563F", art_resonate),
    ("RAKSHABANDHAN",   "RAKSHABANDHAN",   "#E8A33D", art_rakshabandhan),
    ("VERDE PREVIOUS",  "VERDE-PREVIOUS",  "#6E8B7A", art_verde_prev),
]


def card(i, name, accent, art):
    col, row = i % COLS, i // COLS
    x = PAD + col * (CW + GX)
    y = PAD + row * (CH + GY)
    inner_y = y + 22
    inner_h = CH - 22 - 30
    return f'''
  <g>
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="7" fill="{CARD}" stroke="#FFFFFF" stroke-opacity="0.07"/>
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="7" fill="{accent}" fill-opacity="0.022"/>
    {chrome(x, y, CW, accent)}
    {art(x, inner_y, CW, inner_h, accent)}
    <rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="7" fill="{accent}" opacity="0">
      <animate attributeName="opacity" values="0;0.16;0" dur="1.2s" begin="{0.15 + i * 0.11:.2f}s" fill="freeze"/>
    </rect>
    <line x1="{x}" y1="{y + CH - 30}" x2="{x + CW}" y2="{y + CH - 30}" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <circle cx="{x + 16}" cy="{y + CH - 15}" r="3" fill="{accent}" fill-opacity="0.9"/>
    <text x="{x + 26}" y="{y + CH - 11}" font-family="{MONO}" font-size="8.6" letter-spacing="1.5" fill="{CREAM}" fill-opacity="0.85">{name}</text>
  </g>'''


grid = "".join(card(i, n, a, f) for i, (n, _, a, f) in enumerate(PROJECTS))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Selected work">
  <defs>
    <radialGradient id="scGlow" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="{VERM}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="scBeam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.055"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#scGlow)"/>
{grid}
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.10;0.14;1" dur="16s" repeatCount="indefinite"/>
    <rect x="0" y="-90" width="{W}" height="90" fill="url(#scBeam)">
      <animateTransform attributeName="transform" type="translate" values="0 0;0 460" dur="3.2s" repeatCount="indefinite"/>
    </rect>
  </g>
  <text x="{W / 2}" y="{H - 4}" font-family="{MONO}" font-size="8.5" letter-spacing="3.4" fill="{ASH}" fill-opacity="0.62" text-anchor="middle">EIGHT SEALS · ONE HAND</text>
</svg>
'''

if __name__ == "__main__":
    (HERE / "projects.svg").write_text(svg, encoding="utf-8")
    print(f"wrote projects.svg  {len(svg):6d} bytes  {W}x{H}")
