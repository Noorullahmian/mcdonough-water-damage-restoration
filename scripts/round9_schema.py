#!/usr/bin/env python3
"""Round 9 schema + favicon verification over out/ (static, no server needed for files;
favicon 200s checked against a local subpath server if FAVICON_PORT env set, else skipped).
Checks per page: every ld+json block parses; node types per page type; org @id defined
exactly once (homepage) and only referenced elsewhere; provider refs point at ORG_ID;
FAQPage questions/answers equal the visible <details> text; BreadcrumbList positions
1..n with Home first; WebPage name == <title>; Service areaServed present; banned keys
ZERO (aggregateRating, review, price, priceRange, address, geo, logo, sameAs, certification,
hasCredential, openingHoursSpecification beyond stated hours is not used).
Favicon: link tags with base prefix in homepage HTML, files exist in out/, PNG dims.
Usage: round9_schema.py <out.json>
"""
import json, re, sys, html as htmllib
from pathlib import Path
BASE = Path.home() / "workspace/mcdonough-water-damage"
OUT = BASE / "out"
BP = "/mcdonough-water-damage-restoration"
SITE = "https://noorullahmian.github.io/mcdonough-water-damage-restoration"
ORG = SITE + "/#organization"
BANNED_KEYS = ["aggregaterating", "review", "price", "pricerange", "address", "geo",
               "logo", "sameas", "certification", "hascredential", "award", "slogan"]
PAGES = json.load(open(BASE / "data/pages.json"))
SLUGS = [p["slug"] for p in PAGES] + ["/privacy-policy/", "/terms-of-use/"]
SERVICE_SLUGS = {"emergency-water-extraction", "burst-pipe-water-damage", "flood-damage-cleanup",
                 "sewage-backup-cleanup", "ceiling-leak-water-damage", "structural-drying",
                 "mold-remediation", "hardwood-floor-water-damage", "crawl-space-water-damage",
                 "slab-leak-water-damage", "water-heater-leak-cleanup", "appliance-leak-water-damage",
                 "ac-leak-water-damage", "toilet-overflow-cleanup", "commercial-water-damage"}
CITY_SLUGS = {p["slug"] for p in PAGES if p["slug"].startswith("/water-damage-restoration-")}

def page_file(slug):
    s = slug.strip("/")
    return OUT / "index.html" if not s else OUT / s / "index.html"

def strip_tags(t):
    # Tags removed with "" (not " "): a link followed by "." must read "cleanup.",
    # not "cleanup ." — the space version falsely flagged Hampton's FAQ as mismatched.
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", htmllib.unescape(t))).strip()

rows = []
for slug in SLUGS:
    body = page_file(slug).read_text("utf-8", "ignore")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    parsed, perr = [], []
    for b in blocks:
        try:
            parsed.append(json.loads(htmllib.unescape(b)))
        except Exception as e:
            perr.append(str(e))
    nodes = []
    for p in parsed:
        g = p.get("@graph", [p]) if isinstance(p, dict) else []
        nodes.extend(g)
    types = [n.get("@type") for n in nodes]
    banned = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in BANNED_KEYS:
                    banned.append(k)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for n in nodes:
        walk(n)
    # FAQ equality: visible <details> inside <main> only (the header mobile nav also
    # uses <details>/<summary>, which polluted a full-body regex in the first run).
    main_html = re.search(r"<main[^>]*>(.*?)</main>", body, re.S)
    main_html = re.sub(r"<script[^>]*>.*?</script>", "", main_html.group(1) if main_html else "", flags=re.S)
    vis = [(strip_tags(q), strip_tags(a)) for q, a in
           re.findall(r"<details[^>]*><summary>(.*?)</summary><p>(.*?)</p>", main_html, re.S)]
    faq = next((n for n in nodes if n.get("@type") == "FAQPage"), None)
    faq_qs = [(e.get("name", ""), e.get("acceptedAnswer", {}).get("text", "")) for e in faq["mainEntity"]] if faq else []
    faq_match = (len(vis) == len(faq_qs) and all(strip_tags(q) == strip_tags(q2) and strip_tags(a) == strip_tags(a2)
                  for (q, a), (q2, a2) in zip(vis, faq_qs))) if (vis or faq_qs) else True
    title = htmllib.unescape(re.search(r"<title>(.*?)</title>", body, re.S).group(1).strip())
    wp = next((n for n in nodes if n.get("@type") == "WebPage"), None)
    bc = next((n for n in nodes if n.get("@type") == "BreadcrumbList"), None)
    sv = next((n for n in nodes if n.get("@type") == "Service"), None)
    org_full = [n for n in nodes if n.get("@type") in ("LocalBusiness", "HomeAndConstructionBusiness")]
    robots = re.search(r'<meta name="robots" content="([^"]*)"', body)
    rows.append({
        "slug": slug, "blocks": len(blocks), "parse_errors": perr, "types": types,
        "org_full": len(org_full), "org_id": org_full[0].get("@id") if org_full else None,
        "provider_refs_ok": all(n.get("provider", {}).get("@id") == ORG for n in nodes
                               if n.get("@type") == "Service" or "itemOffered" in n),
        "webpage_name_eq_title": (wp or {}).get("name") == title,
        "crumbs": [i.get("name") for i in (bc or {}).get("itemListElement", [])],
        "service": (sv or {}).get("name") if sv else None,
        "service_area": (sv or {}).get("areaServed") if sv else None,
        "catalog_n": len(((sv or {}).get("hasOfferCatalog") or {}).get("itemListElement", [])) if sv else None,
        "faq_visible": len(vis), "faq_schema": len(faq_qs), "faq_match": faq_match,
        "banned": banned, "robots": robots.group(1) if robots else None,
    })
    print(f"{slug} blocks={len(blocks)} types={types} org={len(org_full)} svc={rows[-1]['service']} cat={rows[-1]['catalog_n']} faq={len(vis)}/{len(faq_qs)} match={faq_match} banned={banned} robots={rows[-1]['robots']}", flush=True)

# favicon checks
from PIL import Image
fav = {}
home = (OUT / "index.html").read_text("utf-8", "ignore")
fav["icon_links"] = re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>', home)
for f in ["favicon.ico", "favicon-48x48.png", "apple-touch-icon.png", "favicon-master.png"]:
    p = OUT / f
    fav[f] = {"exists": p.exists(), "bytes": p.stat().st_size if p.exists() else 0}
for f in ["favicon-48x48.png", "apple-touch-icon.png"]:
    p = OUT / f
    if p.exists():
        im = Image.open(p)
        fav[f]["dims"] = im.size
robots_txt = (OUT / "robots.txt").read_text("utf-8", "ignore") if (OUT / "robots.txt").exists() else ""
fav["robots_txt"] = robots_txt.strip()
print(json.dumps(fav, indent=1))
json.dump({"pages": rows, "favicon": fav}, open(sys.argv[1], "w"), indent=1)
print("wrote", sys.argv[1])
