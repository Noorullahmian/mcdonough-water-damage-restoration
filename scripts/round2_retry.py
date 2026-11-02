#!/usr/bin/env python3
"""ROUND 2 retry: replace pixel/source-rejected card images + missing emergency card.
Stricter vet: host OR page URL containing restoration/servicemaster/plumbing/roofing/
waterdamage/moldremoval is skipped, even punycode/brand hosts are checked via page URL."""
import json, os, subprocess
from PIL import Image
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage")
OUT = f"{BASE}/public/images"
BAD = ["restoration", "waterdamage", "water-damage", "moldremoval", "plumbing", "roofing", "servicemaster", "damage-restoration"]
BAD_NAME = ["realistic", "ai-generated", "ai_", "_ai", "midjourney", "dall", "gemini", "illustration", "cartoon"]
JOBS = {
 "emergency-water-extraction": ["water extraction machine flooded floor home", "firefighters pumping water flooded basement", "wet floor extraction equipment room"],
 "flood-damage-cleanup": ["flooded living room sofa water interior", "house interior flood water furniture"],
 "ceiling-leak-water-damage": ["ceiling water stain leak drip interior", "wet ceiling damage leak home"],
 "structural-drying": ["dehumidifier air mover wet floor drying room", "industrial fan drying wet basement floor"],
 "commercial-water-damage": ["flooded office floor water damage", "warehouse flooded floor water"],
 "slab-leak-water-damage": ["wet floor tiles puddle house interior", "water puddle tile floor leak"],
 "toilet-overflow-cleanup": ["bathroom flooded water floor toilet photo", "toilet leak water bathroom floor"],
}
def search(query):
    r = subprocess.run(["/opt/hatch/bin/image-search", query, "--max-results", "8"],
                       capture_output=True, text=True, timeout=120)
    try: return json.loads(r.stdout).get("results", [])
    except Exception: return []
def vet(url, page):
    s = ((url or "") + " " + (page or "")).lower()
    if not url or not url.startswith("https://"): return False
    if any(b in s for b in BAD): return False
    if any(b in s for b in BAD_NAME): return False
    if "fbcdn" in s or "stockcake.com" in s: return False
    return True
def download(url, dest):
    r = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "60", "-A", "Mozilla/5.0",
                        "-H", "Accept: image/*;q=0.5", "-o", dest, url], capture_output=True, text=True, timeout=90)
    if r.returncode != 0: return False
    try:
        with Image.open(dest) as im: im.verify()
    except Exception: return False
    return True
def process(tmp, dest):
    with Image.open(tmp) as im:
        im = im.convert("RGB"); target = 800/500; w, h = im.size
        if w/h > target:
            nw = int(h*target); x = (w-nw)//2; im = im.crop((x, 0, x+nw, h))
        else:
            nh = int(w/target); y = (h-nh)//2; im = im.crop((0, y, w, y+nh))
        im = im.resize((800, 500), Image.LANCZOS); im.save(dest, "JPEG", quality=82, optimize=True)
    os.remove(tmp); return os.path.getsize(dest)
cards = json.load(open(f"{BASE}/data/card-images.json"))
alts = {
 "emergency-water-extraction": "Emergency Water Extraction in McDonough, GA",
 "flood-damage-cleanup": "Flood Damage Cleanup in McDonough, GA",
 "ceiling-leak-water-damage": "Ceiling Leak Water Damage in McDonough, GA",
 "structural-drying": "Structural Drying in McDonough, GA",
 "commercial-water-damage": "Commercial Water Damage in McDonough, GA",
 "slab-leak-water-damage": "Slab Leak Water Damage in McDonough, GA",
 "toilet-overflow-cleanup": "Toilet Overflow Cleanup in McDonough, GA",
}
log = []
for key, queries in JOBS.items():
    dest = f"{OUT}/mcdonough-card-{key}.jpg"; ok = False
    for q in queries:
        if ok: break
        for res in search(q):
            url = res.get("media_url") or res.get("thumbnail_cdn_url"); page = res.get("page_url", "")
            if not vet(url, page):
                log.append(f"{key}: skip {url}"); continue
            tmp = dest + ".tmp"
            if download(url, tmp):
                try:
                    size = process(tmp, dest)
                    cards[f"card:{key}"] = {"src": f"/images/mcdonough-card-{key}.jpg", "alt": alts[key]}
                    log.append(f"{key}: OK {size} bytes from {url} (page: {page})"); ok = True; break
                except Exception as e:
                    log.append(f"{key}: process failed {e} {url}")
            else:
                log.append(f"{key}: download failed {url}")
    if not ok: log.append(f"{key}: FAILED")
json.dump(cards, open(f"{BASE}/data/card-images.json", "w"), indent=1)
open(f"{BASE}/scripts/round2-retry-log.txt", "w").write("\n".join(log) + "\n")
print("\n".join(log))
