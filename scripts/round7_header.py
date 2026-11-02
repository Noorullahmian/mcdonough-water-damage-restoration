#!/usr/bin/env python3
"""Round 5 addendum 2: header-area verification on the NEW call-bar build.
Usage: round7_header.py <out.json>
Serves out/ on QA_PORT or 8948. Fresh browser per page.
Per page x viewport (1366, 1024, 390, 320): header-area screenshot (top 480px),
topbar/call-bar measurements, scroll-away check (header top 0, topbar below viewport),
header-inner overflow, footer stacking columns, tap targets, page overflow.
Plus dropdown hover (1366) and mobile menu open (390).
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "screenshots/round7/header-check.json"
SHOT = BASE / "screenshots/round7/header"
SHOT.mkdir(parents=True, exist_ok=True)
PORT = os.environ.get("QA_PORT", "8948")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", str(BASE / "out")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
TOP_JS = r"""() => {
  const top = document.querySelector('.topbar');
  const call = document.querySelector('.topbar-call');
  const hdr = document.querySelector('.site-header');
  const hi = document.querySelector('.header-inner');
  const foot = document.querySelector('.footer-inner');
  const bar = document.querySelector('.callbar');
  const r = (el) => el ? el.getBoundingClientRect() : null;
  const tr = r(top), cr = r(call), hr = r(hdr), br = r(bar);
  return {
    topbarH: tr ? Math.round(tr.height) : -1,
    topbarText: top ? top.textContent.replace(/\s+/g, ' ').trim().slice(0, 160) : '',
    callH: cr ? Math.round(cr.height) : -1,
    callFont: call ? getComputedStyle(call).fontSize : '',
    callText: call ? call.textContent.trim() : '',
    headerTop: hr ? Math.round(hr.top) : -1,
    headerH: hr ? Math.round(hr.height) : -1,
    topbarBottom: tr ? Math.round(tr.bottom) : -1,
    headerInnerScroll: hi ? hi.scrollWidth : -1,
    headerInnerClient: hi ? hi.clientWidth : -1,
    footerCols: foot ? [...new Set([...foot.children].map(c => Math.round(c.getBoundingClientRect().top)))].length : -1,
    footerBottomSize: document.querySelector('.footer-bottom') ? getComputedStyle(document.querySelector('.footer-bottom')).fontSize : '',
    callbarH: br ? Math.round(br.height) : -1,
    headerCallH: document.querySelector('.header-call') ? Math.round(document.querySelector('.header-call').getBoundingClientRect().height) : -1,
    menuBtnH: document.querySelector('.menu-btn') ? Math.round(document.querySelector('.menu-btn').getBoundingClientRect().height) : -1,
    over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}"""
results = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home, "homepage guard failed"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for p in PAGES:
            slug = p["slug"]; name = slug.strip("/") or "home"
            row = {"slug": slug}
            browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
            try:
                for vw in (1366, 1024, 390, 320):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}{slug}", wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(400)
                    row[f"vw{vw}"] = pg.evaluate(TOP_JS)
                    pg.screenshot(path=str(SHOT / f"{name}-{vw}.png"), clip={"x": 0, "y": 0, "width": vw, "height": 480})
                    if vw == 1366:
                        try:
                            pg.hover(".nav-toggle >> nth=0", timeout=5000); pg.wait_for_timeout(400)
                            row["ddHover"] = pg.evaluate("() => !!document.querySelector('.dropdown')")
                            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                            row["ddEscape"] = pg.evaluate("() => !document.querySelector('.dropdown')")
                        except Exception as e:
                            row["ddHover"] = f"ERR {e}"; row["ddEscape"] = None
                    if vw == 390:
                        try:
                            pg.click(".menu-btn", timeout=5000); pg.wait_for_timeout(400)
                            row["menuOpen"] = pg.evaluate("() => document.querySelector('.mobile-nav').classList.contains('open')")
                        except Exception as e:
                            row["menuOpen"] = f"ERR {e}"
                    pg.evaluate("() => window.scrollTo(0, 1500)"); pg.wait_for_timeout(400)
                    row[f"scroll{vw}"] = pg.evaluate(TOP_JS)
                    ctx.close()
            finally:
                browser.close()
            results.append(row)
            print("done", slug, flush=True)
finally:
    srv.terminate()
OUT.write_text(json.dumps(results, indent=2))
print("wrote", OUT, len(results))
