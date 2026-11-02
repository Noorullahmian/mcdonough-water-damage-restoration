#!/usr/bin/env python3
"""Round 9 CTA-position check: for each of 5+ pages, the first .btn-call inside
<main> AFTER the hero must sit below the intro paragraphs and before the first h2/h3.
Measures: button top, first-h2/h3 top, intro-section top, second-section top, and which
section index the button sits in. Also topbar text + topbar SVG icon presence + h3 colour.
Usage: round9_cta.py <out.json>  (serves /tmp/r9test on QA_PORT or 8969)
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path.home() / "workspace/mcdonough-water-damage"
PAGES = json.load(open(BASE / "data/pages.json"))
PICKS = ["/emergency-water-extraction/", "/water-damage-restoration-stockbridge-ga/",
         "/burst-pipe-water-damage/", "/water-damage-restoration-jackson-ga/",
         "/mold-remediation/", "/about-us/", "/"]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "screenshots/round9/cta-check.json"
PORT = os.environ.get("QA_PORT", "8969")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", "/tmp/r9test"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
JS = r"""() => {
  const secs = [...document.querySelectorAll('main > section:not(.hero)')];
  const btn = document.querySelector('main > section:not(.hero) a.btn-call');
  const r = btn ? btn.getBoundingClientRect() : null;
  let secIdx = -1;
  if (btn) { let el = btn; while (el && el.tagName !== 'SECTION') el = el.parentElement; secIdx = secs.indexOf(el); }
  const firstH = document.querySelector('main > section:not(.hero) h2, main > section:not(.hero) h3');
  const hr = firstH ? firstH.getBoundingClientRect() : null;
  const h3 = document.querySelector('main h3');
  const top = document.querySelector('.topbar');
  return {
    btnTop: r ? Math.round(r.top + window.scrollY) : -1,
    btnSection: secIdx,
    firstH2H3Top: hr ? Math.round(hr.top + window.scrollY) : -1,
    firstH2H3Tag: firstH ? firstH.tagName : '',
    introSectionTop: secs.length ? Math.round(secs[0].getBoundingClientRect().top + window.scrollY) : -1,
    secondSectionTop: secs.length > 1 ? Math.round(secs[1].getBoundingClientRect().top + window.scrollY) : -1,
    h3Color: h3 ? getComputedStyle(h3).color : '',
    topbarText: top ? top.textContent.replace(/\s+/g, ' ').trim() : '',
    topbarHasSvg: !!document.querySelector('.topbar svg'),
    topbarHasEmojiPhone: top ? /📞/.test(top.textContent) : false,
    footerHasGradient: (() => { const f = document.querySelector('.site-footer'); return f ? getComputedStyle(f).backgroundImage : ''; })(),
  };
}"""
rows = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home, "guard failed"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
        try:
            for slug in PICKS:
                for vw in (1366, 390):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration{slug}", wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(400)
                    d = pg.evaluate(JS)
                    d["slug"] = slug; d["vw"] = vw
                    d["cta_below_intro_above_h2"] = (d["btnTop"] >= 0 and d["btnTop"] > d["introSectionTop"] and
                                                     (d["firstH2H3Top"] < 0 or d["btnTop"] < d["firstH2H3Top"]))
                    rows.append(d)
                    print(slug, vw, d, flush=True)
                    ctx.close()
        finally:
            browser.close()
finally:
    srv.terminate()
OUT.write_text(json.dumps(rows, indent=2))
print("wrote", OUT, len(rows))
