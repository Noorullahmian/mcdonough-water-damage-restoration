#!/usr/bin/env python3
"""Dedicated alignment check: overflow, out-of-bounds, button wrap, chips, cards, tables, sticky header."""
import json, os, subprocess, time
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
OUT = BASE / "screenshots" / "align"
OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen(["python3", "-m", "http.server", "8917", "--directory", str(BASE / "out")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    import urllib.request as _u
    assert "McDonough Water Damage Restoration" in _u.urlopen("http://127.0.0.1:8917/", timeout=10).read().decode("utf-8", "ignore")
    from playwright.sync_api import sync_playwright
    results = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in PAGES:
            url = f"http://127.0.0.1:8917{p['slug']}"
            row = {"slug": p["slug"]}
            for vw in (320, 390, 768, 1024, 1366):
                ctx = b.new_context(viewport={"width": vw, "height": 900})
                pg = ctx.new_page()
                pg.goto(url, wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(300)
                m = pg.evaluate("""() => {
                  const vw = document.documentElement.clientWidth;
                  const over = document.documentElement.scrollWidth - vw;
                  const bad = [];
                  document.querySelectorAll('body *').forEach(el => {
                    if (el.classList.contains('skip')) return;
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && (r.left < -1 || r.right > vw + 1)) bad.push(el.tagName + '.' + (typeof el.className === 'string' ? el.className : ''));
                  });
                  const callBtn = document.querySelector('.hero .btn-call');
                  const callH = callBtn ? Math.round(callBtn.getBoundingClientRect().height) : 0;
                  const chips = [...document.querySelectorAll('.chip')].map(c => ({t: c.textContent, w: Math.round(c.getBoundingClientRect().width)}));
                  const cards = [...document.querySelectorAll('.svc-card')].map(c => Math.round(c.getBoundingClientRect().height));
                  const tables = [...document.querySelectorAll('table')].map(t => Math.round(t.getBoundingClientRect().width));
                  const h1 = document.querySelector('h1');
                  return {over, bad: [...new Set(bad)].slice(0,6), callH, chips, cards: cards.slice(0,6), tables, h1Lines: h1 ? h1.getBoundingClientRect().height : 0};
                }""")
                # sticky check at 1366 only: scroll and see topbar out, header in
                sticky = None
                if vw == 1366:
                    pg.evaluate("() => window.scrollTo(0, 600)")
                    pg.wait_for_timeout(300)
                    sticky = pg.evaluate("""() => {
                      const tb = document.querySelector('.topbar').getBoundingClientRect();
                      const hd = document.querySelector('.site-header').getBoundingClientRect();
                      return {topbarBottom: Math.round(tb.bottom), headerTop: Math.round(hd.top), headerH: Math.round(hd.height)};
                    }""")
                row[str(vw)] = {**m, "sticky": sticky}
                ctx.close()
            results.append(row)
            print(p["slug"], {k: (v["over"], v["bad"], v["callH"]) for k, v in row.items() if k != "slug"}, "sticky:", row["1366"]["sticky"])
        b.close()
    json.dump(results, open(OUT / "align.json", "w"), indent=1)
    fails = []
    for r in results:
        for vw in ("320","390","768","1024","1366"):
            v = r[vw]
            if v["over"] != 0 or v["bad"]: fails.append((r["slug"], vw, v["over"], v["bad"]))
            if v["callH"] > 65: fails.append((r["slug"], vw, "call button wrapped", v["callH"]))
        st = r["1366"]["sticky"]
        if st and st["topbarBottom"] > 0: fails.append((r["slug"], "sticky-topbar-visible", st))
    print("ALIGN FAILS:", fails if fails else "none")
finally:
    srv.terminate()
