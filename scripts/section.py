#!/usr/bin/env python3
"""Added phase round check: per page, per section.
Sections = hero + each <section> + footer. For each: heading, images (rendered vs natural),
buttons, colours, phone-above-fold, overflow. Plus page weight from out/."""
import json, os, subprocess, time
from pathlib import Path
BASE = Path(os.path.expanduser("~/workspace/mcdonough-water-damage"))
PAGES = json.load(open(BASE / "data/pages.json"))
LABEL = os.environ.get("SEC_LABEL", "added1")
OUT = BASE / "screenshots" / LABEL
OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen(["python3", "-m", "http.server", "8917", "--directory", str(BASE / "out")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    import urllib.request as _u
    assert "McDonough Water Damage Restoration" in _u.urlopen("http://127.0.0.1:8917/", timeout=10).read().decode("utf-8", "ignore")
    from playwright.sync_api import sync_playwright
    report = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in PAGES:
            url = f"http://127.0.0.1:8917{p['slug']}"
            row = {"slug": p["slug"], "sections": []}
            for vw in (1366, 390):
                ctx = b.new_context(viewport={"width": vw, "height": 900})
                pg = ctx.new_page()
                pg.goto(url, wait_until="networkidle", timeout=60000)
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
                  push(document.querySelector('.hero'), 'hero');
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
            # page weight from out/
            slugpath = p["slug"].strip("/")
            htmlf = BASE / "out" / slugpath / "index.html" if slugpath else BASE / "out" / "index.html"
            row["html_bytes"] = htmlf.stat().st_size if htmlf.exists() else 0
            report.append(row)
            # print compact flags
            for vw in (1366, 390):
                s = row[f"vw{vw}"]
                badimgs = [(sec["name"], i) for sec in s["sections"] for i in sec["imgs"] if not i["ok"] or (i["rw"] > 0 and abs(i["nw"] - i["rw"]) > 400)]
                print(f"{p['slug']:50s} vw{vw} over={s['over']} heroCallY={s['heroCallY']} visible={s['heroCallVisible']} bar={s['callbarVisible']} badimgs={badimgs} sections={len(s['sections'])}")
        b.close()
    json.dump(report, open(OUT / "sections.json", "w"), indent=1)
    print("sections report saved")
finally:
    srv.terminate()
