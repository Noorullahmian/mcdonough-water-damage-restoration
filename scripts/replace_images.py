#!/usr/bin/env python3
"""Replacement round: stricter source denylist, generic queries."""
import json, os, subprocess
from PIL import Image
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage")
OUT = f"{BASE}/public/images"
LOG = f"{BASE}/scripts/image-log2.txt"
DENY = ["restor", "plumb", "roof", "foundation", "exterior", "realty", "realtor", "listing", "idx",
        "mls", "gofundme", "pinimg", "ytimg", "leadconnector", "msgsndr", "marblism", "surferseo",
        "heyflow", "squarespace", "snappyscout", "cirrussystem", "brivity", "marketleader",
        "homelight", "goldpeach", "thesparksite", "knowatlanta", "akamaized", "socialistsanddemocrats",
        "ivu.ro", "hvac", "airperfection", "gdimprovement", "myersexteriors", "jluservices",
        "spectrumplumbing", "kennypage", "readyrooter", "leakingshower", "disaster-experts",
        "thefreshair", "planpreparehome", "atlantic-foundation", "aceroofing", "puroclean",
        "rescueclean", "rhino-", "restoreadvisor", "peachtreecorners", "homesbymarco", "sierrastatic",
        "showingnew", "d2g8igdw", "d2xsxph", "onekindesign", "nomadlawyer", "exploregeorgia"]
# NOTE: nomadlawyer/exploregeorgia/onekindesign are kept slots; they are in DENY only to force
# re-search for slots that reference them, not to delete kept files. Kept files are untouched.
REPLACE = {
 "/": ("hero", "wet wooden floor water puddle home"),
 "/emergency-water-extraction/": ("hero", "wet floor water pump hose"),
 "/emergency-water-extraction/": ("second", "mop bucket cleaning wet floor"),
 "/burst-pipe-water-damage/": ("hero", "leaking pipe water drip wall"),
 "/burst-pipe-water-damage/": ("second", "water dripping ceiling bucket"),
 "/flood-damage-cleanup/": ("hero", "flooded street houses rain storm"),
 "/flood-damage-cleanup/": ("second", "muddy flood water house porch"),
 "/sewage-backup-cleanup/": ("hero", "hazmat suit worker cleaning disinfection"),
 "/sewage-backup-cleanup/": ("second", "rubber gloves cleaning bathroom"),
 "/ceiling-leak-water-damage/": ("hero", "brown water stain ceiling"),
 "/ceiling-leak-water-damage/": ("second", "attic roof leak insulation wet"),
 "/mold-remediation/": ("hero", "black mold spots wall corner"),
 "/mold-remediation/": ("second", "moldy wall bathroom moisture"),
 "/structural-drying/": ("hero", "dehumidifier machine drying room"),
 "/structural-drying/": ("second", "fan blower drying wet floor"),
 "/commercial-water-damage/": ("hero", "office building lobby interior"),
 "/commercial-water-damage/": ("second", "warehouse empty floor interior"),
 "/crawl-space-water-damage/": ("hero", "dark crawl space dirt floor house"),
 "/crawl-space-water-damage/": ("second", "house foundation crawl space vent"),
 "/slab-leak-water-damage/": ("second", "concrete floor crack water"),
 "/water-heater-leak-cleanup/": ("second", "water heater tank basement utility room"),
 "/appliance-leak-water-damage/": ("hero", "laundry room washing machine floor"),
 "/ac-leak-water-damage/": ("hero", "air conditioner unit wall home"),
 "/ac-leak-water-damage/": ("second", "attic insulation ceiling"),
 "/hardwood-floor-water-damage/": ("hero", "wooden floor planks close up"),
 "/toilet-overflow-cleanup/": ("hero", "bathroom toilet floor tiles"),
 "/toilet-overflow-cleanup/": ("second", "bathroom shower tiles water"),
 "/water-damage-restoration-stockbridge-ga/": ("hero", "suburban street houses trees USA"),
 "/water-damage-restoration-stockbridge-ga/": ("second", "two story brick house front yard"),
 "/water-damage-restoration-locust-grove-ga/": ("hero", "small town main street USA"),
 "/water-damage-restoration-locust-grove-ga/": ("second", "suburban house driveway neighborhood"),
 "/water-damage-restoration-hampton-ga/": ("hero", "residential street houses trees"),
 "/water-damage-restoration-hampton-ga/": ("second", "brick ranch house front porch"),
 "/water-damage-restoration-jonesboro-ga/": ("second", "historic downtown street small town"),
 "/water-damage-restoration-lovejoy-ga/": ("hero", "new houses subdivision street"),
 "/water-damage-restoration-lovejoy-ga/": ("second", "suburban home garage driveway"),
 "/water-damage-restoration-forest-park-ga/": ("hero", "suburban neighborhood aerial view houses"),
 "/water-damage-restoration-forest-park-ga/": ("second", "single story house lawn street"),
 "/water-damage-restoration-conyers-ga/": ("hero", "georgia small town street buildings"),
 "/water-damage-restoration-conyers-ga/": ("second", "house porch rocking chairs southern"),
 "/water-damage-restoration-griffin-ga/": ("second", "victorian house small town street"),
 "/water-damage-restoration-jackson-ga/": ("hero", "rural georgia road houses trees"),
 "/about-us/": ("hero", "home inspection worker clipboard house"),
 "/about-us/": ("second", "technician checking wall moisture meter"),
 "/contact-us/": ("hero", "person calling phone emergency home"),
 "/contact-us/": ("second", "flooded basement stairs water"),
}
# fix duplicate keys: build list properly
REPLACE_LIST = [
 ("/", "hero", "wet wooden floor water puddle home"),
 ("/emergency-water-extraction/", "hero", "wet floor water pump hose"),
 ("/emergency-water-extraction/", "second", "mop bucket cleaning wet floor"),
 ("/burst-pipe-water-damage/", "hero", "leaking pipe water drip wall"),
 ("/burst-pipe-water-damage/", "second", "water dripping ceiling bucket"),
 ("/flood-damage-cleanup/", "hero", "flooded street houses rain storm"),
 ("/flood-damage-cleanup/", "second", "muddy flood water house porch"),
 ("/sewage-backup-cleanup/", "hero", "hazmat suit worker cleaning disinfection"),
 ("/sewage-backup-cleanup/", "second", "rubber gloves cleaning bathroom"),
 ("/ceiling-leak-water-damage/", "hero", "brown water stain ceiling"),
 ("/ceiling-leak-water-damage/", "second", "attic roof leak insulation wet"),
 ("/mold-remediation/", "hero", "black mold spots wall corner"),
 ("/mold-remediation/", "second", "moldy wall bathroom moisture"),
 ("/structural-drying/", "hero", "dehumidifier machine drying room"),
 ("/structural-drying/", "second", "fan blower drying wet floor"),
 ("/commercial-water-damage/", "hero", "office building lobby interior"),
 ("/commercial-water-damage/", "second", "warehouse empty floor interior"),
 ("/crawl-space-water-damage/", "hero", "dark crawl space dirt floor house"),
 ("/crawl-space-water-damage/", "second", "house foundation crawl space vent"),
 ("/slab-leak-water-damage/", "second", "concrete floor crack water"),
 ("/water-heater-leak-cleanup/", "second", "water heater tank basement utility room"),
 ("/appliance-leak-water-damage/", "hero", "laundry room washing machine floor"),
 ("/ac-leak-water-damage/", "hero", "air conditioner unit wall home"),
 ("/ac-leak-water-damage/", "second", "attic insulation ceiling"),
 ("/hardwood-floor-water-damage/", "hero", "wooden floor planks close up"),
 ("/toilet-overflow-cleanup/", "hero", "bathroom toilet floor tiles"),
 ("/toilet-overflow-cleanup/", "second", "bathroom shower tiles water"),
 ("/water-damage-restoration-stockbridge-ga/", "hero", "suburban street houses trees USA"),
 ("/water-damage-restoration-stockbridge-ga/", "second", "two story brick house front yard"),
 ("/water-damage-restoration-locust-grove-ga/", "hero", "small town main street USA"),
 ("/water-damage-restoration-locust-grove-ga/", "second", "suburban house driveway neighborhood"),
 ("/water-damage-restoration-hampton-ga/", "hero", "residential street houses trees"),
 ("/water-damage-restoration-hampton-ga/", "second", "brick ranch house front porch"),
 ("/water-damage-restoration-jonesboro-ga/", "second", "historic downtown street small town"),
 ("/water-damage-restoration-lovejoy-ga/", "hero", "new houses subdivision street"),
 ("/water-damage-restoration-lovejoy-ga/", "second", "suburban home garage driveway"),
 ("/water-damage-restoration-forest-park-ga/", "hero", "suburban neighborhood aerial view houses"),
 ("/water-damage-restoration-forest-park-ga/", "second", "single story house lawn street"),
 ("/water-damage-restoration-conyers-ga/", "hero", "georgia small town street buildings"),
 ("/water-damage-restoration-conyers-ga/", "second", "house porch rocking chairs southern"),
 ("/water-damage-restoration-griffin-ga/", "second", "victorian house small town street"),
 ("/water-damage-restoration-jackson-ga/", "hero", "rural georgia road houses trees"),
 ("/about-us/", "hero", "home inspection worker clipboard house"),
 ("/about-us/", "second", "technician checking wall moisture meter"),
 ("/contact-us/", "hero", "person calling phone emergency home"),
 ("/contact-us/", "second", "flooded basement stairs water"),
]
ALTS = {}
orig = json.load(open(f"{BASE}/data/images.json"))
for slug, v in orig.items():
    ALTS[(slug, "hero")] = v.get("heroAlt", "")
    ALTS[(slug, "second")] = v.get("secondAlt", "")
# missing alts
ALTS[("/hardwood-floor-water-damage/", "hero")] = "Hardwood floor water damage in McDonough, GA"
ALTS[("/about-us/", "hero")] = "About McDonough Water Damage Restoration"
ALTS[("/contact-us/", "second")] = "Water damage crew in McDonough, GA"

def search(query):
    r = subprocess.run(["/opt/hatch/bin/image-search", query, "--max-results", "5"], capture_output=True, text=True, timeout=120)
    try: return json.loads(r.stdout).get("results", [])
    except Exception: return []

def vet(url):
    if not url or not url.startswith("https://"): return False
    low = url.lower()
    if any(b in low for b in DENY): return False
    if any(b in low for b in ["realistic", "gemini_generated", "generated_image", "midjourney", "dall"]): return False
    if "fbcdn" in low: return False
    return True

def download(url, dest):
    h = subprocess.run(["curl", "-fsSLI", "-A", "Mozilla/5.0", "-H", "Accept: image/*", "-H", "Referer: https://www.google.com/", url], capture_output=True, text=True, timeout=60)
    if h.returncode != 0: return False
    if not any(l.lower().startswith("content-type:") and "image" in l.lower() for l in h.stdout.splitlines()): return False
    r = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "60", "-A", "Mozilla/5.0", "-H", "Accept: image/*", "-o", dest, url], capture_output=True, text=True, timeout=90)
    if r.returncode != 0: return False
    try:
        with Image.open(dest) as im: im.verify()
    except Exception: return False
    return True

def process(src_tmp, dest, maxw, maxh):
    with Image.open(src_tmp) as im:
        im = im.convert("RGB")
        target = maxw / maxh; w, h = im.size
        if w / h > target:
            nw = int(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
        im = im.resize((maxw, maxh), Image.LANCZOS)
        im.save(dest, "JPEG", quality=82, optimize=True)
    os.remove(src_tmp)
    return os.path.getsize(dest)

log = []
results = orig
for slug, kind, query in REPLACE_LIST:
    name = slug.strip("/").replace("/", "-") or "home"
    dest = f"{OUT}/mcdonough-{name}-{kind}.jpg"
    maxw, maxh = (1200, 900) if kind == "hero" else (1100, 420)
    ok = False
    for res in search(query):
        url = res.get("media_url") or res.get("thumbnail_cdn_url")
        if not vet(url):
            log.append(f"{slug} {kind}: rejected {url}"); continue
        tmp = dest + ".tmp"
        if download(url, tmp):
            try:
                size = process(tmp, dest, maxw, maxh)
                results[slug][kind] = f"/images/mcdonough-{name}-{kind}.jpg"
                results[slug][kind + "Alt"] = ALTS.get((slug, kind), "")
                log.append(f"{slug} {kind}: OK {size} bytes from {url} (page: {res.get('page_url','')})")
                ok = True; break
            except Exception as e:
                log.append(f"{slug} {kind}: process failed {e} {url}")
        else:
            log.append(f"{slug} {kind}: download failed {url}")
    if not ok:
        log.append(f"{slug} {kind}: FAILED query={query}")
json.dump(results, open(f"{BASE}/data/images.json", "w"), indent=1)
open(LOG, "w").write("\n".join(log) + "\n")
print(f"done hero {sum(1 for v in results.values() if v['hero'])}/27 second {sum(1 for v in results.values() if v['second'])}/27")
for l in log: print(l)
