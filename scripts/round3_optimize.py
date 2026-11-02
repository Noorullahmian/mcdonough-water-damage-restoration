#!/usr/bin/env python3
"""ROUND 3 image optimization: resize to rendered box (+retina headroom) and
re-encode progressive JPEG q78, EXIF stripped (PIL does not copy EXIF by default).
- heroes 1200x900 -> 1080x810 (rendered ~523px wide, 2.06x retina)
- seconds 1100x420 -> unchanged size (rendered ~1140px wide banner)
- cards/areas 800x500 -> 720x450 (rendered ~366px wide, 1.97x retina)
Filenames, alts, hashes-in-use unchanged in name; content bytes change (expected).
"""
import os
from PIL import Image
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage/public/images")
def target(name):
    if name.endswith("-hero.jpg"): return (1080, 810)
    if name.endswith("-second.jpg"): return None  # keep size
    return (720, 450)
total_before = total_after = 0
for fn in sorted(os.listdir(BASE)):
    if not fn.endswith(".jpg"): continue
    path = os.path.join(BASE, fn)
    before = os.path.getsize(path)
    with Image.open(path) as im:
        im = im.convert("RGB")
        t = target(fn)
        if t and im.size != t:
            im = im.resize(t, Image.LANCZOS)
        im.save(path, "JPEG", quality=78, optimize=True, progressive=True)
    after = os.path.getsize(path)
    total_before += before; total_after += after
    print(f"{fn:70s} {before:7d} -> {after:7d}  ({100*(after-before)/before:+.1f}%)")
print(f"TOTAL {total_before} -> {total_after}  ({100*(total_after-total_before)/total_before:+.1f}%)  MB {total_before/1e6:.2f} -> {total_after/1e6:.2f}")
