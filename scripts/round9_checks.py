#!/usr/bin/env python3
"""Round 8 static HTML checks (AUDIT-LIST-10X checks 1, 2, 12).
Serves out/ on QA_PORT (default 8955), homepage-title guard first, then per page:
HTTP 200, real H1, every <img> src resolves in out/, no width/height attrs on <img>,
banned phrases ZERO, no bracket markers visible, titles <=60 / metas <=160 (decoded),
no body (<main>) self-links. Usage: round8_checks.py <out.json>
"""
import html, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
PAGES = PAGES + [{"slug": "/privacy-policy/", "tab": 0}, {"slug": "/terms-of-use/", "tab": 0}]

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "screenshots/round9/checks.json"
PORT = os.environ.get("QA_PORT", "8968")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", "/tmp/r9test"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home and "<h1" in home, "HOMEPAGE GUARD FAILED"
    print("guard OK on port", PORT)
    rows = []
    for p in PAGES:
        slug = p["slug"]
        url = f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration{slug}"
        try:
            resp = urllib.request.urlopen(url, timeout=15)
            status, body = resp.status, resp.read().decode("utf-8", "ignore")
        except Exception as e:
            rows.append({"slug": slug, "error": str(e)}); continue
        title = html.unescape(re.search(r"<title>(.*?)</title>", body, re.S).group(1).strip()) if re.search(r"<title>(.*?)</title>", body, re.S) else ""
        m = re.search(r'<meta name="description" content="([^"]*)"', body)
        meta = html.unescape(m.group(1)) if m else ""
        h1n = len(re.findall(r"<h1[\s>]", body))
        imgs = re.findall(r"<img\b([^>]*)>", body)
        srcs = [re.search(r'src="([^"]+)"', t).group(1) for t in imgs if re.search(r'src="([^"]+)"', t)]
        missing = [s for s in srcs if not (BASE / "out" / s.replace("/mcdonough-water-damage-restoration/","",1).lstrip("/")).exists() and not s.startswith("http")]
        attributed = [t for t in imgs if re.search(r"\b(width|height)=", t)]
        low = re.sub(r"<[^>]+>", " ", body).lower()
        banned = [w for w in ("free estimate", "certified", "licensed") if w in low]
        markers = [w for w in ("Button:", "Tagline:", "Trust points") if w in body]
        main = re.search(r"<main[^>]*>(.*?)</main>", body, re.S)
        main_html = main.group(1) if main else ""
        hrefs = re.findall(r'href="([^"]+)"', main_html)
        norm = lambda h: h if h.endswith("/") else h + "/"
        selflinks = [h for h in hrefs if norm(h) == norm(slug) and not h.startswith("#")]
        maps = len(re.findall(r"<iframe", body))
        rows.append({"slug": slug, "status": status, "title": title, "title_len": len(title),
                     "meta_len": len(meta), "h1n": h1n, "imgs": len(srcs), "missing": missing,
                     "attributed_imgs": len(attributed), "banned": banned, "markers": markers,
                     "selflinks": selflinks, "maps": maps})
        print(f"{slug} {status} h1={h1n} imgs={len(srcs)} missing={len(missing)} attr={len(attributed)} banned={banned} markers={markers} self={selflinks} maps={maps} title={len(title)} meta={len(meta)}", flush=True)
    json.dump(rows, open(OUT, "w"), indent=1)
    print("wrote", OUT, len(rows))
finally:
    srv.terminate()
