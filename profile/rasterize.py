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
from PIL import Image, ImageChops, ImageDraw, ImageFont

SS = 2  # supersample
BACKDROP = '#0B0A10'


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


FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def load_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    try:
        return ImageFont.truetype(path, max(4, int(size)))
    except Exception:
        try:
            return ImageFont.load_default(size=max(4, int(size)))
        except Exception:
            return ImageFont.load_default()


def stroke_color(raw, grads):
    """Resolve a stroke paint to an RGB tuple, tolerating url(#gradient)."""
    mg = re.match(r'url\(#(.+?)\)', raw or '')
    if mg and mg.group(1) in grads:
        return grads[mg.group(1)].at(0.35)[:3]
    if raw and raw.startswith('#'):
        return hex_rgb(raw)
    return (255, 255, 255)


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
    def __init__(self, kind, stops, cx=0.5, cy=0.5, r=0.5,
                 x1=0.0, y1=0.0, x2=1.0, y2=0.0, spread=None):
        self.kind, self.stops = kind, stops
        self.cx, self.cy, self.r = cx, cy, (r if r else 0.5)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.spread = spread

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

    def image(self, size, box, scale):
        """Rasterise this gradient at device size `size`, bbox-normalised.

        SVG objectBoundingBox semantics: the unit square is stretched to the
        shape's box, so a radial gradient becomes an ellipse, never a circle.
        Getting this wrong paints phantom dark blobs, so it is done properly.
        """
        w, h = max(1, int(size[0])), max(1, int(size[1]))
        at = self.at
        if self.kind == 'radial':
            k = max(2, min(160, max(w, h)))
            small = Image.new('RGBA', (k, k))
            px = small.load()
            cx, cy, r = self.cx, self.cy, self.r
            for j in range(k):
                v = j / (k - 1)
                dy = (v - cy) / r
                row = []
                for i in range(k):
                    u = (i / (k - 1) - cx) / r
                    c = at(math.hypot(u, dy))
                    row.append((c[0], c[1], c[2], int(c[3])))
                for i, c in enumerate(row):
                    px[i, j] = c
            return small.resize((w, h), Image.BICUBIC)
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        den = dx * dx + dy * dy
        if abs(dy) < 1e-6 and den > 0:
            k = max(2, min(160, w))
            strip = Image.new('RGBA', (k, 1))
            px = strip.load()
            for i in range(k):
                c = at(((i / (k - 1)) - self.x1) / dx)
                px[i, 0] = (c[0], c[1], c[2], int(c[3]))
            return strip.resize((w, h), Image.BILINEAR)
        k = max(2, min(160, max(w, h)))
        small = Image.new('RGBA', (k, k))
        px = small.load()
        for j in range(k):
            v = j / (k - 1)
            for i in range(k):
                u = i / (k - 1)
                t = (((u - self.x1) * dx) + ((v - self.y1) * dy)) / den
                c = at(t)
                px[i, j] = (c[0], c[1], c[2], int(c[3]))
        return small.resize((w, h), Image.BICUBIC)

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


def flatten_subpaths(d):
    """Flatten `d` into a list of closed polygons, one per subpath.

    A glyph run is a single <path> with one subpath per contour: the outside
    of an O and its hole, every letter in a word. Treating the whole thing as
    one polygon welds the letters together, so the split is not optional.
    """
    toks = []
    for cmd, num in TOKEN.findall(d):
        toks.append(cmd if cmd else float(num))
    polys, pts = [], []
    cur = start = None
    cmd = None
    i = 0

    def flush():
        nonlocal pts
        if len(pts) >= 3:
            polys.append(pts)
        pts = []

    while i < len(toks):
        t = toks[i]
        if isinstance(t, str):
            cmd = t
            i += 1
            if cmd in 'Zz':
                if start:
                    pts.append(start)
                flush()
                cur = start = None
            continue
        if cmd in 'Mm':
            x, y = toks[i], toks[i + 1]
            i += 2
            flush()
            cur = start = (x, y)
            pts = [cur]
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
            for k in range(1, 17):
                u = k / 16
                v = 1 - u
                pts.append((v**3*p0[0] + 3*v*v*u*x1 + 3*v*u*u*x2 + u**3*x,
                            v**3*p0[1] + 3*v*v*u*y1 + 3*v*u*u*y2 + u**3*y))
            cur = (x, y)
        elif cmd in 'Qq':
            x1, y1, x, y = toks[i:i + 4]
            i += 4
            p0 = cur
            for k in range(1, 13):
                u = k / 12
                v = 1 - u
                pts.append((v*v*p0[0] + 2*v*u*x1 + u*u*x,
                            v*v*p0[1] + 2*v*u*y1 + u*u*y))
            cur = (x, y)
        elif cmd in 'Aa':
            rx, ry, rot, large, sweep, x, y = toks[i:i + 7]
            i += 7
            pts.extend(arc_points(cur, rx, ry, rot, int(large), int(sweep), (x, y)))
            cur = (x, y)
        else:
            i += 1
    flush()
    return polys


def flatten_path(d):
    """Every point of every subpath, in order. Kept for stroke rendering."""
    out = []
    for poly in flatten_subpaths(d):
        out.extend(poly)
    return out


def _signed_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def _point_in_poly(pt, poly):
    """Standard ray cast."""
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1
            if x < xin:
                inside = not inside
    return inside


def _inside_point(poly):
    """A point that is very likely inside the contour, not on its edge."""
    n = len(poly)
    if n < 3:
        return poly[0]
    cx = sum(p[0] for p in poly) / n
    cy = sum(p[1] for p in poly) / n
    if _point_in_poly((cx, cy), poly):
        return (cx, cy)
    # concave shape: nudge toward each vertex, take the first hit
    for p in poly:
        q = ((p[0] + cx) / 2, (p[1] + cy) / 2)
        if _point_in_poly(q, poly):
            return q
    return (cx, cy)


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
                float(el.get('r', 0.5)),
                float(el.get('x1', 0)), float(el.get('y1', 0)),
                float(el.get('x2', 1)), float(el.get('y2', 0)),
                el.get('spreadMethod'),
            )
        elif tag == 'clipPath':
            clips[el.get('id')] = el

    def paint_shape(poly, paint, alpha, m):
        """Fill one or more polygons as a single shape, even-odd.

        Passing a list means the polygons belong to one <path>: the outer
        contour of an O and the hole inside it. Drawing them independently
        fills the hole in, which is how you end up with a word full of
        solid blobs. Here they are combined with XOR, which is exactly what
        the even-odd fill rule does.
        """
        polys = poly if isinstance(poly, list) and poly and isinstance(poly[0], list) else [poly]
        polys = [p for p in polys if p and len(p) >= 3]
        if not polys:
            return
        allp = [apply(m, x, y) for p in polys for x, y in p]
        xs = [p[0] for p in allp]
        ys = [p[1] for p in allp]
        box = (min(xs), min(ys),
               max(max(xs) - min(xs), .001), max(max(ys) - min(ys), .001))

        if isinstance(paint, Gradient):
            bx, by, bw, bh = box
            x0 = max(0, int(bx * scale)); y0 = max(0, int(by * scale))
            x1 = min(canvas.size[0], int((bx + bw) * scale) + 2)
            y1 = min(canvas.size[1], int((by + bh) * scale) + 2)
            if x1 <= x0 or y1 <= y0:
                return
            gimg = paint.image((x1 - x0, y1 - y0), box, scale)
        else:
            x0 = max(0, int(box[0] * scale)); y0 = max(0, int(box[1] * scale))
            x1 = min(canvas.size[0], int((box[0] + box[2]) * scale) + 2)
            y1 = min(canvas.size[1], int((box[1] + box[3]) * scale) + 2)
            if x1 <= x0 or y1 <= y0:
                return
            gimg = Image.new('RGBA', (x1 - x0, y1 - y0),
                             tuple(paint) + (255,))

        # Contours carry their own meaning in the direction they are wound.
        # An outer contour goes one way, the counter inside an 'o' goes the
        # other. Overlapping contours — the stem of a 't' and its crossbar —
        # are wound the SAME way and both belong to the glyph, so they union.
        # Classifying by orientation gets all three cases right; classifying
        # by nesting depth, or by XOR, mangles the overlap.
        tpolys = [[(px * scale - x0, py * scale - y0)
                   for px, py in (apply(m, qx, qy) for qx, qy in p)]
                  for p in polys]
        areas = [abs(_signed_area(p)) for p in tpolys]
        paint_sign = 1
        if areas:
            big = tpolys[areas.index(max(areas))]
            paint_sign = 1 if _signed_area(big) >= 0 else -1

        mask = Image.new('L', (x1 - x0, y1 - y0), 0)
        holes = Image.new('L', (x1 - x0, y1 - y0), 0)
        for p in tpolys:
            a = _signed_area(p)
            same = (a >= 0) == (paint_sign >= 0)
            ImageDraw.Draw(mask if same else holes).polygon(p, fill=255)
        if holes.getbbox():
            mask = ImageChops.subtract(mask, holes)
        if alpha < 0.999:
            ga = gimg.getchannel('A').point(lambda v: int(v * alpha))
            gimg.putalpha(ga)
        ga = gimg.getchannel('A')
        gimg.putalpha(ImageChops.multiply(ga, mask))

        layer = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
        layer.paste(gimg, (0, 0))
        canvas.alpha_composite(layer, (x0, y0))

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

        if tag == 'image':
            href = el.get('href') or el.get('{http://www.w3.org/1999/xlink}href') or ''
            if href.startswith('data:'):
                import base64, io
                head, b64 = href.split(',', 1)
                img = Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGBA')
                iw = float(el.get('width', img.width))
                ih = float(el.get('height', img.height))
                ix = float(el.get('x', 0))
                iy = float(el.get('y', 0))
                px, py = apply(m, ix, iy)
                sx, sy = abs(m[0]), abs(m[3])
                tw, th = max(1, int(iw * sx * scale)), max(1, int(ih * sy * scale))
                img = img.resize((tw, th), Image.LANCZOS)
                if a < 0.999:
                    img.putalpha(img.getchannel('A').point(lambda v: int(v * a)))
                layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
                layer.paste(img, (int(px * scale), int(py * scale)), img)
                canvas.alpha_composite(layer)
        elif tag == 'rect' and paint:
            x, y = float(el.get('x', 0)), float(el.get('y', 0))
            w, h = float(el.get('width', 0)), float(el.get('height', 0))
            paint_shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], paint, a, m)
        elif tag == 'circle' and not paint and el.get('stroke'):
            cx, cy, r = float(el.get('cx', 0)), float(el.get('cy', 0)), float(el.get('r', 0))
            sw = float(el.get('stroke-width', 1))
            layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            raw = el.get('stroke')
            mg = re.match(r'url\(#(.+?)\)', raw or '')
            if mg and mg.group(1) in grads:
                c = grads[mg.group(1)].at(0.35)[:3]
            elif raw and raw.startswith('#'):
                c = hex_rgb(raw)
            else:
                c = (255, 255, 255)
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
                c = stroke_color(el.get('stroke'), grads)
                sa = float(el.get('stroke-opacity', 1)) * a
                d.line([(x * scale, y * scale) for x, y in pts], fill=c + (int(255 * sa),),
                       width=max(1, int(sw * scale)), joint='curve')
                canvas.alpha_composite(layer)
        elif tag == 'path' and paint:
            paint_shape(flatten_subpaths(el.get('d', '')), paint, a, m)
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
            bold = int(float(el.get('font-weight', 400) or 400)) >= 600
            font = load_font(size, bold)
            ls = float(el.get('letter-spacing', 0) or 0) * scale
            x, y = float(el.get('x', 0)), float(el.get('y', 0))
            layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            px, py = apply(m, x, y)
            col = paint.at(0.35) if isinstance(paint, Gradient) else tuple(paint) + (255,)
            ta = float(el.get('opacity', 1)) * a
            anchor = el.get('text-anchor', 'start')
            advances = [d.textlength(ch, font=font) for ch in txt]
            tw = (sum(advances) + ls * max(0, len(txt) - 1)) / scale
            if anchor == 'middle':
                px -= tw / 2
            elif anchor == 'end':
                px -= tw
            cur = px * scale
            for ch, adv in zip(txt, advances):
                d.text((cur, py * scale), ch, font=font, fill=col[:3] + (int(255 * ta),), anchor='ls')
                cur += adv + ls
            canvas.alpha_composite(layer)

        for child in el:
            walk(child, m, a, inherited, stroke_in)

    walk(root, IDENT, 1.0)

    final = canvas.resize((W, H), Image.LANCZOS)
    bg = Image.new('RGBA', final.size, hex_rgb(BACKDROP) + (255,))
    bg.alpha_composite(final)
    bg.convert('RGB').save(out_path)
    print(f'{out_path}  {W}x{H}')


if __name__ == '__main__':
    import sys as _s
    if '--bg' in _s.argv:
        BACKDROP = _s.argv[_s.argv.index('--bg') + 1]
        del _s.argv[_s.argv.index('--bg'):_s.argv.index('--bg') + 2]
    render(_s.argv[1], _s.argv[2])
