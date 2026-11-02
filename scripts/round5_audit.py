#!/usr/bin/env python3
"""Round 5 audit: headings line counts + last-line words, small text inventory, overflow.
Usage: round5_audit.py <outfile.json>  (serves out/ on QA_PORT or 8925)
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "screenshots/round5/audit.json"
PORT = os.environ.get("QA_PORT", "8925")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", str(BASE / "out")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
JS = r"""() => {
  function linesOf(el){
    // group word rects by top
    const text = el.textContent.trim();
    if(!text) return {lines:0, lastWords:0, words:0};
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while(walker.nextNode()){ const n = walker.currentNode; if(n.textContent.trim()) nodes.push(n); }
    const tops = [];
    let wi = 0;
    for(const n of nodes){
      const words = n.textContent.split(/\s+/).filter(Boolean);
      let off = 0;
      for(const w of words){
        const start = n.textContent.indexOf(w, off); off = start + w.length;
        try{
          const r = document.createRange(); r.setStart(n, start); r.setEnd(n, start + w.length);
          const rects = r.getClientRects();
          if(rects.length) tops.push(Math.round(rects[0].top));
        }catch(e){}
        wi++;
      }
    }
    if(!tops.length) return {lines:0, lastWords:0, words:wi};
    const uniq = [...new Set(tops)];
    const lastTop = uniq[uniq.length-1];
    const lastWords = tops.filter(t=>t===lastTop).length;
    return {lines: uniq.length, lastWords, words: wi};
  }
  function smallText(){
    const out = {};
    const seen = new Set();
    document.querySelectorAll('body *').forEach(el=>{
      if(el.children.length) return;
      const t = el.textContent.trim();
      if(!t || t.length < 2) return;
      const r = el.getBoundingClientRect();
      if(r.width===0 || r.height===0) return;
      const cs = getComputedStyle(el);
      const fs = parseFloat(cs.fontSize);
      const key = el.tagName + '|' + cs.fontSize + '|' + (el.className||'');
      if(fs < 17 && !seen.has(key)){ seen.add(key); out[key] = {tag: el.tagName, size: cs.fontSize, cls: String(el.className||''), sample: t.slice(0,60)}; }
    });
    return Object.values(out);
  }
  const headings = [...document.querySelectorAll('h1,h2,h3')].map(el=>{
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const L = linesOf(el);
    return {tag: el.tagName, text: el.textContent.trim().slice(0,110), size: cs.fontSize, width: Math.round(r.width), height: Math.round(r.height), lines: L.lines, lastWords: L.lastWords, words: L.words, wrap: cs.textWrap || cs.getPropertyValue('text-wrap')};
  });
  const over = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return {headings, small: smallText(), over, bodySize: getComputedStyle(document.body).fontSize};
}"""
results = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home, "homepage guard failed"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for p in PAGES:
            row = {"slug": p["slug"], "tab": p["tab"]}
            browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
            try:
                for vw, tag in [(1366, "d"), (390, "m")]:
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}{p['slug']}", wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(400)
                    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(600)
                    pg.evaluate("() => window.scrollTo(0, 0)")
                    row[tag] = pg.evaluate(JS)
                    ctx.close()
                for vw in (320, 768, 1024):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}{p['slug']}", wait_until="domcontentloaded", timeout=60000)
                    pg.wait_for_timeout(300)
                    row.setdefault("align", {})[vw] = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    ctx.close()
            finally:
                browser.close()
            results.append(row)
            print("done", p["slug"], flush=True)
finally:
    srv.terminate()
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2))
print("wrote", OUT, len(results))
