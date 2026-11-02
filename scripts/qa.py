#!/usr/bin/env python3
"""QA: screenshots + measurements for every exported page.
Usage: qa.py <round-label> <out-dir>  (serves out/ on 8901)
Measures: H1 count, body font size, H1/H2 colours, overflow at widths,
image natural sizes, map iframe, internal-link targets, title/meta.
"""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
LABEL = sys.argv[1] if len(sys.argv) > 1 else "r1"
SHOTDIR = Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "screenshots" / LABEL
SHOTDIR.mkdir(parents=True, exist_ok=True)

# start static server
PORT = os.environ.get("QA_PORT", "8917")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", str(BASE / "out")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    import urllib.request as _u
    _home = _u.urlopen(f"http://127.0.0.1:{PORT}/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in _home, f"WRONG SERVER on port {PORT}: " + _home[:200]
    from playwright.sync_api import sync_playwright
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for p in PAGES:
            url = f"http://127.0.0.1:{PORT}{p['slug']}"
            slugname = p["slug"].strip("/").replace("/", "-") or "home"
            row = {"slug": p["slug"], "tab": p["tab"]}
            for vw, tag in [(1366, "d"), (390, "m")]:
                ctx = browser.new_context(viewport={"width": vw, "height": 900})
                pg = ctx.new_page()
                pg.goto(url, wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(600)
                # ROUND 2 fix: lazy below-fold images read nw=0 before scrolling; scroll through the page first so measurement reflects real load state.
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(1500)
                pg.evaluate("() => window.scrollTo(0, 0)")
                pg.wait_for_timeout(500)
                m = pg.evaluate("""() => {
                  const h1 = document.querySelectorAll('h1').length;
                  const body = getComputedStyle(document.body);
                  const h1el = document.querySelector('h1');
                  const h2el = document.querySelector('h2');
                  const cs = (el, prop) => el ? getComputedStyle(el)[prop] : '';
                  const over = document.documentElement.scrollWidth - document.documentElement.clientWidth;
                  const imgs = [...document.querySelectorAll('img')].map(i => ({src: i.getAttribute('src'), nw: i.naturalWidth, ok: i.complete && i.naturalWidth > 0}));
                  const maps = document.querySelectorAll('iframe').length;
                  const bad = [];
                  document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && !el.classList.contains('skip') && (r.left < -1 || r.right > document.documentElement.clientWidth + 1)) bad.push(el.tagName + '.' + (el.className.baseVal || el.className || ''));
                  });
                  return {h1, bodySize: body.fontSize, h1Color: cs(h1el,'color'), h1Size: cs(h1el,'fontSize'), h2Color: cs(h2el,'color'), h2Size: cs(h2el,'fontSize'), over, imgs, maps, bad: [...new Set(bad)].slice(0,8), title: document.title, h1Text: h1el ? h1el.textContent.trim() : ''};
                }""")
                row[tag] = m
                pg.screenshot(path=str(SHOTDIR / f"{slugname}-{tag}.png"), full_page=True)
                ctx.close()
            # alignment widths (desktop page, quick)
            align = {}
            for vw in (320, 768, 1024):
                ctx = browser.new_context(viewport={"width": vw, "height": 900})
                pg = ctx.new_page()
                pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(400)
                align[vw] = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                ctx.close()
            row["align"] = align
            # internal links check
            ctx = browser.new_context(viewport={"width": 1366, "height": 900})
            pg = ctx.new_page()
            pg.goto(url, wait_until="domcontentloaded", timeout=60000)
            hrefs = pg.evaluate("() => [...new Set([...document.querySelectorAll('a[href^=\"/\"]')].map(a => a.getAttribute('href')))]")
            ctx.close()
            missing = []
            for h in hrefs:
                path = h.strip("/")
                if path == "": continue
                if not (BASE / "out" / path / "index.html").exists():
                    missing.append(h)
            row["links_missing"] = missing
            row["links"] = len(hrefs)
            results.append(row)
            print(f"{p['slug']} d_over={row['d']['over']} m_over={row['m']['over']} align={align} h1={row['d']['h1']} imgs={[(i['src'], i['ok']) for i in row['d']['imgs']]} maps={row['d']['maps']} missing_links={missing}")
        browser.close()
    json.dump(results, open(SHOTDIR / "measurements.json", "w"), indent=1)
    bad = [r for r in results if r["d"]["over"] != 0 or r["m"]["over"] != 0 or any(v != 0 for v in r["align"].values()) or r["d"]["h1"] != 1 or r["links_missing"]]
    print(f"\nTOTAL {len(results)} pages, FAILING {len(bad)}")
    for r in bad:
        print("FAIL", r["slug"], "d_over", r["d"]["over"], "m_over", r["m"]["over"], "align", r["align"], "h1", r["d"]["h1"], "missing", r["links_missing"])
finally:
    srv.terminate()
