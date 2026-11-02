#!/usr/bin/env python3
import json, os, re, shutil
BASE = os.path.expanduser("~/workspace/mcdonough-water-damage")
pages = json.load(open(f"{BASE}/data/pages.json"))
try:
    images = json.load(open(f"{BASE}/data/images.json"))
except FileNotFoundError:
    images = {}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

def city_of(p):
    m = re.search(r"in (.+), GA", p["h1"])
    return f"{m.group(1)}, GA" if m else "McDonough, GA"

for p in pages:
    slug = p["slug"].strip("/")
    if slug:
        d = f"{BASE}/app/{slug}"
    else:
        d = f"{BASE}/app"
    os.makedirs(d, exist_ok=True)
    img = images.get(p["slug"], {})
    if p["slug"] == "/":
        eyebrow = "Open 24 Hours · McDonough & Henry County"; place = "McDonough, GA"
    elif p["tab"] >= 17 and p["tab"] <= 25:
        place = city_of(p); eyebrow = f"{place} · Open 24 Hours"
    else:
        place = "McDonough, GA"; eyebrow = "McDonough, GA · Open 24 Hours"
    code = f'''import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type {{ Metadata }} from "next";

export const metadata: Metadata = {{
  title: "{esc(p["title"])}",
  description: "{esc(p["meta"])}",
}};

export default function Page() {{
  const page = (pages as any[]).find((x) => x.slug === "{p["slug"]}");
  return (
    <PageRenderer
      page={{page}}
      heroImg={{"{img.get('hero','')}" || undefined}}
      heroAlt={{"{esc(img.get('heroAlt',''))}" || undefined}}
      secondImg={{"{img.get('second','')}" || undefined}}
      secondAlt={{"{esc(img.get('secondAlt',''))}" || undefined}}
      mapPlace={{"{place}"}}
      mapTitle={{"Map of {place}"}}
      eyebrow={{"{eyebrow}"}}
    />
  );
}}
'''
    # fix: for homepage the relative path is ../components, not ../../
    if slug == "":
        code = code.replace('"../../components/PageRenderer"', '"../components/PageRenderer"').replace('"../../data/pages.json"', '"../data/pages.json"')
    open(f"{d}/page.tsx", "w").write(code)
open(f"{BASE}/public/robots.txt", "w").write("User-agent: *\nAllow: /\n")
print(f"generated {len(pages)} page files")
