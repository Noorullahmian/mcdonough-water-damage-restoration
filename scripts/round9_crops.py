#!/usr/bin/env python3
"""Round 9 deliverable crops — fresh, final build only, never reused.
Serves /tmp/r9test on QA_PORT or 8971. Saves into ~/workspace/your_files/mcdonough-round9/.
Crops: topbar (top strip), footer (footer element), h3 section (homepage section holding
the first h3), emergency intro (first section after hero, button below paragraphs),
privacy + terms full pages. Desktop 1366 + mobile 390.
"""
import os, subprocess, sys, time, urllib.request
from pathlib import Path
BASE = Path.home() / "workspace/mcdonough-water-damage"
OUT = Path.home() / "workspace/your_files/mcdonough-round9"
OUT.mkdir(parents=True, exist_ok=True)
PORT = os.environ.get("QA_PORT", "8971")
srv = subprocess.Popen(["python3", "-m", "http.server", PORT, "--directory", "/tmp/r9test"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
B = f"http://127.0.0.1:{PORT}/mcdonough-water-damage-restoration"
try:
    home = urllib.request.urlopen(B + "/", timeout=10).read().decode("utf-8", "ignore")
    assert "McDonough Water Damage Restoration" in home, "guard failed"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"])
        try:
            jobs = []
            for vw, tag in [(1366, "d"), (390, "m")]:
                ctx = browser.new_context(viewport={"width": vw, "height": 900})
                pg = ctx.new_page()
                # topbar strip
                pg.goto(B + "/", wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"topbar-{tag}.png"), clip={"x": 0, "y": 0, "width": vw, "height": 200})
                # footer element
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(500)
                pg.locator(".site-footer").screenshot(path=str(OUT / f"footer-{tag}.png"))
                # h3 section: homepage section containing the first h3
                pg.goto(B + "/", wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(400)
                pg.locator("main h3").first.scroll_into_view_if_needed()
                pg.wait_for_timeout(300)
                sec = pg.evaluate("""() => { const h = document.querySelector('main h3'); let el = h; while (el && el.tagName !== 'SECTION') el = el.parentElement; const r = el.getBoundingClientRect(); return {y: window.scrollY + r.top, h: r.height}; }""")
                pg.evaluate(f"() => window.scrollTo(0, {sec['y'] - 20})")
                pg.wait_for_timeout(300)
                pg.screenshot(path=str(OUT / f"h3-section-{tag}.png"), clip={"x": 0, "y": 0, "width": vw, "height": min(900, int(sec['h']) + 40)})
                # emergency intro section (first section after hero)
                pg.goto(B + "/emergency-water-extraction/", wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"emergency-intro-{tag}.png"), clip={"x": 0, "y": 0, "width": vw, "height": 900})
                # privacy + terms full pages
                for slug, name in [("/privacy-policy/", "privacy"), ("/terms-of-use/", "terms")]:
                    pg.goto(B + slug, wait_until="networkidle", timeout=60000)
                    pg.wait_for_timeout(400)
                    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(500)
                    pg.evaluate("() => window.scrollTo(0, 0)")
                    pg.wait_for_timeout(300)
                    pg.screenshot(path=str(OUT / f"{name}-{tag}.png"), full_page=True)
                ctx.close()
                print("done viewport", vw, flush=True)
        finally:
            browser.close()
finally:
    srv.terminate()
print("wrote", sorted(p.name for p in OUT.glob("*.png")))
