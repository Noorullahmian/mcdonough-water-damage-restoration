# McDonough Water Damage Restoration — 10x Audit Checklist (reusable)

**Purpose:** the exact list used for every "10x" audit round on this site. It is built from
OUR OWN mistakes on this site, not a generic checklist. Every item states the past failure,
the rule that now prevents it, how it is measured, what counts as pass/fail, and the proof
required before anyone may claim the item passed. A round that skips an item, or claims an
item without its proof, is not a 10x audit.

**Scope of one audit run:** all 27 pages, per section, desktop 1366 + mobile 390, plus
overflow at 320 and 1024. Viewports, ports and scripts are named below so a later round
cannot silently change them.

**Standing rules (never overridden by an audit):** no Doc word changes; no title/meta changes
unless a defect proves one (logged separately); banned phrases "free estimate", "certified",
"licensed" = ZERO everywhere; no deploy, no push, no domain/DNS touch; no new claims;
no fake photos; city photos are representative Georgia imagery unless a verified town photo
is found without real-estate/AI sources (see check 3).

## How to audit, in order

1. **Build first, then serve the fresh build.** `npm run build` must pass. Serve `out/` only,
   on a fresh unique port (see check 5). Never audit `public/`, never audit a stale `out/`.
2. **Run the measurement scripts** (all three, fresh, on the final build):
   - Full-page QA: `scripts/round7_qa.py` (copied per round, e.g. `round8_qa.py`) → 54
     full-page screenshots + `measurements.json` (headings, sizes, overflow, images, taps,
     dropdowns, menu, maps, H1 count).
   - Header run: `scripts/round7_header.py` (copied per round) → 108 header-area shots +
     `header-check.json` (call bar, sticky header, scroll-away, header-inner overflow,
     footer stacking, taps, dropdowns, menu).
   - Per-section run: `scripts/round4_section.py 0 27` → `sections.json` (936 section
     measurements: per-section heading colour, rendered image sizes, hero-call position,
     overflow, sticky call bar visibility).
3. **Run the static HTML checks** (`scripts/round8_checks.py` or later copy): per page —
   HTTP 200 + homepage-title guard, every `<img>` src resolves to a file in `out/`,
   no width/height attributes on `<img>` (check 2), banned phrases ZERO, no bracket
   markers visible, titles ≤60 chars and metas ≤160 chars (decoded), no body self-links.
4. **View pixels, don't just read JSON.** View the header crops, the hero crop, and the
   four image contact sheets (heroes, seconds, cards, areas) with your own eyes. A
   measurement that was never looked at is not a visual pass.
5. **Fix genuine defects only** (CSS/images, scoped edits — check 13), then **re-verify
   fresh on the rebuilt final build** (all three scripts again). A fix verified only on
   the pre-fix build is not verified.
6. **Write the audit report** (FINDINGS.md round section + brief DONE note) with: defect
   list per page/section, fixes with before/after values, the honest exceptions that were
   NOT fixed and why, and the proof file paths. Never reuse an old report's numbers.

## The 14 baked-in checks

### 1. A 200 is not proof — check assets + a real render
- **Past failure:** pages returning success were treated as working while styling or images
  were broken; a page served below root depth must use root-absolute asset links, and a
  status code says nothing about either.
- **Rule:** for every page, assert HTTP 200 AND the homepage-title guard AND a real H1 in
  the served HTML AND every referenced `<img>`/CSS file resolving, AND a real-browser
  render (full-page screenshot) with no broken-image flags.
- **Measure:** `round8_checks.py` (status, title, H1, img-src resolution) + QA script
  (imgs ok, full-page shots).
- **Pass:** 27/27 pages, 0 broken images, 0 missing assets. **Fail:** any 200 page with a
  missing asset, a missing H1, or a broken image in the render.
- **Proof:** checks output + 54 full-page screenshots on the final build.

### 2. Image width alone is false — always measure HEIGHT + aspect ratio (height:auto trap)
- **Past failure (Fort Myers, 2026-11-02, user caught it):** width/height attributes on an
  `<img>` count as a SPECIFIED height in Chromium and defeat `aspect-ratio` unless the rule
  also carries `height:auto`; width-only checks (359/361 flush) passed while images rendered
  as tall crops and short boxes.
- **Rule:** every image is judged by rendered width AND rendered height AND natural size.
  CORRECTION (Round 8, found by the checks script — the first draft of this list wrongly
  claimed no `<img>` attributes exist): this site's `<img>` tags DO carry width/height
  attributes by design in `components/PageRenderer.tsx` (hero 760×570, second 1100×420,
  cards 800×500, all matching their boxes). That is safe ONLY because the base rule
  `img{max-width:100%;height:auto}` is present in `app/globals.css` AND the container
  rules set explicit heights with `object-fit:cover` — the two conditions that neutralize
  the Fort Myers trap. The grep therefore checks the safeguard, not attribute absence:
  attributes are permitted only while `height:auto` survives in the base img rule.
- **Measure:** section run records rw/rh/nw/nh per image; HTML grep for width/height
  attributes (expected: all 78 attributed, matching box ratios) + grep confirming
  `height:auto` in the base img rule.
- **Pass:** `height:auto` present in the base img rule; 0 zero-height renders; rendered
  heights match their boxes (hero 4:3 desktop / 16:10 mobile, cards 16:10, figures 440px
  desktop). **Fail:** `height:auto` removed, or any rendered height not matching its box.
- **Proof:** sections data + both grep outputs.

### 3. Filename/alt is not relevance — viewed pixels + hash + corner watermark scan + logo check
- **Past failures:** (a) Jackson hero carried a baked-in "GEORGIA MLS REAL ESTATE SERVICES"
  watermark, found only by a corner scan in Round 6; (b) the AC card showed a visible
  Samsung logo, fixed in Round 5; (c) a rejected cartoon toilet once survived in a stale
  screenshot sheet (see check 4); (d) AI-named, competitor-host and real-estate-marketing
  photos were repeatedly offered and rejected in Rounds 5–6.
- **Rule:** relevance is judged by VIEWED PIXELS at first glance (the image must clearly
  show that exact service/city), never by filename or alt alone. Every image must also be
  hash-unique in-site with 0 collisions vs other-site images; every image gets a corner
  scan for baked-in watermarks/branding; any visible third-party logo = defect. Sources
  rejected outright: AI-generated or AI-named files, competitor-hosted images,
  real-estate marketing photos. No image is ever claimed to be a real job photo.
- **Measure:** four contact sheets (heroes, seconds, cards, areas) viewed by eye;
  `scripts/hashcheck.py` (in-site uniqueness + cross-site collisions); corner scan of all
  78 files.
- **Pass:** 78/78 clearly relevant at first glance, 0 watermarks, 0 visible logos,
  0 collisions. **Fail:** any ambiguous, generic-when-specific-exists, watermarked, or
  logo-bearing image — it is replaced, not argued with.
- **Proof:** contact sheets + hashcheck output + replacement list (or an explicit "0
  replacements" statement with the sheets as evidence).
- **Honest limit (standing):** city heroes/seconds + area cards are representative Georgia
  town/suburban imagery, NOT verified photos of each exact town. This is reported, never
  papered over; provably town-specific photos need the user's own town photos or a
  licensed per-town search.

### 4. Never reuse old screenshots or reports — re-capture on the FINAL build
- **Past failure:** a Round 2 card sheet was stale and still showed a rejected cartoon
  toilet as live, while the live file was already the correct photographic image; the
  parent had to rebuild the sheet from final files before delivery.
- **Rule:** every screenshot, measurement and number in an audit report comes from the
  FINAL build of that round. Pre-fix shots are kept in a separate folder and labelled
  pre-fix; they are never presented as post-fix proof. If a fix lands after the screenshots,
  the screenshots are re-taken.
- **Measure:** file mtimes + build order (build → screenshots → report, in that order).
- **Pass:** all proof files dated after the final build. **Fail:** any proof older than
  the last code/image change it claims to prove.
- **Proof:** screenshot folders + measurements files on the final build, with any
  pre-fix/final distinction labelled in the report.

### 5. Unique port + homepage-title guard (never measure the wrong site)
- **Past failure:** a QA run measured a Texas site because port 8901 was already serving
  another site; the run was discarded and the script moved to a fresh port plus a
  homepage-title guard.
- **Rule:** every audit server runs on a port used by nothing else in that round, and the
  first fetch asserts the homepage contains "McDonough Water Damage Restoration" (and a
  real H1) before any page is measured.
- **Measure:** port recorded in the report; guard assertion in the script output.
- **Pass:** guard passes on the first fetch; all 27 measured pages belong to this site
  (slugs from `data/pages.json`).
- **Proof:** script output showing the guard + the port used.

### 6. Own script crashes plainly — rerun detached, nothing reused from partial runs
- **Past failures:** a Round 4 batch was SIGTERM-killed, a Round 6A QA attempt died after
  6 pages when its exec session was lost, and a Round 7 section run vanished with its
  session. In each case the partial run was discarded, not patched up.
- **Rule:** if a run dies, say so in the report (what died, after how many pages), rerun
  it detached with unbuffered logging, and reuse NOTHING from the partial run — no
  measurements, no screenshots carried over.
- **Measure:** run logs; output file completeness (27 pages, 54 shots, 108 header shots,
  936 sections) checked before the report is written.
- **Pass:** complete outputs on the final build, or a plainly logged rerun that produced
  them. **Fail:** a report citing a partial run's numbers as final.
- **Proof:** complete output files + the crash note (or "no crashes this round").

### 7. Wrap experiments are measured before/after with the SAME script — or not done
- **Past failure:** `text-wrap:pretty` made things WORSE (desktop orphans 1 → 66, homepage
  H2 last line 4 words → lone "GA"); natural wrap on H1 only also lost (H1 orphans 1 → 7).
  Both were caught only by comparing after-measurements to the before-audit with the same
  script, and both were reverted. Balance on h1/h2/h3 is the measured-best setting.
- **Rule:** any wrap/width/font change that could affect line breaks is measured before
  AND after with the same script (orphan counts + H1 line counts, desktop + mobile).
  A change that increases orphans or line counts is reverted, not shipped. No wrap change
  is ever justified by theory alone.
- **Measure:** QA script heading lines/lastWords, desktop + mobile, before vs after.
- **Pass:** orphans ≤ before (current inherent baseline: desktop 1 About H1, mobile 26
  long verbatim titles) and no new 4+ line H1s. **Fail:** any increase — revert.
- **Proof:** before/after orphan + H1-line tables.

### 8. Lazy-load flags are scroll-verified before calling an image broken
- **Past failure (Round 2):** homepage lazy-load image flags looked like broken images
  until scroll-verified loads disproved them — a measurement artifact, not a defect.
- **Rule:** an image is only "broken" if it is still incomplete after scrolling the page
  fully (top → bottom → top) and waiting. The section script already scrolls; the QA
  script's img flags are cross-checked against the section run before any image is
  declared broken.
- **Measure:** section run (scrolls) imgs ok + QA imgs ok, compared.
- **Pass:** 0 images incomplete after scroll. **Fail:** an image incomplete after scroll
  on the final build.
- **Proof:** both runs' img results agreeing.

### 9. A mobile menu open in a QA shot is a capture artifact — label it
- **Past failure (recurring):** mobile full-page shots show the menu EXPANDED because the
  QA script opens it to verify it; without a label, that looks like the menu is broken
  open by default.
- **Rule:** every delivery that includes QA mobile shots states this in the report (and
  the parent states it to the user): the open menu is the verification capture, not the
  default state. The default state is verified separately (menu closed on load).
- **Measure:** menu-open check in the QA script + a closed-by-default observation.
- **Pass:** menu opens on tap, closes on selection/Escape, closed on load.
- **Proof:** QA menu checks + the label in the report.

### 10. Map tiles blank in the VM is a tunnel block, not a site defect
- **Past failure (recurring):** Google Maps tiles do not render in this VM's headless
  browser (connection failure to google.com); treating that as a site defect would send
  fixes at a working embed.
- **Rule:** the map check is: exactly 1 iframe per page with the correct place query, plus
  a visible "Open <place> in Google Maps ↗" fallback link. Tile rendering itself is
  verified only in the user's real browser (still an open item, never claimed done here).
- **Measure:** QA maps count per page + fallback link presence.
- **Pass:** 27/27 pages, maps = 1, fallback link present. **Fail:** missing/wrong iframe
  or missing fallback link.
- **Proof:** maps counts + the standing open item carried forward.

### 11. Sticky call bar overlay is standard — measure the hero call above the fold
- **Past failure (Round 4):** the mobile hero call on About measured inside the fold but
  partly covered by the fixed 57px sticky call bar; that is not a defect on its own —
  a call button is always visible via the bar.
- **Rule:** the hero-call check is the call button's TOP position vs the 900px fold
  (desktop + mobile, all pages), reported as a number per page, with the worst page named.
  Overlay by the sticky bar is reported as the standing limit, not hidden and not fixed
  by shrinking content.
- **Measure:** section run heroCallY + heroCallVisible + callbarVisible.
- **Pass:** hero call visible above the fold on 27/27 pages at 1366 + 390.
- **Proof:** hero-call table with the worst page named (current: About mobile, tight —
  see Round 7).

### 12. Verbatim words, banned phrases ZERO, no body self-links, bracket markers never visible, titles/metas in limit
- **Past failures (standing, from the original build rules):** bracket markers in the Doc
  are instructions only and must never appear on the site; a page must never link to
  itself from its own body (header/footer exempt); titles/metas over limit were trimmed
  in Round 2 and must stay trimmed.
- **Rule:** every audit greps the built HTML and `data/pages.json` for: banned phrases
  ("free estimate", "certified", "licensed" and variants) = 0; bracket markers ("Button:",
  "Tagline:", "Trust points") = 0 visible; body self-links = 0 (a link in `<main>` whose
  href equals the page's own slug); titles ≤60 chars and metas ≤160 chars, decoded.
  Content words are never "fixed" by an audit — a verbatim problem is reported to the
  user, not silently edited.
- **Measure:** `round8_checks.py` over `out/` + `data/`.
- **Pass:** banned 0, markers 0, body self-links 0, titles 0 over 60, metas 0 over 160.
- **Proof:** checks output with the counts.

### 13. No global first-match replaces — scope insertions to the target section
- **Past failure (Tulsa linking round, 2026-10-27):** a generic close pattern matched an
  earlier section and 12 related cards landed in the wrong section; caught by the link
  verifier and repaired the same round.
- **Rule:** any fix that inserts content targets its section substring (find section
  start, then search inside it) and re-verifies placement in the rendered page before
  delivery. Global first-match marker replaces are forbidden on this site.
- **Measure:** edit diff reviewed + rendered placement check for any insertion fix.
- **Pass:** every insertion lands in its target section, verified in the render.
- **Proof:** the fix list naming the scoped edit, or "no insertions this round".

### 14. Tap targets, header wrap at 1024, call-bar scroll-away + sticky header, overflow at all widths — all measured, none eyeballed
- **Past failures:** Menu 36px, nav toggles 40px and topbar phone 24px tap targets were
  all under 44px until Round 3 fixed them; header wrap at 1024px is a recurring risk
  (brand + nav + call already fill ~980 of 984px there).
- **Rule:** header run measures, per page × 1366/1024/390/320: tap targets ≥44px for
  header call, hero call, sticky call bar, menu button, nav toggles; header-inner
  scrollWidth ≤ clientWidth (no wrap/overflow at 1024); after scrolling, header top = 0
  and call-bar bottom < 0 (sticky header, scrolling call bar, no double header); footer
  1 row desktop / stacked mobile. QA measures overflow 0 at 320/390/768/1024/1366.
- **Measure:** header-check.json + QA overflow fields.
- **Pass:** all taps ≥44px (display:none elements excluded — a "0" for a hidden element
  is not a defect), no header-inner overflow, scroll-away on 27/27, overflow 0 everywhere.
- **Proof:** header-check.json + measurements.json.

## Pass/fail for the whole round

A 10x audit passes only if: all 14 checks pass (or fail only on the standing honest
exceptions, named explicitly); every genuine defect found was fixed and re-verified fresh;
and the report names its proofs. Known standing exceptions that are NOT audit failures
unless this round proves otherwise: desktop About H1 + 26 mobile orphans (inherent
verbatim titles); representative (not exact-town) city photos; stock-only licensing
question; 44px footer/prose links; call-bar reading correction; domain; form delivery;
map tiles in a real browser. A round that claims any of these fixed without proof has
failed its own audit.
