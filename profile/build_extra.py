#!/usr/bin/env python3
"""Second wave: the eye EVOLVES, plus a Bingo Book dossier card.

  evolution.svg  Sharingan -> Mangekyo -> Rinnegan, timed and morphing
  bingo.svg      S-rank dossier card, bounty sheet
  seal.svg       rotating Uchiha crest watermark for section breaks

Run after build_svgs.py:  python3 build_extra.py
"""
import math
import pathlib

from build_svgs import (
    DEFS, VOID, INK, BLOOD, CRIMSON, SCARLET, BLAZE, EMBER, GOLD,
    IVORY, ASH, DIM, MONO, SERIF, BLACK,
    tomoe, rotating_tomoe, crest, embers,
)

HERE = pathlib.Path(__file__).parent
CYCLE = "18s"          # one full evolution loop
KT = "0;0.30;0.33;0.63;0.66;0.97;1"


# ─── geometry ────────────────────────────────────────────────────────────────
def blade_path(r0=26.0, r1=96.0, th0=0.0, th1=128.0, wmax=34.0, n=44, hook=0.95):
    """A Mangekyo blade swept in polar space: thin at the root, wide at the rim."""
    def edge(sign):
        pts = []
        for i in range(n + 1):
            t = i / n
            r = r0 + (r1 - r0) * t
            th = math.radians(th0 + (th1 - th0) * t)
            half = (wmax / 2) * math.sin(math.pi * (t ** hook)) * sign

            t2 = min(1.0, t + 0.01)
            r2 = r0 + (r1 - r0) * t2
            th2 = math.radians(th0 + (th1 - th0) * t2)
            dx = r2 * math.cos(th2) - r * math.cos(th)
            dy = r2 * math.sin(th2) - r * math.sin(th)
            L = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / L, dx / L
            cx, cy = r * math.cos(th), r * math.sin(th)
            pts.append((cx + nx * half, cy + ny * half))
        return pts

    pts = edge(+1) + edge(-1)[::-1]
    return "M " + " L ".join("%.2f,%.2f" % p for p in pts) + " Z"


BLADE = blade_path()


# ─── the three eyes ──────────────────────────────────────────────────────────
def eye_shell(cx, cy, R, glow_id="eyeGlow"):
    """Rim, iris, halo - shared by every stage."""
    return f'''
    <circle cx="{cx}" cy="{cy}" r="{R * 1.20:.1f}" fill="none" stroke="{CRIMSON}" stroke-opacity="0.20" stroke-width="1">
      <animate attributeName="r" values="{R * 1.14:.1f};{R * 1.30:.1f};{R * 1.14:.1f}" dur="4.5s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values="0.24;0.03;0.24" dur="4.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="{R * 1.16:.1f}" fill="url(#{glow_id})"/>
    <circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="url(#irisGrad)"/>
    <circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="none" stroke="{SCARLET}" stroke-opacity="0.50" stroke-width="1.8"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.955:.1f}" fill="none" stroke="{VOID}" stroke-opacity="0.60" stroke-width="2.4"/>'''


def stage3(cx, cy, R, dur="9s"):
    span = 0.93 * R - 0.26 * R
    ts = span / 54.0
    return eye_shell(cx, cy, R) + rotating_tomoe(cx, cy, 0.585 * R, dur=dur, scale=ts) + f'''
    <circle cx="{cx}" cy="{cy}" r="{R * 0.205:.1f}" fill="#040206"/>'''


def stage_mangekyo(cx, cy, R, dur="11s"):
    """Three-blade Mangekyo.

    translate + scale on the outer group, rotation on an inner one, so the
    animation cannot shadow the positioning transform.
    """
    k = R / 96.0
    arms = "".join(
        f'<g transform="rotate({a})"><path d="{BLADE}" fill="#050308"/></g>'
        for a in (0, 120, 240)
    )
    return eye_shell(cx, cy, R) + f'''
    <g transform="translate({cx},{cy})">
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="0 0 0" to="360 0 0" dur="{dur}" repeatCount="indefinite"/>
        <g transform="scale({k:.3f})">{arms}</g>
      </g>
    </g>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.175:.1f}" fill="#040206"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.175:.1f}" fill="none" stroke="{CRIMSON}" stroke-opacity="0.5" stroke-width="1.2"/>'''


def stage_rinnegan(cx, cy, R, dur="14s"):
    rings = []
    for i, frac in enumerate((0.94, 0.78, 0.62, 0.46, 0.30, 0.16)):
        rings.append(
            f'<circle cx="{cx}" cy="{cy}" r="{R * frac:.1f}" fill="none" '
            f'stroke="#372C52" stroke-width="{2.6 - i * 0.22:.2f}" stroke-opacity="{0.85 - i * 0.07:.2f}">'
            f'<animate attributeName="r" values="{R * frac:.1f};{R * frac * 1.035:.1f};{R * frac:.1f}" '
            f'dur="{3 + i * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return f'''
    <circle cx="{cx}" cy="{cy}" r="{R * 1.20:.1f}" fill="none" stroke="#7B6CA8" stroke-opacity="0.22" stroke-width="1">
      <animate attributeName="stroke-opacity" values="0.28;0.05;0.28" dur="5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="{R * 1.16:.1f}" fill="url(#rinGlow)"/>
    <circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="url(#rinGrad)"/>
    <circle cx="{cx}" cy="{cy}" r="{R * 0.955:.1f}" fill="none" stroke="#241C38" stroke-opacity="0.8" stroke-width="2.6"/>
    {''.join(rings)}
    <circle cx="{cx}" cy="{cy}" r="{R * 0.085:.1f}" fill="#050308"/>'''


# ─── extra defs ──────────────────────────────────────────────────────────────
EXTRA_DEFS = f'''
    <radialGradient id="rinGrad" cx="0.45" cy="0.40" r="0.70">
      <stop offset="0" stop-color="#B9A9E0"/>
      <stop offset="0.45" stop-color="#6F5C9E"/>
      <stop offset="1" stop-color="#2A2140"/>
    </radialGradient>
    <radialGradient id="rinGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#9C86D8" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#9C86D8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#14100F"/>
      <stop offset="0.5" stop-color="#0C0908"/>
      <stop offset="1" stop-color="#120A0C"/>
    </linearGradient>
    <pattern id="grain" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="3" fill="none"/>
      <circle cx="0.5" cy="0.5" r="0.45" fill="#FFFFFF" fill-opacity="0.035"/>
      <circle cx="2.1" cy="1.7" r="0.4" fill="#FFFFFF" fill-opacity="0.022"/>
    </pattern>'''


# ─── evolution.svg ───────────────────────────────────────────────────────────
EW, EH = 1000, 360
CX, CY, ER = 500, 168, 108

evolution = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{EW}" height="{EH}" viewBox="0 0 {EW} {EH}" fill="none" role="img" aria-label="Sharingan evolving into Mangekyo into Rinnegan">
{DEFS}
{EXTRA_DEFS}
  <rect width="{EW}" height="{EH}" fill="{VOID}"/>
  <rect width="{EW}" height="{EH}" fill="url(#gridFine)"/>
  <rect width="{EW}" height="{EH}" fill="url(#voidGlow)"/>

  <g opacity="0.28">{crest(CX, CY, r=210, fill="#3A1116", spin="150s")}</g>
  {embers(18, EW, EH)}

  <g opacity="1">
    <animate attributeName="opacity" values="1;1;0;0;0;0;1" keyTimes="{KT}" dur="{CYCLE}" repeatCount="indefinite"/>
    {stage3(CX, CY, ER, dur="9s")}
  </g>

  <g opacity="0">
    <animate attributeName="opacity" values="0;0;1;1;0;0;0" keyTimes="{KT}" dur="{CYCLE}" repeatCount="indefinite"/>
    {stage_mangekyo(CX, CY, ER, dur="11s")}
  </g>

  <g opacity="0">
    <animate attributeName="opacity" values="0;0;0;0;1;1;0" keyTimes="{KT}" dur="{CYCLE}" repeatCount="indefinite"/>
    {stage_rinnegan(CX, CY, ER, dur="14s")}
  </g>

  <!-- evolution flash -->
  <circle cx="{CX}" cy="{CY}" r="{ER * 1.15:.0f}" fill="none" stroke="{BLAZE}" stroke-width="2" opacity="0">
    <animate attributeName="opacity" values="0;0;0.5;0;0;0;0.5;0;0" keyTimes="0;0.28;0.315;0.35;0.61;0.63;0.665;0.70;1" dur="{CYCLE}" repeatCount="indefinite"/>
  </circle>

  <!-- captions -->
  <g font-family="{MONO}" text-anchor="middle">
    <text x="{CX}" y="304" font-size="13" letter-spacing="6" fill="{BLAZE}">SHARINGAN</text>
    <animate attributeName="opacity" values="1;0" keyTimes="0;0.30" dur="{CYCLE}" repeatCount="indefinite"/>
  </g>
  <g font-family="{MONO}" text-anchor="middle" opacity="0">
    <text x="{CX}" y="304" font-size="13" letter-spacing="6" fill="{BLAZE}">MANGEKYŌ SHARINGAN</text>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.33;0.60;0.66" dur="{CYCLE}" repeatCount="indefinite"/>
  </g>
  <g font-family="{MONO}" text-anchor="middle" opacity="0">
    <text x="{CX}" y="304" font-size="13" letter-spacing="6" fill="#B9A9E0">RINNEGAN</text>
    <animate attributeName="opacity" values="0;1" keyTimes="0;0.66" dur="{CYCLE}" repeatCount="indefinite"/>
  </g>

  <text x="{CX}" y="332" font-family="{MONO}" text-anchor="middle" font-size="9.5" letter-spacing="3" fill="{DIM}">THE EYE EVOLVES · I · II · III</text>
</svg>
'''


# ─── bingo.svg ───────────────────────────────────────────────────────────────
BW, BH = 860, 300
bingo = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" fill="none" role="img" aria-label="Bingo Book dossier">
{DEFS}
{EXTRA_DEFS}
  <rect width="{BW}" height="{BH}" rx="10" fill="url(#cardGrad)"/>
  <rect width="{BW}" height="{BH}" rx="10" fill="url(#grain)"/>
  <rect x="0.75" y="0.75" width="{BW - 1.5}" height="{BH - 1.5}" rx="9.5" fill="none" stroke="{CRIMSON}" stroke-opacity="0.35" stroke-width="1.5"/>
  <rect x="6.75" y="6.75" width="{BW - 13.5}" height="{BH - 13.5}" rx="6" fill="none" stroke="{CRIMSON}" stroke-opacity="0.12" stroke-width="1"/>

  <rect x="0" y="0" width="5" height="{BH}" fill="{CRIMSON}" fill-opacity="0.55"/>

  <text x="34" y="38" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{ASH}">BINGO BOOK · CONFIDENTIAL</text>
  <text x="{BW - 34}" y="38" font-family="{MONO}" font-size="10.5" letter-spacing="3.6" fill="{BLAZE}" text-anchor="end">S-RANK</text>
  <line x1="34" y1="52" x2="{BW - 34}" y2="52" stroke="{CRIMSON}" stroke-opacity="0.30" stroke-width="1"/>

  <!-- portrait -->
  <rect x="34" y="72" width="176" height="176" rx="6" fill="#0A0709" stroke="{CRIMSON}" stroke-opacity="0.35"/>
  <g transform="translate(122,160) scale(0.55)">
    {stage3(0, 0, 108, dur="8s")}
  </g>
  <text x="122" y="272" font-family="{MONO}" font-size="8.5" letter-spacing="2" fill="{DIM}" text-anchor="middle">NO. 001 · UCHIHA</text>

  <!-- record -->
  <text x="248" y="88" font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{ASH}">TARGET DESIGNATION</text>
  <text x="246" y="126" font-family="{BLACK}" font-size="34" letter-spacing="1" fill="{IVORY}">ANUJ PHULERA</text>
  <line x1="248" y1="140" x2="{BW - 40}" y2="140" stroke="{CRIMSON}" stroke-opacity="0.35" stroke-width="1"/>

  <g font-family="{MONO}" font-size="10.5" fill="{ASH}">
    <text x="248" y="168">ORIGIN</text>
    <text x="248" y="192">AFFILIATION</text>
    <text x="248" y="216">KEKKEI GENKAI</text>
    <text x="248" y="240">NATURE</text>
    <text x="248" y="264">STATUS</text>
  </g>
  <g font-family="{MONO}" font-size="10.5" fill="{IVORY}">
    <text x="400" y="168">JAIPUR, INDIA</text>
    <text x="400" y="192">INDEPENDENT</text>
    <text x="400" y="216" fill="{BLAZE}">PROCEDURAL LAYOUT</text>
    <text x="400" y="240">REACT · TYPE · ESP32</text>
    <text x="400" y="264" fill="#7BE38B">ACTIVE</text>
  </g>

  <g stroke="{DIM}" stroke-opacity="0.25" stroke-width="0.8">
    <line x1="248" y1="176" x2="{BW - 40}" y2="176"/>
    <line x1="248" y1="200" x2="{BW - 40}" y2="200"/>
    <line x1="248" y1="224" x2="{BW - 40}" y2="224"/>
    <line x1="248" y1="248" x2="{BW - 40}" y2="248"/>
  </g>

  <text x="248" y="288" font-family="{MONO}" font-size="9" letter-spacing="2.4" fill="{DIM}">BOUNTY · NOT FOR SALE</text>
</svg>
'''


# ─── seal.svg ────────────────────────────────────────────────────────────────
SW = SH = 160
seal = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}" fill="none" role="img" aria-label="Uchiha crest">
{DEFS}
{crest(SW / 2, SH / 2, r=74, fill=CRIMSON, opacity="0.85")}
</svg>
'''

if __name__ == "__main__":
    for name, content in [
        ("evolution.svg", evolution),
        ("bingo.svg", bingo),
        ("seal.svg", seal),
    ]:
        (HERE / name).write_text(content, encoding="utf-8")
        print(f"wrote {name:16s} {len(content):6d} bytes")
