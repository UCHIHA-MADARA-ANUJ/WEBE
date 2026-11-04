#!/usr/bin/env python3
"""Evaluate an SMIL timeline at an arbitrary time and rasterize the result.

This is the tool that was missing. Without it every frame except t=0 was
invisible, so every animation bug shipped unseen.

It does not attempt to be a browser. It resolves `animate` and
`animateTransform` at time t, writes those values onto their parents as plain
attributes, strips the animation nodes, and hands the result to rasterize.py.

Supported: numeric interpolation, numeric lists (x y / angle cx cy), colours and
everything else as a discrete step, `additive="sum"` on transforms, repeatCount
by wrapping t into the cycle.

    python3 frames.py <svg> <t> <out.png>
    python3 frames.py <svg> --sheet <out.png> t1 t2 t3 ...
"""
import copy
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from PIL import Image

HERE = pathlib.Path(__file__).parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def local(tag):
    return tag.split("}")[-1]


def num_list(s):
    parts = [p for p in re.split(r"[,\s]+", str(s).strip()) if p]
    out = []
    for p in parts:
        try:
            out.append(float(p))
        except ValueError:
            return None
    return out


def interp(a, b, u):
    na, nb = num_list(a), num_list(b)
    if na is not None and nb is not None and len(na) == len(nb):
        vals = [x + (y - x) * u for x, y in zip(na, nb)]
        return " ".join(f"{v:.4f}".rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"
                        for v in vals)
    return a if u < 1.0 else b


def sample(values, keytimes, t):
    vals = values.split(";")
    if len(vals) == 1:
        return vals[0]
    if keytimes:
        kts = [float(x) for x in keytimes.split(";")]
    else:
        kts = [i / (len(vals) - 1) for i in range(len(vals))]
    if len(kts) != len(vals):
        kts = [i / (len(vals) - 1) for i in range(len(vals))]
    if t <= kts[0]:
        return vals[0]
    if t >= kts[-1]:
        return vals[-1]
    for i in range(len(kts) - 1):
        if kts[i] <= t <= kts[i + 1]:
            span = kts[i + 1] - kts[i]
            u = 0.0 if span <= 0 else (t - kts[i]) / span
            return interp(vals[i], vals[i + 1], u)
    return vals[-1]


def anim_time(el, t):
    """Wrap t into the element's own duration / begin offset."""
    dur = el.get("dur", "")
    m = re.fullmatch(r"([\d.]+)s", dur)
    begin = 0.0
    bm = re.match(r"([\d.]+)s", el.get("begin", "0s") or "0s")
    if bm:
        begin = float(bm.group(1))
    tt = t - begin
    if tt < 0:
        return None
    if m:
        d = float(m.group(1))
        if d > 0:
            if el.get("repeatCount") in ("indefinite", None):
                tt = tt % d
            else:
                tt = min(tt, d)
            # keyTimes are FRACTIONS of dur, not seconds
            return tt / d
    return tt


def _drop(parent, child):
    """Remove an animate node without losing the text that follows it."""
    if child.tail:
        kids = list(parent)
        i = kids.index(child)
        if i > 0:
            pv = kids[i - 1]
            pv.tail = (pv.tail or "") + child.tail
        else:
            parent.text = (parent.text or "") + child.tail
    parent.remove(child)


def resolve(root, t):
    for parent in list(root.iter()):
        for child in list(parent):
            if local(child.tag) not in ("animate", "animateTransform"):
                continue
            tt = anim_time(child, t)
            if tt is None:
                _drop(parent, child)
                continue

            vals, kts = child.get("values"), child.get("keyTimes")
            if vals:
                v = sample(vals, kts, tt)
            else:
                frm, to = child.get("from"), child.get("to")
                v = frm if tt <= 0 else to

            if local(child.tag) == "animateTransform":
                typ = child.get("type", "translate")
                cur = parent.get("transform") or ""
                if (child.get("additive") or "replace") == "sum" and cur:
                    parent.set("transform", f"{cur} {typ}({v})")
                else:
                    parent.set("transform", f"{typ}({v})")
            else:
                attr = child.get("attributeName")
                if attr:
                    parent.set(attr, v)
            _drop(parent, child)

    for el in root.iter():
        for child in list(el):
            if local(child.tag) in ("animate", "animateTransform"):
                el.remove(child)
    return root


def snapshot(svg_path, t, out_svg):
    tree = ET.parse(svg_path)
    root = resolve(tree.getroot(), t)
    tree.write(out_svg, encoding="unicode", xml_declaration=False)
    return out_svg


def render(svg_path, t, out_png):
    tmp = pathlib.Path(f"/tmp/_snap_{abs(hash((str(svg_path), t))) % 10**8}.svg")
    snapshot(svg_path, t, tmp)
    subprocess.run([sys.executable, str(HERE / "rasterize.py"), str(tmp), str(out_png)],
                   check=True, capture_output=True)
    tmp.unlink(missing_ok=True)
    return out_png


def sheet(svg_path, times, out_png, cols=2, scale=0.5):
    frames = [Image.open(render(svg_path, t, f"/tmp/_f{i}.png")) for i, t in enumerate(times)]
    w, h = frames[0].size
    tw, th = int(w * scale), int(h * scale)
    rows = (len(frames) + cols - 1) // cols
    pad = 8
    canvas = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                               rows * th + (rows + 1) * pad), (12, 10, 14))
    for i, im in enumerate(frames):
        c, r = i % cols, i // cols
        canvas.paste(im.resize((tw, th), Image.LANCZOS),
                     (pad + c * (tw + pad), pad + r * (th + pad)))
    canvas.save(out_png)
    return out_png


if __name__ == "__main__":
    svg = sys.argv[1]
    if sys.argv[2] == "--sheet":
        times = [float(x) for x in sys.argv[4:]]
        p = sheet(svg, times, sys.argv[3])
        print(p, f"{len(times)} frames")
    else:
        p = render(svg, float(sys.argv[2]), sys.argv[3])
        print(p, sys.argv[2] + "s")
