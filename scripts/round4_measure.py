#!/usr/bin/env python3
"""Round 4 measurements only (no screenshots): fresh browser per page.
Usage: round4_measure.py <start> <end> <outfile.json>"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
START, END, OUT = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
PORT = os.environ.get("QA_PORT", "8917")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", str(BASE / "out")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
results = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for p in PAGES[START:END]:
            url = f"http://127.0.0.1:{PORT}{p['slug']}"
            row = {"slug": p["slug"], "tab": p["tab"]}
            browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
            try:
                for vw, tag in [(1366, "d"), (390, "m")]:
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(url, wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(500)
                    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(1000)
                    pg.evaluate("() => window.scrollTo(0, 0)")
                    pg.wait_for_timeout(300)
                    m = pg.evaluate("""() => {
                      const cs = (el, prop) => el ? getComputedStyle(el)[prop] : '';
                      const h1el = document.querySelector('h1'); const h2el = document.querySelector('h2');
                      const heroCall = document.querySelector('.hero .btn-call');
                      const hr = heroCall ? heroCall.getBoundingClientRect() : null;
                      const taps = {};
                      for (const [name, sel] of [['headerCall','.header-call'],['menuBtn','.menu-btn'],['heroCall','.hero .btn-call'],['callbar','.callbar'],['submit','.form-card button']]) {
                        const el = document.querySelector(sel);
                        if (el) { const r = el.getBoundingClientRect(); taps[name] = Math.round(r.height); }
                      }
                      const navT = [...document.querySelectorAll('.nav-toggle')].map(e => Math.round(e.getBoundingClientRect().height));
                      const bad = [];
                      document.querySelectorAll('*').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (r.width > 0 && !el.classList.contains('skip') && (r.left < -1 || r.right > document.documentElement.clientWidth + 1)) bad.push(el.tagName);
                      });
                      const cards = [...document.querySelectorAll('.svc-card')].slice(0, 3).map(e => Math.round(e.getBoundingClientRect().height));
                      return {h1: document.querySelectorAll('h1').length, bodySize: getComputedStyle(document.body).fontSize,
                        h1Color: cs(h1el,'color'), h1Size: cs(h1el,'fontSize'), h2Color: cs(h2el,'color'), h2Size: cs(h2el,'fontSize'),
                        over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                        imgs: [...document.querySelectorAll('img')].map(i => [i.getAttribute('src'), i.complete && i.naturalWidth > 0]),
                        maps: document.querySelectorAll('iframe').length, bad: [...new Set(bad)].slice(0,8),
                        title: document.title, heroCallY: hr ? Math.round(hr.top) : -1,
                        heroCallVisible: hr ? (hr.top < 900 && hr.bottom > 0) : false, taps, navT, cards};
                    }""")
                    row[tag] = m
                    ctx.close()
                align = {}
                for vw in (320, 768, 1024):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                    pg.wait_for_timeout(300)
                    align[vw] = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    ctx.close()
                row["align"] = align
                ctx = browser.new_context(viewport={"width": 1366, "height": 900})
                pg = ctx.new_page()
                pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                hrefs = pg.evaluate("() => [...new Set([...document.querySelectorAll('a[href^=\"/\"]')].map(a => a.getAttribute('href')))]")
                ctx.close()
                missing = []
                for h in hrefs:
                    path = h.strip("/")
                    cand = BASE / "out" / path / "index.html" if path else BASE / "out" / "index.html"
                    if not cand.exists():
                        missing.append(h)
                row["missing_links"] = missing
                row["links"] = len(hrefs)
            finally:
                browser.close()
            results.append(row)
            print(f"{p['slug']} d_over={row['d']['over']} m_over={row['m']['over']} align={row['align']} "
                  f"body={row['d']['bodySize']} h1={row['d']['h1Size']} h2={row['d']['h2Size']} "
                  f"heroY_d={row['d']['heroCallY']} heroY_m={row['m']['heroCallY']} maps={row['d']['maps']} missing={row['missing_links']}", flush=True)
    json.dump(results, open(OUT, "w"), indent=1)
    print("MEASURE DONE", len(results))
finally:
    srv.terminate()
