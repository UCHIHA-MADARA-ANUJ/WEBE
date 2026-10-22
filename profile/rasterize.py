#!/usr/bin/env python3
"""A deliberately small SVG rasterizer — enough to eyeball the banner layout.

Supports: rect, circle, ellipse, line, polyline, path (M/L/C/Q/Z absolute),
linear + radial gradients with stops, translate/rotate/scale transforms,
fill-opacity, group opacity, and rough text via PIL's default font.

It is a proofreading tool, not a renderer. Text metrics will not match a
browser, so treat type as a placement check only.
"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersample


# ── matrices ────────────────────────────────────────────────────────────────
def mul(a, b):
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (
        a0 * b0 + a2 * b1, a1 * b0 + a3 * b1,
        a0 * b2 + a2 * b3, a1 * b2 + a3 * b3,
        a0 * b4 + a2 * b5 + a4, a1 * b4 + a3 * b5 + a5,
    )


IDENT = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def parse_transform(s):
    m = IDENT
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', s or ''):
        v = [float(x) for x in re.findall(r'-?\d*\.?\d+(?:e-?\d+)?', args)]
        if name == 'translate':
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == 'scale':
            sx = v[0]
            sy = v[1] if len(v) > 1 else sx
            t = (sx, 0, 0, sy, 0, 0)
        elif name == 'rotate':
            a = math.radians(v[0])
            ca, sa = math.cos(a), math.sin(a)
            t = (ca, sa, -sa, ca, 0, 0)
            if len(v) >= 3:
                t = mul((1, 0, 0, 1, v[1], v[2]), mul(t, (1, 0, 0, 1, -v[1], -v[2])))
        else:
            continue
        m = mul(m, t)
    return m


# ── colour ──────────────────────────────────────────────────────────────────
def hex_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Gradient:
    def __init__(self, kind, stops, cx=0.5, cy=0.5, x1=0, x2=1):
        self.kind, self.stops = kind, stops
        self.cx, self.cy = cx, cy
        self.x1, self.x2 = x1, x2

    def at(self, u):
        u = max(0.0, min(1.0, u))
        for i in range(len(self.stops) - 1):
            o0, c0, a0 = self.stops[i]
            o1, c1, a1 = self.stops[i + 1]
            if o0 <= u <= o1:
                t = 0 if o1 == o0 else (u - o0) / (o1 - o0)
                c = tuple(int(c0[j] + (c1[j] - c0[j]) * t) for j in range(3))
                return c + (a0 + (a1 - a0) * t,)
        o, c, a = self.stops[-1]
        return c + (a,)

    def sample(self, x, y, box):
        bx, by, bw, bh = box
        if self.kind == 'radial':
            gx = bx + self.cx * bw
            gy = by + self.cy * bh
            d = math.hypot(x - gx, y - gy)
            r = 0.5 * math.hypot(bw, bh)
            return self.at(d / r if r else 0)
        t = ((x - bx) / bw) if bw else 0
        return self.at(t)


def parse_paint(el, idmap):
    f = el.get('fill')
    if not f or f == 'none':
        return None
    m = re.match(r'url\(#(.+?)\)', f)
    if m:
        return idmap.get(m.group(1))
    if f == 'currentColor':
        return hex_rgb('#000000')
    try:
        return hex_rgb(f)
    except Exception:
        return None


# ── path flattening ─────────────────────────────────────────────────────────
TOKEN = re.compile(r'([MmLlCcQqAaZz])|(-?\d*\.?\d+(?:e-?\d+)?)')


def arc_points(p0, rx, ry, phi_deg, large, sweep, p1, steps=24):
    """SVG endpoint arc -> list of points (standard W3C parameterisation)."""
    x0, y0 = p0
    x1, y1 = p1
    if rx == 0 or ry == 0:
        return [(x1, y1)]
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg)
    cp, sp = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x1) / 2, (y0 - y1) / 2
    x1p = cp * dx2 + sp * dy2
    y1p = -sp * dx2 + cp * dy2
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        co = -co
    cxp = co * rx * y1p / ry
    cyp = -co * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x0 + x1) / 2
    cy = sp * cxp + cp * cyp + (y0 + y1) / 2
    th1 = math.atan2((y1p - cyp) / ry, (x1p - cxp) / rx)
    th2 = math.atan2((-y1p - cyp) / ry, (-x1p - cxp) / rx)
    dth = th2 - th1
    if not sweep and dth > 0:
        dth -= 2 * math.pi
    elif sweep and dth < 0:
        dth += 2 * math.pi
    pts = []
    for k in range(1, steps + 1):
        th = th1 + dth * k / steps
        pts.append((
            cx + rx * math.cos(th) * cp - ry * math.sin(th) * sp,
            cy + rx * math.cos(th) * sp + ry * math.sin(th) * cp,
        ))
    return pts


def flatten_path(d):
    toks = []
    for cmd, num in TOKEN.findall(d):
        toks.append(cmd if cmd else float(num))
    pts, cur, start, cmd = [], None, None, None
    i = 0
    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            cmd = t
            i += 1
            if cmd in 'Zz':
                if start:
                    pts.append(start)
                cur = start
            continue
        if cmd in 'Mm':
            x, y = toks[i], toks[i + 1]
            i += 2
            cur = (x, y)
            start = cur
            pts.append(cur)
            cmd = 'L' if cmd == 'M' else 'l'
        elif cmd in 'Ll':
            x, y = toks[i], toks[i + 1]
            i += 2
            cur = (x, y)
            pts.append(cur)
        elif cmd in 'Cc':
            x1, y1, x2, y2, x, y = toks[i:i + 6]
            i += 6
            p0 = cur
            for s in range(1, 17):
                u = s / 16
                v = 1 - u
                px = v**3*p0[0] + 3*v*v*u*x1 + 3*v*u*u*x2 + u**3*x
                py = v**3*p0[1] + 3*v*v*u*y1 + 3*v*u*u*y2 + u**3*y
                pts.append((px, py))
            cur = (x, y)
        elif cmd in 'Qq':
            x1, y1, x, y = toks[i:i + 4]
            i += 4
            p0 = cur
            for s in range(1, 13):
                u = s / 12
                v = 1 - u
                pts.append((v*v*p0[0] + 2*v*u*x1 + u*u*x, v*v*p0[1] + 2*v*u*y1 + u*u*y))
            cur = (x, y)
        elif cmd in 'Aa':
            rx, ry, rot, large, sweep, x, y = toks[i:i + 7]
            i += 7
            pts.extend(arc_points(cur, rx, ry, rot, int(large), int(sweep), (x, y)))
            cur = (x, y)
        else:
            i += 1
    return pts


def ellipse_pts(cx, cy, rx, ry, n=96):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


# ── main routine ────────────────────────────────────────────────────────────
def render(svg_path, out_path, scale=SS):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    W = int(float(root.get('width')))
    H = int(float(root.get('height')))

    canvas = Image.new('RGBA', (W * scale, H * scale), (0, 0, 0, 0))

    # index defs
    grads, clips = {}, {}
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag in ('linearGradient', 'radialGradient'):
            stops = []
            for s in el:
                if s.tag.split('}')[-1] != 'stop':
                    continue
                o = float(s.get('offset', 0))
                col = hex_rgb(s.get('stop-color', '#000'))
                a = float(s.get('stop-opacity', 1)) * 255
                stops.append((o, col, a))
            grads[el.get('id')] = Gradient(
                'radial' if tag == 'radialGradient' else 'linear',
                stops,
                float(el.get('cx', 0.5)), float(el.get('cy', 0.5)),
            )
        elif tag == 'clipPath':
            clips[el.get('id')] = el

    def paint_shape(poly, paint, alpha, m):
        if not poly:
            return
        tp = [apply(m, x, y) for x, y in poly]
        xs = [p[0] for p in tp]
        ys = [p[1] for p in tp]
        box = (min(xs), min(ys), max(max(xs) - min(xs), .001), max(max(ys) - min(ys), .001))
        layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        sp = [(x * scale, y * scale) for x, y in tp]
        if isinstance(paint, Gradient):
            # coarse: fill by horizontal/radial bands
            cx = box[0] + box[2] / 2
            cy = box[1] + box[3] / 2
            col = paint.sample(cx, cy, box)
            rgba = col[:3] + (int(col[3] * alpha),)
            d.polygon(sp, fill=rgba)
        else:
            d.polygon(sp, fill=tuple(paint) + (int(255 * alpha),))
        canvas.alpha_composite(layer)

    def walk(el, m, alpha, inh_fill=None, inh_stroke=None):
        tag = el.tag.split('}')[-1]
        m = mul(m, parse_transform(el.get('transform')))
        op = float(el.get('opacity', 1))
        fo = float(el.get('fill-opacity', 1))
        a = alpha * op * fo

        inherited = el.get('fill') or inh_fill
        if el.get('fill') is None and inh_fill:
            class _E:  # shim so parse_paint sees the inherited value
                def get(self, k, d=None):
                    return inh_fill if k == 'fill' else el.get(k, d)
            paint = parse_paint(_E(), grads)
        else:
            paint = parse_paint(el, grads)
        stroke_in = el.get('stroke') or inh_stroke

        if tag == 'rect' and paint:
            x, y = float(el.get('x', 0)), float(el.get('y', 0))
            w, h = float(el.get('width', 0)), float(el.get('height', 0))
            paint_shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], paint, a, m)
        elif tag == 'circle' and not paint and el.get('stroke'):
            cx, cy, r = float(el.get('cx', 0)), float(el.get('cy', 0)), float(el.get('r', 0))
            sw = float(el.get('stroke-width', 1))
            layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            c = hex_rgb(el.get('stroke'))
            sa = float(el.get('stroke-opacity', 1)) * a
            px, py = apply(m, cx, cy)
            rr = r * (abs(m[0]) if m[0] else 1)
            d.ellipse([(px - rr) * scale, (py - rr) * scale, (px + rr) * scale, (py + rr) * scale],
                      outline=c + (int(255 * sa),), width=max(1, int(sw * scale)))
            canvas.alpha_composite(layer)
        elif tag == 'circle' and paint:
            cx, cy, r = float(el.get('cx', 0)), float(el.get('cy', 0)), float(el.get('r', 0))
            paint_shape(ellipse_pts(cx, cy, r, r), paint, a, m)
        elif tag == 'ellipse' and paint:
            cx, cy = float(el.get('cx', 0)), float(el.get('cy', 0))
            rx, ry = float(el.get('rx', 0)), float(el.get('ry', 0))
            paint_shape(ellipse_pts(cx, cy, rx, ry), paint, a, m)
        elif tag == 'path' and not paint and el.get('stroke'):
            pts = [apply(m, x, y) for x, y in flatten_path(el.get('d', ''))]
            if len(pts) > 1:
                sw = float(el.get('stroke-width', 1))
                layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                c = hex_rgb(el.get('stroke'))
                sa = float(el.get('stroke-opacity', 1)) * a
                d.line([(x * scale, y * scale) for x, y in pts], fill=c + (int(255 * sa),),
                       width=max(1, int(sw * scale)), joint='curve')
                canvas.alpha_composite(layer)
        elif tag == 'path' and paint:
            paint_shape(flatten_path(el.get('d', '')), paint, a, m)
        elif tag == 'line':
            x1, y1 = float(el.get('x1', 0)), float(el.get('y1', 0))
            x2, y2 = float(el.get('x2', 0)), float(el.get('y2', 0))
            sw = float(el.get('stroke-width', 1))
            sp = [apply(m, x1, y1), apply(m, x2, y2)]
            layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            stroke_raw = el.get('stroke', '#ffffff')
            mg = re.match(r'url\(#(.+?)\)', stroke_raw)
            if mg and mg.group(1) in grads:
                gc = grads[mg.group(1)]
                col = gc.sample((sp[0][0] + sp[1][0]) / 2, (sp[0][1] + sp[1][1]) / 2,
                                (min(sp[0][0], sp[1][0]), min(sp[0][1], sp[1][1]), 1, 1))
                c = col[:3]
            else:
                c = hex_rgb(stroke_raw)
            sa = float(el.get('stroke-opacity', 1)) * a
            d.line([(p[0] * scale, p[1] * scale) for p in sp], fill=c + (int(255 * sa),),
                   width=max(1, int(sw * scale)))
            canvas.alpha_composite(layer)
        elif tag == 'text' and paint:
            txt = ' '.join(''.join(el.itertext()).split())
            size = int(float(el.get('font-size', 12)) * scale)
            try:
                font = ImageFont.load_default(size=size)
            except Exception:
                font = ImageFont.load_default()
            x, y = float(el.get('x', 0)), float(el.get('y', 0))
            layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            px, py = apply(m, x, y)
            col = paint.at(0.35) if isinstance(paint, Gradient) else tuple(paint) + (255,)
            ta = float(el.get('opacity', 1)) * a
            anchor = el.get('text-anchor', 'start')
            try:
                tw = d.textlength(txt, font=font) / scale
            except Exception:
                tw = 0.0
            if anchor == 'middle':
                px -= tw / 2
            elif anchor == 'end':
                px -= tw
            d.text((px * scale, py * scale), txt, font=font, fill=col[:3] + (int(255 * ta),), anchor='ls')
            canvas.alpha_composite(layer)

        for child in el:
            walk(child, m, a, inherited, stroke_in)

    walk(root, IDENT, 1.0)

    final = canvas.resize((W, H), Image.LANCZOS)
    bg = Image.new('RGBA', final.size, hex_rgb('#0B0A10') + (255,))
    bg.alpha_composite(final)
    bg.convert('RGB').save(out_path)
    print(f'{out_path}  {W}x{H}')


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2])
