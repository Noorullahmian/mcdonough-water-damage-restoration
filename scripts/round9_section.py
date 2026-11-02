#!/usr/bin/env python3
"""Round 4 per-section 10x pass for a slice of pages (no screenshots).
Usage: round4_section.py <start> <end> <outfile.json>
Same section logic as section.py, fresh browser per page."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
PAGES = PAGES + [{"slug": "/privacy-policy/", "tab": 0}, {"slug": "/terms-of-use/", "tab": 0}]

START, END, OUT = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
PORT = os.environ.get("QA_PORT", "8967")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", "/tmp/r9test"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
report = []
try:
    home = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for p in PAGES[START:END]:
            url = f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration{p['slug']}"
            row = {"slug": p["slug"], "sections": []}
            browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
            try:
                for vw in (1366, 390):
                    ctx = browser.new_context(viewport={"width": vw, "height": 900})
                    pg = ctx.new_page()
                    pg.goto(url, wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(300)
                    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(800)
                    pg.evaluate("() => window.scrollTo(0, 0)")
                    pg.wait_for_timeout(300)
                    secs = pg.evaluate("""() => {
                      const out = [];
                      const push = (el, name) => {
                        const r = el.getBoundingClientRect();
                        const imgs = [...el.querySelectorAll('img')].map(i => {
                          const rr = i.getBoundingClientRect();
                          return {src: i.getAttribute('src'), rw: Math.round(rr.width), rh: Math.round(rr.height), nw: i.naturalWidth, nh: i.naturalHeight, ok: i.complete && i.naturalWidth > 0};
                        });
                        const h = el.querySelector('h1,h2,h3');
                        const hc = h ? getComputedStyle(h).color : '';
                        const btns = [...el.querySelectorAll('a.btn-call')].map(a => a.textContent.trim());
                        out.push({name, heading: h ? h.textContent.trim().slice(0,70) : '', hcolor: hc, imgs, btns, h: Math.round(r.height)});
                      };
                      const hm = document.querySelector('.hero'); if (hm) push(hm, 'hero');
                      document.querySelectorAll('main > section:not(.hero)').forEach((s, i) => push(s, 'section-' + (i+1)));
                      push(document.querySelector('footer'), 'footer');
                      const heroCall = document.querySelector('.hero .btn-call');
                      const hr = heroCall ? heroCall.getBoundingClientRect() : null;
                      const bar = document.querySelector('.callbar');
                      const br = bar ? bar.getBoundingClientRect() : null;
                      return {sections: out, heroCallY: hr ? Math.round(hr.top) : -1, heroCallVisible: hr ? (hr.top < 900 && hr.bottom > 0) : false,
                              callbarVisible: br ? (br.top < 900) : false, over: document.documentElement.scrollWidth - document.documentElement.clientWidth};
                    }""")
                    row[f"vw{vw}"] = secs
                    ctx.close()
                slugpath = p["slug"].strip("/")
                htmlf = BASE / "out" / slugpath / "index.html" if slugpath else BASE / "out" / "index.html"
                row["html_bytes"] = htmlf.stat().st_size if htmlf.exists() else 0
            finally:
                browser.close()
            report.append(row)
            nsec = sum(len(row[f"vw{vw}"]["sections"]) for vw in (1366, 390))
            print(f"{p['slug']} sections={nsec} over1366={row['vw1366']['over']} over390={row['vw390']['over']} "
                  f"heroY1366={row['vw1366']['heroCallY']} heroY390={row['vw390']['heroCallY']} callbar390={row['vw390']['callbarVisible']}", flush=True)
    json.dump(report, open(OUT, "w"), indent=1)
    print("SECTION DONE", len(report))
finally:
    srv.terminate()
