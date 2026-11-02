#!/usr/bin/env python3
"""Search, vet, download, resize fresh images. Reject competitor restoration sites and AI-named files."""
import json, os, re, subprocess, sys
from PIL import Image
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage")
OUT = f"{BASE}/public/images"
os.makedirs(OUT, exist_ok=True)
LOG = f"{BASE}/scripts/image-log.txt"
BAD_HOSTS = ["restoration", "waterdamage", "water-damage", "moldremoval", "plumbing", "damage-restoration"]
BAD_NAME = ["realistic", "ai-generated", "ai_", "_ai", "midjourney", "dall"]

Q = {
 "/": ("flooded living room floor water damage home interior", "Water damage restoration in McDonough, GA",
       "industrial air mover dehumidifier drying wet room", "Structural drying equipment in a McDonough home"),
 "/emergency-water-extraction/": ("water extraction pump removing flood water floor", "Emergency water extraction in McDonough, GA",
       "wet vacuum extracting water from carpet", "Water extraction from carpet in McDonough, GA"),
 "/burst-pipe-water-damage/": ("burst pipe leaking water wall ceiling", "Burst pipe water damage in McDonough, GA",
       "plumber repairing burst pipe", "Burst pipe repair in a McDonough home"),
 "/flood-damage-cleanup/": ("flood water inside house after storm", "Flood damage cleanup in McDonough, GA",
       "storm flooding street houses rain", "Storm flooding near McDonough, GA"),
 "/sewage-backup-cleanup/": ("worker protective suit cleaning disinfection", "Sewage backup cleanup in McDonough, GA",
       "professional cleaning disinfection protective equipment", "Safe sewage cleanup in McDonough, GA"),
 "/ceiling-leak-water-damage/": ("water stain damaged ceiling leak", "Ceiling leak water damage in McDonough, GA",
       "wet ceiling stain roof leak interior", "Roof leak ceiling damage in McDonough, GA"),
 "/mold-remediation/": ("mold on wall after water damage", "Mold remediation in McDonough, GA",
       "worker removing mold wall protective suit", "Mold removal after water damage in McDonough, GA"),
 "/structural-drying/": ("industrial dehumidifier air mover drying room", "Structural drying in McDonough, GA",
       "moisture meter checking wet wall", "Moisture readings during structural drying in McDonough, GA"),
 "/commercial-water-damage/": ("commercial building office water damage floor", "Commercial water damage restoration in McDonough, GA",
       "warehouse office flooded floor cleanup", "Commercial water damage cleanup in McDonough, GA"),
 "/crawl-space-water-damage/": ("crawl space under house water pipes", "Crawl space water damage in McDonough, GA",
       "standing water crawl space foundation", "Crawl space drying in McDonough, GA"),
 "/slab-leak-water-damage/": ("wet tile floor leak under floor", "Slab leak water damage in McDonough, GA",
       "water damage wet floor tiles home", "Slab leak wet floor in McDonough, GA"),
 "/water-heater-leak-cleanup/": ("water heater tank garage leak", "Water heater leak cleanup in McDonough, GA",
       "water heater in garage utility", "Water heater leak in a McDonough garage"),
 "/appliance-leak-water-damage/": ("washing machine leak laundry room floor water", "Appliance leak water damage in McDonough, GA",
       "laundry room washing machine hose", "Washing machine leak in McDonough, GA"),
 "/ac-leak-water-damage/": ("air conditioner attic unit condensate", "AC leak water damage in McDonough, GA",
       "hvac air handler attic", "Attic AC unit in a McDonough home"),
 "/hardwood-floor-water-damage/": ("cupped warped hardwood floor water damage", "Hardwood floor water damage in McDonough, GA",
       "wood floor drying restoration", "Hardwood floor drying in McDonough, GA"),
 "/toilet-overflow-cleanup/": ("bathroom toilet overflow water floor", "Toilet overflow cleanup in McDonough, GA",
       "bathroom water leak floor tiles", "Bathroom leak cleanup in McDonough, GA"),
 "/water-damage-restoration-stockbridge-ga/": ("suburban neighborhood homes street Georgia", "Water damage restoration in Stockbridge, GA",
       "two story suburban home exterior", "Stockbridge, GA home exterior"),
 "/water-damage-restoration-locust-grove-ga/": ("small town Georgia homes neighborhood street", "Water damage restoration in Locust Grove, GA",
       "suburban house front yard Georgia", "Locust Grove, GA home"),
 "/water-damage-restoration-hampton-ga/": ("suburban homes street trees Georgia", "Water damage restoration in Hampton, GA",
       "house exterior driveway Georgia neighborhood", "Hampton, GA home"),
 "/water-damage-restoration-jonesboro-ga/": ("historic small town Georgia street homes", "Water damage restoration in Jonesboro, GA",
       "brick suburban home Georgia", "Jonesboro, GA home"),
 "/water-damage-restoration-lovejoy-ga/": ("new subdivision homes Georgia street", "Water damage restoration in Lovejoy, GA",
       "new suburban home exterior Georgia", "Lovejoy, GA home"),
 "/water-damage-restoration-forest-park-ga/": ("suburban homes Atlanta Georgia neighborhood", "Water damage restoration in Forest Park, GA",
       "ranch home exterior Georgia", "Forest Park, GA home"),
 "/water-damage-restoration-conyers-ga/": ("suburban neighborhood Georgia homes trees", "Water damage restoration in Conyers, GA",
       "two story home Georgia neighborhood", "Conyers, GA home"),
 "/water-damage-restoration-griffin-ga/": ("small city Georgia homes street", "Water damage restoration in Griffin, GA",
       "brick home front porch Georgia", "Griffin, GA home"),
 "/water-damage-restoration-jackson-ga/": ("lake town Georgia homes neighborhood", "Water damage restoration in Jackson, GA",
       "country home Georgia exterior", "Jackson, GA home"),
 "/about-us/": ("water damage restoration team equipment home", "About McDonough Water Damage Restoration",
       "technician moisture meter wall inspection", "Moisture inspection in a McDonough home"),
 "/contact-us/": ("flooded home phone call emergency help", "Emergency water damage help in McDonough, GA",
       "water damage restoration crew equipment", "Water damage crew in McDonough, GA"),
}

def search(query):
    r = subprocess.run(["/opt/hatch/bin/image-search", query, "--max-results", "5"],
                       capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(r.stdout)
    except Exception:
        return []
    return data.get("results", [])

def vet(url):
    if not url or not url.startswith("https://"): return False
    low = url.lower()
    if any(b in low for b in BAD_HOSTS): return False
    if any(b in low for b in BAD_NAME): return False
    if "?" in url and ("fbcdn" in low or "xx.fbcdn" in low): return False
    return True

def download(url, dest):
    # preflight HEAD
    h = subprocess.run(["curl", "-fsSLI", "-A", "Mozilla/5.0", "-H", "Accept: image/png,image/jpeg,image/gif,image/webp,image/*;q=0.5",
                        "-H", "Referer: https://www.google.com/", url], capture_output=True, text=True, timeout=60)
    if h.returncode != 0: return False
    ct = ""
    for line in h.stdout.splitlines():
        if line.lower().startswith("content-type:"): ct = line.split(":", 1)[1].strip()
    if "image" not in ct: return False
    r = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "60", "-A", "Mozilla/5.0",
                        "-H", "Accept: image/png,image/jpeg,image/gif,image/webp,image/*;q=0.5", "-o", dest, url],
                       capture_output=True, text=True, timeout=90)
    if r.returncode != 0: return False
    try:
        with Image.open(dest) as im: im.verify()
    except Exception:
        return False
    return True

def process(src_tmp, dest, maxw, maxh):
    with Image.open(src_tmp) as im:
        im = im.convert("RGB")
        # center crop to target aspect then resize
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

results = {}
log = []
for slug, (hq, ha, sq, sa) in Q.items():
    name = slug.strip("/").replace("/", "-") or "home"
    entry = {}
    for kind, query, alt, maxw, maxh in [("hero", hq, ha, 1200, 900), ("second", sq, sa, 1100, 420)]:
        dest = f"{OUT}/mcdonough-{name}-{kind}.jpg"
        ok = False
        tried = []
        for res in search(query):
            url = res.get("media_url") or res.get("thumbnail_cdn_url")
            tried.append(url)
            if not vet(url): continue
            tmp = dest + ".tmp"
            if download(url, tmp):
                try:
                    size = process(tmp, dest, maxw, maxh)
                    entry[kind] = f"/images/mcdonough-{name}-{kind}.jpg"
                    entry[kind + "Alt"] = alt
                    log.append(f"{slug} {kind}: OK {size} bytes from {url} (source page: {res.get('page_url','')})")
                    ok = True; break
                except Exception as e:
                    log.append(f"{slug} {kind}: process failed {e} for {url}")
            else:
                log.append(f"{slug} {kind}: download/preflight failed {url}")
        if not ok:
            log.append(f"{slug} {kind}: FAILED all candidates tried={tried}")
    results[slug] = {"hero": entry.get("hero", ""), "heroAlt": entry.get("heroAlt", ""),
                     "second": entry.get("second", ""), "secondAlt": entry.get("secondAlt", "")}
json.dump(results, open(f"{BASE}/data/images.json", "w"), indent=1)
open(LOG, "w").write("\n".join(log) + "\n")
print(f"done: {sum(1 for v in results.values() if v['hero'])}/27 hero, {sum(1 for v in results.values() if v['second'])}/27 second")
for l in log: print(l)
