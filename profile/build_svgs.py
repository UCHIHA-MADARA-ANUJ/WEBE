#!/usr/bin/env python3
"""Generate the Madara-themed animated SVGs for the profile README.

Everything is self-contained: SMIL animation, system fonts, no external
services. GitHub renders these as images, and SMIL/CSS inside an <img>
SVG does animate.

Run:  python3 build_svgs.py
Out:  banner.svg, sharingan.svg, divider.svg, typing.svg
"""
import math
import random

random.seed(7)

# ─── palette ─────────────────────────────────────────────────────────────────
VOID      = "#06050A"
INK       = "#0B0709"
BLOOD     = "#8B0A14"
CRIMSON   = "#C1121F"
SCARLET   = "#E01E2B"
BLAZE     = "#FF3B3B"
EMBER     = "#FF7A18"
GOLD      = "#FFB020"
IVORY     = "#F5EFE6"
ASH       = "#8A8189"
DIM       = "#5A4E56"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"
BLACK = "'Arial Black', 'Helvetica Neue', Impact, 'DejaVu Sans', sans-serif"


def tomoe(scale=1.0, fill="#050308"):
    """A magatama: full circular head with a tail that spirals inward."""
    return (
        f'<g transform="scale({scale})">'
        f'<path d="M 0,-14 A 14,14 0 1 1 -12.1,7 C -8,12 -3,16 2,23 '
        f'C 4,26.5 1.5,29.5 -1.8,28 C -9,24.5 -14,17 -14,7 A 14,14 0 0 1 0,-14 Z" '
        f'fill="{fill}"/>'
        f'</g>'
    )


def rotating_tomoe(cx, cy, orbit, count=3, dur="9s", fill="#050308", scale=1.0):
    """Three tomoe that spin forever.

    The translate lives on an OUTER group and the rotation on an INNER one.
    Putting both on the same element lets <animateTransform additive="replace">
    wipe out the translate, which draws the tomoe around the origin instead of
    around the eye. Never merge these two groups.
    """
    parts = []
    for i in range(count):
        a = i * (360 / count)
        parts.append(
            f'<g transform="rotate({a}) translate(0,{-orbit})">{tomoe(scale, fill)}</g>'
        )
    return (
        f'<g transform="translate({cx},{cy})">'
        f'<g opacity="0.97">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0 0 0" to="360 0 0" dur="{dur}" repeatCount="indefinite"/>'
        + "".join(parts) +
        '</g></g>'
    )


def embers(n=30, w=1200, h=340):
    """Rising sparks across the banner."""
    out = []
    for i in range(n):
        x = random.uniform(20, w - 20)
        r = random.uniform(0.7, 2.2)
        dur = random.uniform(7.5, 15)
        begin = random.uniform(0, 12)
        drift = random.uniform(-34, 34)
        rise = h + 40
        base = EMBER if random.random() > 0.35 else GOLD
        out.append(
            f'<circle cx="{x:.1f}" cy="{h + 10}" r="{r:.1f}" fill="{base}" opacity="0">'
            f'<animate attributeName="cy" values="{h + 10};-30" dur="{dur:.1f}s" '
            f'begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{x:.1f};{x + drift:.1f}" dur="{dur:.1f}s" '
            f'begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.85;0.55;0" '
            f'keyTimes="0;0.18;0.65;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "".join(out)


def crest(cx, cy, r=56, fill="#3A1116", opacity="0.30", spin=None):
    """Uchiha uchiwa - a fan: circle with a curved tapering tail.

    As with the tomoe, the spin is applied to an inner group so it cannot
    shadow the outer translate.
    """
    anim = (f'<animateTransform attributeName="transform" type="rotate" '
            f'from="0 0 0" to="360 0 0" dur="{spin}" repeatCount="indefinite"/>') if spin else ""
    body = (
        f'<circle cx="0" cy="{-r * 0.22:.1f}" r="{r * 0.80:.1f}"/>'
        f'<path d="M {r * 0.46:.1f},{r * 0.36:.1f} '
        f'C {r * 0.84:.1f},{r * 0.70:.1f} {r * 0.94:.1f},{r * 1.16:.1f} {r * 0.70:.1f},{r * 1.46:.1f} '
        f'C {r * 0.50:.1f},{r * 1.71:.1f} {r * 0.14:.1f},{r * 1.77:.1f} {r * 0.00:.1f},{r * 1.58:.1f} '
        f'C {r * -0.09:.1f},{r * 1.45:.1f} {r * -0.02:.1f},{r * 1.29:.1f} {r * 0.12:.1f},{r * 1.25:.1f} '
        f'C {r * 0.24:.1f},{r * 1.22:.1f} {r * 0.33:.1f},{r * 1.31:.1f} {r * 0.31:.1f},{r * 1.41:.1f} '
        f'L {r * 0.45:.1f},{r * 1.33:.1f} '
        f'C {r * 0.52:.1f},{r * 1.10:.1f} {r * 0.34:.1f},{r * 0.94:.1f} {r * 0.14:.1f},{r * 1.02:.1f} '
        f'C {r * -0.12:.1f},{r * 1.12:.1f} {r * -0.19:.1f},{r * 1.46:.1f} {r * 0.02:.1f},{r * 1.63:.1f} '
        f'C {r * 0.30:.1f},{r * 1.88:.1f} {r * 0.74:.1f},{r * 1.77:.1f} {r * 1.00:.1f},{r * 1.45:.1f} '
        f'C {r * 1.30:.1f},{r * 1.08:.1f} {r * 1.18:.1f},{r * 0.62:.1f} {r * 0.78:.1f},{r * 0.32:.1f} Z"/>'
    )
    return (
        f'<g transform="translate({cx},{cy})">'
        f'<g opacity="{opacity}" fill="{fill}">{anim}{body}</g>'
        f'</g>'
    )


def sharingan_group(cx, cy, R, dur="10s", glow_id="eyeGlow", tomoe_mult=1.0):
    """Full three-tomoe Sharingan.

    The tomoe are sized so the whole comma spans from just outside the pupil
    (0.30 R) to just inside the rim (0.95 R) - they never merge into the pupil.
    """
    span = 0.93 * R - 0.26 * R          # radial space the comma must fill
    tscale = (span / 54.0) * tomoe_mult  # comma is 56 units tall at scale 1
    orbit = 0.585 * R
    return f'''
  <g>
    <circle cx="{cx}" cy="{cy}" r="{R * 1.20:.1f}" fill="none" stroke="{CRIMSON}" stroke-opacity="0.20" stroke-width="1">
      <animate attributeName="r" values="{R * 1.14:.1f};{R * 1.30:.1f};{R * 1.14:.1f}" dur="4.5s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.24;0.03;0.24" dur="4.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="{R * 1.16:.1f}" fill="url(#{glow_id})"/>

    <circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="url(#irisGrad)"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.88:.1f}" fill="none" stroke="{BLAZE}" stroke-opacity="0.10" stroke-width="1"/>
    <circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="none" stroke="{SCARLET}" stroke-opacity="0.50" stroke-width="1.8"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.955:.1f}" fill="none" stroke="{VOID}" stroke-opacity="0.60" stroke-width="2.4"/>

    {rotating_tomoe(cx, cy, orbit, dur=dur, scale=tscale)}

    <circle cx="{cx}" cy="{cy}" r="{R * 0.205:.1f}" fill="#040206"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.205:.1f}" fill="none" stroke="{CRIMSON}" stroke-opacity="0.40" stroke-width="1.3">
      <animate attributeName="stroke-opacity" values="0.15;0.65;0.15" dur="3.2s" repeatCount="indefinite"/>
    </circle>

    <ellipse cx="{cx - R * 0.36:.1f}" cy="{cy - R * 0.40:.1f}" rx="{R * 0.075:.1f}" ry="{R * 0.038:.1f}"
             fill="{IVORY}" opacity="0.09" transform="rotate(-30 {cx - R * 0.36:.1f} {cy - R * 0.40:.1f})"/>
  </g>'''


# ─── shared defs ─────────────────────────────────────────────────────────────
DEFS = f'''
  <defs>
    <radialGradient id="irisGrad" cx="0.42" cy="0.36" r="0.72">
      <stop offset="0" stop-color="#E8453F"/>
      <stop offset="0.38" stop-color="{CRIMSON}"/>
      <stop offset="0.74" stop-color="#5C060C"/>
      <stop offset="1" stop-color="#2A0206"/>
    </radialGradient>

    <radialGradient id="eyeGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{SCARLET}" stop-opacity="0.55"/>
      <stop offset="0.55" stop-color="{BLOOD}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{BLOOD}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="voidGlow" cx="0.74" cy="0.44" r="0.62">
      <stop offset="0" stop-color="{CRIMSON}" stop-opacity="0.22"/>
      <stop offset="0.5" stop-color="{BLOOD}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{VOID}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="emberWash" cx="0.10" cy="0.95" r="0.55">
      <stop offset="0" stop-color="{EMBER}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="ruleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CRIMSON}" stop-opacity="0.85"/>
      <stop offset="0.45" stop-color="{EMBER}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="nameGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFF3EA"/>
      <stop offset="0.55" stop-color="{IVORY}"/>
      <stop offset="1" stop-color="#C9A9A0"/>
    </linearGradient>

    <pattern id="gridFine" width="44" height="44" patternUnits="userSpaceOnUse">
      <path d="M44 0H0V44" stroke="#FFFFFF" stroke-opacity="0.022" stroke-width="1"/>
    </pattern>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>'''


# ─── banner.svg ──────────────────────────────────────────────────────────────
W, H = 1200, 340
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Anuj Phulera — wake up to reality">
{DEFS}

  <rect width="{W}" height="{H}" fill="{VOID}"/>
  <rect width="{W}" height="{H}" fill="url(#gridFine)"/>
  <rect width="{W}" height="{H}" fill="url(#voidGlow)"/>
  <rect width="{W}" height="{H}" fill="url(#emberWash)"/>

  {crest(975, 172, r=215, fill="#3A1116", opacity="0.20", spin="150s")}

  {embers(30, W, H)}

  {sharingan_group(975, 172, 122, dur="9s")}

  <rect x="0" y="0" width="3" height="{H}" fill="{CRIMSON}" fill-opacity="0.75"/>

  <text x="72" y="86" font-family="{MONO}" font-size="12" letter-spacing="4.6" fill="{ASH}">UCHIHA CLAN · INTERFACE ENGINEER</text>

  <text x="70" y="163" font-family="{BLACK}" font-size="58" letter-spacing="1.2" fill="url(#nameGrad)" filter="url(#softGlow)">ANUJ PHULERA</text>

  <rect x="72" y="190" width="430" height="1.5" fill="url(#ruleGrad)"/>

  <text x="72" y="228" font-family="{SERIF}" font-size="25" font-style="italic" fill="{BLAZE}" opacity="0.95">Wake up to reality.</text>

  <text x="72" y="262" font-family="{MONO}" font-size="12.5" letter-spacing="0.3" fill="#B8AEB5">I build interfaces that rebuild themselves</text>
  <text x="72" y="282" font-family="{MONO}" font-size="12.5" letter-spacing="0.3" fill="#B8AEB5">around the person using them.</text>

  <text x="72" y="318" font-family="{MONO}" font-size="10" letter-spacing="2.4" fill="{DIM}">DEEP FIELD · VERDE · NIRMAN · RESONATE</text>
</svg>
'''

# ─── sharingan.svg ───────────────────────────────────────────────────────────
S = 420
eye = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}" fill="none" role="img" aria-label="Sharingan">
{DEFS}
  <rect width="{S}" height="{S}" fill="none"/>
  {sharingan_group(S / 2, S / 2, 150, dur="10s")}
</svg>
'''

# ─── divider.svg ─────────────────────────────────────────────────────────────
DW, DH = 1200, 64
divider = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{DW}" height="{DH}" viewBox="0 0 {DW} {DH}" fill="none" role="img" aria-label="divider">
{DEFS}
  <!-- left + right rules, drawn as plain lines: no mirrored transforms, no
       gradient-unit assumptions, so every renderer draws them identically -->
  <line x1="30"  y1="32" x2="{DW / 2 - 30:.0f}" y2="32" stroke="{CRIMSON}" stroke-opacity="0.55" stroke-width="1.2"/>
  <line x1="{DW / 2 + 30:.0f}" y1="32" x2="{DW - 30}" y2="32" stroke="{CRIMSON}" stroke-opacity="0.55" stroke-width="1.2"/>
  <line x1="30"  y1="32" x2="{DW / 2 - 30:.0f}" y2="32" stroke="{EMBER}" stroke-opacity="0.16" stroke-width="3"/>
  <line x1="{DW / 2 + 30:.0f}" y1="32" x2="{DW - 30}" y2="32" stroke="{EMBER}" stroke-opacity="0.16" stroke-width="3"/>

  <circle cx="{DW / 2 - 30:.0f}" cy="32" r="2" fill="{CRIMSON}" fill-opacity="0.9"/>
  <circle cx="{DW / 2 + 30:.0f}" cy="32" r="2" fill="{CRIMSON}" fill-opacity="0.9"/>

  {sharingan_group(DW / 2, 32, 20, dur="7s")}
</svg>
'''

# ─── typing.svg ──────────────────────────────────────────────────────────────
TW, TH = 640, 52
TEXT = "Wake up to reality."
CH = 13.6 * 0.60  # approx advance for 13.6px mono
tw = len(TEXT) * 13.6 * 0.60
typing = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" fill="none" role="img" aria-label="Wake up to reality.">
  <defs>
    <clipPath id="reveal">
      <rect x="0" y="0" width="0" height="{TH}">
        <animate attributeName="width" from="0" to="{tw + 6:.0f}" dur="2.2s" begin="0.4s" fill="freeze"/>
      </rect>
    </clipPath>
  </defs>

  <text x="{TW / 2 - tw / 2:.0f}" y="34" font-family="{MONO}" font-size="21" letter-spacing="1.6"
        fill="{BLAZE}" clip-path="url(#reveal)">{TEXT}</text>

  <rect x="{TW / 2 - tw / 2:.0f}" y="16" width="9" height="22" fill="{BLAZE}" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.95;1;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
</svg>
'''

if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    for name, content in [
        ("banner.svg", banner),
        ("sharingan.svg", eye),
        ("divider.svg", divider),
        ("typing.svg", typing),
    ]:
        (here / name).write_text(content, encoding="utf-8")
        print(f"wrote {name:16s} {len(content):6d} bytes")
