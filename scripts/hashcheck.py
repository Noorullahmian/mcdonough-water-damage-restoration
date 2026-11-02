#!/usr/bin/env python3
"""Check downloaded images do not hash-match any other site image in ~/workspace."""
import hashlib, os, sys
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage/public/images")
def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
mine = {}
for f in sorted(os.listdir(BASE)):
    if f.endswith(".jpg"):
        mine[md5(os.path.join(BASE, f))] = f
print(f"my images: {len(mine)}")
collisions = []
root = os.path.expanduser("~/workspace")
skip = {"node_modules", "out", "screenshots", ".git", "mcdonough-water-damage"}
count = 0
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]
    for fn in filenames:
        if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            p = os.path.join(dirpath, fn)
            try:
                h = md5(p)
            except Exception:
                continue
            count += 1
            if h in mine:
                collisions.append((mine[h], p))
print(f"scanned other-site images: {count}")
print("COLLISIONS:", collisions if collisions else "none")
