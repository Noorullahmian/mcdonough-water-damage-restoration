#!/usr/bin/env python3
"""ROUND 2: fresh photographic images for homepage service cards (15) + area cards (9).
Same vetting as images.py: reject competitor/restoration/plumbing hosts and AI-named files.
Output: public/images/mcdonough-card-*.jpg + mcdonough-area-*.jpg (800x500, JPEG 82),
and data/card-images.json {service-slug: {src, alt}, area-city-slug: {src, alt}}."""
import json, os, subprocess
from PIL import Image
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage")
OUT = f"{BASE}/public/images"
os.makedirs(OUT, exist_ok=True)
LOG = f"{BASE}/scripts/round2-image-log.txt"
BAD_HOSTS = ["restoration", "waterdamage", "water-damage", "moldremoval", "plumbing", "damage-restoration"]
BAD_NAME = ["realistic", "ai-generated", "ai_", "_ai", "midjourney", "dall", "gemini"]

CARDS = {
 "emergency-water-extraction": ("workers extracting water flooded room equipment", "Emergency Water Extraction in McDonough, GA"),
 "burst-pipe-water-damage": ("broken pipe spraying water basement wall", "Burst Pipe Water Damage in McDonough, GA"),
 "flood-damage-cleanup": ("flood water inside living room furniture", "Flood Damage Cleanup in McDonough, GA"),
 "sewage-backup-cleanup": ("protective worker sanitizing floor disinfection", "Sewage Backup Cleanup in McDonough, GA"),
 "ceiling-leak-water-damage": ("water damaged ceiling stain dripping", "Ceiling Leak Water Damage in McDonough, GA"),
 "mold-remediation": ("black mold wall corner water damage", "Mold Remediation in McDonough, GA"),
 "structural-drying": ("air movers fans drying wet concrete floor room", "Structural Drying in McDonough, GA"),
 "commercial-water-damage": ("office building flooded lobby floor water", "Commercial Water Damage in McDonough, GA"),
 "crawl-space-water-damage": ("crawl space dirt floor pipes under house", "Crawl Space Water Damage in McDonough, GA"),
 "slab-leak-water-damage": ("tile floor water puddle leak home interior", "Slab Leak Water Damage in McDonough, GA"),
 "water-heater-leak-cleanup": ("water heater tank leaking puddle garage floor", "Water Heater Leak Cleanup in McDonough, GA"),
 "appliance-leak-water-damage": ("washing machine water leak laundry room floor", "Appliance Leak Water Damage in McDonough, GA"),
 "ac-leak-water-damage": ("air conditioning unit ceiling water stain", "AC Leak Water Damage in McDonough, GA"),
 "hardwood-floor-water-damage": ("warped cupped wood floor planks water damage", "Hardwood Floor Water Damage in McDonough, GA"),
 "toilet-overflow-cleanup": ("toilet overflowing water bathroom floor", "Toilet Overflow Cleanup in McDonough, GA"),
}
AREAS = {
 "stockbridge-ga": ("suburban brick house Georgia front yard", "Water damage restoration in Stockbridge, GA"),
 "locust-grove-ga": ("small town Georgia homes neighborhood street", "Water damage restoration in Locust Grove, GA"),
 "hampton-ga": ("Georgia suburban home driveway trees", "Water damage restoration in Hampton, GA"),
 "jonesboro-ga": ("historic Georgia town street homes", "Water damage restoration in Jonesboro, GA"),
 "lovejoy-ga": ("new subdivision Georgia homes street", "Water damage restoration in Lovejoy, GA"),
 "forest-park-ga": ("ranch style house Atlanta Georgia neighborhood", "Water damage restoration in Forest Park, GA"),
 "conyers-ga": ("two story house Georgia trees neighborhood", "Water damage restoration in Conyers, GA"),
 "griffin-ga": ("brick house front porch Georgia small town", "Water damage restoration in Griffin, GA"),
 "jackson-ga": ("country house Georgia road neighborhood", "Water damage restoration in Jackson, GA"),
}

def search(query):
    r = subprocess.run(["/opt/hatch/bin/image-search", query, "--max-results", "5"],
                       capture_output=True, text=True, timeout=120)
    try:
        return json.loads(r.stdout).get("results", [])
    except Exception:
        return []

def vet(url):
    if not url or not url.startswith("https://"): return False
    low = url.lower()
    if any(b in low for b in BAD_HOSTS): return False
    if any(b in low for b in BAD_NAME): return False
    if "fbcdn" in low: return False
    return True

def download(url, dest):
    h = subprocess.run(["curl", "-fsSLI", "-A", "Mozilla/5.0", "-H", "Accept: image/*;q=0.5",
                        "-H", "Referer: https://www.google.com/", url], capture_output=True, text=True, timeout=60)
    if h.returncode != 0: return False
    if "image" not in "\n".join(h.stdout.splitlines()).lower() and not any(
            l.lower().startswith("content-type:") and "image" in l.lower() for l in h.stdout.splitlines()):
        # fall through: some servers omit content-type on HEAD; try GET anyway
        pass
    r = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "60", "-A", "Mozilla/5.0",
                        "-H", "Accept: image/*;q=0.5", "-o", dest, url],
                       capture_output=True, text=True, timeout=90)
    if r.returncode != 0: return False
    try:
        with Image.open(dest) as im: im.verify()
    except Exception:
        return False
    return True

def process(src_tmp, dest, maxw=800, maxh=500):
    with Image.open(src_tmp) as im:
        im = im.convert("RGB")
        target = maxw / maxh
        w, h = im.size
        if w / h > target:
            nw = int(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
        im = im.resize((maxw, maxh), Image.LANCZOS)
        im.save(dest, "JPEG", quality=82, optimize=True)
    os.remove(src_tmp)
    return os.path.getsize(dest)

results, log = {}, []
for kind, mapping, prefix in [("card", CARDS, "card"), ("area", AREAS, "area")]:
    for key, (query, alt) in mapping.items():
        dest = f"{OUT}/mcdonough-{prefix}-{key}.jpg"
        ok = False
        for res in search(query):
            url = res.get("media_url") or res.get("thumbnail_cdn_url")
            if not vet(url):
                log.append(f"{prefix}/{key}: skip vet {url}"); continue
            tmp = dest + ".tmp"
            if download(url, tmp):
                try:
                    size = process(tmp, dest)
                    results[f"{prefix}:{key}"] = {"src": f"/images/mcdonough-{prefix}-{key}.jpg", "alt": alt}
                    log.append(f"{prefix}/{key}: OK {size} bytes from {url} (page: {res.get('page_url','')})")
                    ok = True; break
                except Exception as e:
                    log.append(f"{prefix}/{key}: process failed {e} for {url}")
            else:
                log.append(f"{prefix}/{key}: download failed {url}")
        if not ok:
            log.append(f"{prefix}/{key}: FAILED")
json.dump(results, open(f"{BASE}/data/card-images.json", "w"), indent=1)
open(LOG, "w").write("\n".join(log) + "\n")
print(f"done: {len(results)}/24")
for l in log: print(l)
