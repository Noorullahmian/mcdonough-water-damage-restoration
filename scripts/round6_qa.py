#!/usr/bin/env python3
"""Round 5 after-fix QA: full-page screenshots + headings/small/overflow + header/footer checks.
Usage: round6_qa.py <measurements-out.json>
Serves out/ on QA_PORT or 8937. Fresh browser per page.
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "screenshots/round6/measurements.json"
SHOT = BASE / "screenshots/round6"
SHOT.mkdir(parents=True, exist_ok=True)
PORT = os.environ.get("QA_PORT", "8937")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", str(BASE / "out")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
HEAD_JS = r"""() => {
  function linesOf(el){
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while(walker.nextNode()){ const n = walker.currentNode; if(n.textContent.trim()) nodes.push(n); }
    const tops = []; let wi = 0;
    for(const n of nodes){
      const words = n.textContent.split(/\s+/).filter(Boolean); let off = 0;
      for(const w of words){
        const start = n.textContent.indexOf(w, off); off = start + w.length;
        try{ const r = document.createRange(); r.setStart(n, start); r.setEnd(n, start + w.length);
          const rects = r.getClientRects(); if(rects.length) tops.push(Math.round(rects[0].top)); }catch(e){}
        wi++;
      }
    }
    if(!tops.length) return {lines:0, lastWords:0, words:wi};
    const uniq = [...new Set(tops)]; const lastTop = uniq[uniq.length-1];
    return {lines: uniq.length, lastWords: tops.filter(t=>t===lastTop).length, words: wi};
  }
  const headings = [...document.querySelectorAll('h1,h2,h3')].map(el=>{
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); const L = linesOf(el);
    return {tag: el.tagName, text: el.textContent.trim().slice(0,110), size: cs.fontSize, width: Math.round(r.width), lines: L.lines, lastWords: L.lastWords};
  });
  const small = [];
  const seen = new Set();
  document.querySelectorAll('body *').forEach(el=>{
    if(el.children.length) return; const t = el.textContent.trim(); if(!t || t.length < 2) return;
    const r = el.getBoundingClientRect(); if(r.width===0 || r.height===0) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    const key = el.tagName + '|' + getComputedStyle(el).fontSize + '|' + String(el.className||'');
    if(fs < 17 && !seen.has(key)){ seen.add(key); small.push({tag: el.tagName, size: getComputedStyle(el).fontSize, cls: String(el.className||''), sample: t.slice(0,60)}); }
  });
  return {headings, small, over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          bodySize: getComputedStyle(document.body).fontSize, h1n: document.querySelectorAll('h1').length,
          imgs: [...document.querySelectorAll('img')].map(i => [i.getAttribute('src'), i.complete && i.naturalWidth > 0]),
          maps: document.querySelectorAll('iframe').length, title: document.title};
}"""
HF_JS = r"""() => {
  const out = {};
  const hdr = document.querySelector('.site-header');
  const top = document.querySelector('.topbar');
  if(hdr){ const r = hdr.getBoundingClientRect(); out.headerTop = Math.round(r.top); out.headerH = Math.round(r.height); }
  if(top){ const r = top.getBoundingClientRect(); out.topbarBottom = Math.round(r.bottom); }
  const hi = document.querySelector('.header-inner');
  if(hi){ out.headerInnerScroll = hi.scrollWidth; out.headerInnerClient = hi.clientWidth; }
  const taps = {};
  for(const [name, sel] of [['headerCall','.header-call'],['menuBtn','.menu-btn'],['heroCall','.hero .btn-call'],['callbar','.callbar'],['submit','.form-card button']]){
    const el = document.querySelector(sel);
    if(el){ const r = el.getBoundingClientRect(); taps[name] = Math.round(r.height); }
  }
  out.taps = taps;
  out.navT = [...document.querySelectorAll('.nav-toggle')].map(e => Math.round(e.getBoundingClientRect().height));
  const foot = document.querySelector('.footer-inner');
  if(foot){
    const kids = [...foot.children].map(c => Math.round(c.getBoundingClientRect().top));
    out.footerCols = [...new Set(kids)].length;
    out.footerBottomSize = getComputedStyle(document.querySelector('.footer-bottom')).fontSize;
  }
  return out;
}"""
results = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home, "homepage guard failed"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for p in PAGES:
            slug = p["slug"]; name = slug.strip("/") or "home"
            row = {"slug": slug, "tab": p["tab"]}
            browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
            try:
                for vw, tag, suf in [(1366, "d", "d"), (390, "m", "m")]:
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}{slug}", wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(400)
                    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(700)
                    pg.evaluate("() => window.scrollTo(0, 0)")
                    pg.wait_for_timeout(300)
                    row[tag] = pg.evaluate(HEAD_JS)
                    # header/footer live checks
                    if vw == 1366:
                        # hover Services dropdown
                        try:
                            pg.hover(".nav-toggle >> nth=0", timeout=5000); pg.wait_for_timeout(400)
                            row["ddHover"] = pg.evaluate("() => !!document.querySelector('.dropdown')")
                            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                            row["ddEscape"] = pg.evaluate("() => !document.querySelector('.dropdown')")
                        except Exception as e:
                            row["ddHover"] = f"ERR {e}"; row["ddEscape"] = None
                        pg.evaluate("() => window.scrollTo(0, 1500)"); pg.wait_for_timeout(300)
                        row["hfD"] = pg.evaluate(HF_JS)
                        pg.evaluate("() => window.scrollTo(0, 0)")
                    else:
                        try:
                            pg.click(".menu-btn", timeout=5000); pg.wait_for_timeout(400)
                            row["menuOpen"] = pg.evaluate("() => document.querySelector('.mobile-nav').classList.contains('open')")
                        except Exception as e:
                            row["menuOpen"] = f"ERR {e}"
                        row["hfM"] = pg.evaluate(HF_JS)
                    pg.screenshot(path=str(SHOT / f"{name}-{suf}.png"), full_page=True)
                    ctx.close()
                for vw in (320, 768, 1024):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}{slug}", wait_until="domcontentloaded", timeout=60000)
                    pg.wait_for_timeout(300)
                    row.setdefault("align", {})[vw] = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    ctx.close()
            finally:
                browser.close()
            results.append(row)
            print("done", slug, flush=True)
finally:
    srv.terminate()
OUT.write_text(json.dumps(results, indent=2))
print("wrote", OUT, len(results))
