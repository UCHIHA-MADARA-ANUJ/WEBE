#!/usr/bin/env python3
"""Catch the SMIL transform-shadowing bug.

An element that has BOTH a `transform` attribute and a direct-child
<animateTransform attributeName="transform"> will have that attribute
*replaced* by the animation (additive="replace" is the default). A group
written as

    <g transform="translate(975,172)">
      <animateTransform type="rotate" from="0 975 172" to="360 975 172"/>
      ...
    </g>

loses its translate the moment the animation starts, and its children are
drawn around the origin instead of around the eye.

The fix is always to nest: translate on the outer group, rotation on an
inner group that rotates about its own local origin.

Run: python3 check_motion.py
"""
import pathlib
import sys
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).parent
SVGS = sorted(p.name for p in HERE.glob("*.svg") if not p.name.startswith("_"))


def local(tag):
    return tag.split("}")[-1]


def scan(path):
    root = ET.parse(path).getroot()
    bad = []

    def walk(el, trail):
        name = local(el.tag)
        here = trail + "/" + name + (f"[@{el.get('id')}]" if el.get("id") else "")
        has_transform = el.get("transform") is not None

        direct_anim = any(
            local(c.tag) == "animateTransform"
            and c.get("attributeName") == "transform"
            and (c.get("additive") or "replace") == "replace"
            for c in el
        )
        if has_transform and direct_anim:
            bad.append((here, el.get("transform")))

        for c in el:
            walk(c, here)

    walk(root, path.name)
    return bad


def main():
    total = 0
    for name in SVGS:
        p = HERE / name
        if not p.exists():
            continue
        hits = scan(p)
        if hits:
            total += len(hits)
            print(f"\n  {name}  —  {len(hits)} transform conflict(s)")
            for where, tr in hits:
                short = where.split("/")[-2:]
                print(f"    {'/'.join(short)}")
                print(f"      transform=\"{tr}\"")
        else:
            print(f"  {name:16s} ok")

    print(f"\n{'FAIL' if total else 'PASS'} — {total} transform-shadowing conflict(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
