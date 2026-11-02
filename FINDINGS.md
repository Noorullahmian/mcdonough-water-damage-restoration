# McDonough Water Damage Restoration — Findings Log (local only)

## Build
- Next.js 14.2.5 static export (`output: "export"`, `trailingSlash: true`), `npm run build` succeeds, 27 routes + 404 prerendered.
- Source: `~/workspace/mcdonough-water-damage/` — Next.js source + `out/` export (9.2 MB).
- Pages: 27. Homepage (Tab 1) + 15 services (Tabs 2–16) + 9 cities (Tabs 17–25) + About (26) + Contact (27). Tab 28 is header/footer/nav only, not a page.
- Business: McDonough Water Damage Restoration, McDonough, GA 30252 & 30253, Henry County, phone (470) 745-9798, Open 24 hours. No street address in the Doc — none invented.

## Theme + colours (new, nothing visible copied from Tulsa EMD)
- Tulsa EMD used for STRUCTURE ONLY (component/layout system). No Tulsa text, phone, logo, image, or colour was copied.
- New palette: H1 deep navy #0B2F4A (Georgia serif), H2 vivid aqua #0E8AC0 with aqua/gold underline, H3 slate #243B53, call CTA crimson #D9232E, sections white / mist #F3F8FB.
- Measured: H1 rgb(11, 47, 74) at 57.6 px desktop, H2 rgb(14, 138, 192) at 40 px desktop, body 19 px desktop / 18 px mobile, line-height 1.7.

## Verbatim content
- Parser uses the Doc JSON paragraph styles (HEADING_1/2/3, bullets, tables) — not guesswork from plain text.
- Word-level check vs the Doc (excluding table pipe separators and the service-card colon, which the renderer keeps as "Name:" + description): 26/27 tabs exact, Tab 1 exact on words (colon artifact only). No invented certification, license, review, rate, or place.
- Em/en dashes: no em dashes in the Doc; en dashes occur only in month ranges (Dec–Feb) and are rendered with a hyphen (Dec-Feb). Middots kept only in the homepage trust chips.
- Bracket markers never visible: [Form fields] rendered as the contact form, [Submit button: Get Help Now] as its button label, [Embed Google Map] as the map.
- Internal links: header/footer (Tab 28 exactly: Services 15, Areas 9, About, Contact) + homepage service cards + areas list + first-occurrence prose links to existing pages only, never to the page itself. All 27 distinct internal links per page resolve (checked live in QA).
- Footer bottom bar exactly per Tab 28 (© 2026 … · About · Contact · Privacy Policy · Terms). Privacy/Terms are footer text only — no invented privacy/terms pages.

## Images (54 files, 7.1 MB, all in public/images/)
- 1 hero + 1 in-content image per page, local SEO filenames (mcdonough-<slug>-hero/second.jpg), resized to their boxes (hero 1200×900, in-content 1100×420), JPEG quality 82, no AI word in filename/alt/metadata, not claimed as real job photos.
- Viewed by pixels: 2 contact sheets (all 27 heroes + all 27 seconds) + full-size views of the 2 replacements.
- Hash check: 54/54 unique inside this site; scanned 31,571 images elsewhere in ~/workspace, ZERO hash collisions — nothing copied from any other site in the workspace.
- First image round rejected and replaced: competitor restoration/plumbing/roofing company images, real-estate listing photos, a GoFundMe personal flood photo, an AI-named file (Gemini_Generated_Image), funnel-builder images, and a COVID disinfection photo used for sewage. Second round used generic subjects with a strict denylist.

## QA sequence (all local, no deploy/push/DNS)
### 1x build
- `next build` passes; 27/27 routes static.

### UI/UX round 1 (fresh screenshots desktop 1366 + mobile 390, every page)
- Measurements: 27/27 overflow 0 at 320/390/768/1024/1366, H1 = 1 per page, body 19 px, maps = 1 per page, all images load, all links resolve.
- Defects found + fixed (3 + 1):
  1. Flood hero looked illustrated/AI-like → replaced with a photographic flooded street (Flooded sign, submerged cars, emergency vehicles), pixel-verified full-size.
  2. Toilet second image was shower tiles → replaced with a toilet base leaking onto tile, pixel-verified full-size.
  3. Contact page "Open 24 hours, 7 days a week." line was stolen into hero chips → fixed: trust chips only from the first 4 blocks (homepage only). Contact now shows 0 hero chips, homepage 3, Hours line back in body.
  4. Topbar was inside the sticky header (would stick on scroll) → moved outside; verified after scroll: topbar bottom −562, header top 0, header height 73.
- False alarm owned: first QA run measured a Texas site because port 8901 was already serving another agent's site. That run was discarded, the QA script was patched to use port 8917 + a homepage-title guard, and the round was re-run clean.
- Map note (honest limit): Google Maps tiles could NOT render in this VM's headless browser (ERR_TUNNEL_CONNECTION_FAILED to google.com; curl returns 301 to Google). The embed URL is the standard `google.com/maps?q=<place>&output=embed` format, the iframe is present on every page (1 per page, 420 px desktop / 320 px mobile, rounded + shadow), and a visible "Open <place> in Google Maps ↗" fallback link was added under every map. Tile rendering in a real browser still needs the user's own check.

### UI/UX round 2 (fresh, after fixes)
- 27/27 PASS: overflow 0 at all widths, H1 = 1, H1 navy / H2 aqua, body 19 px, maps 1, links 27 distinct per page, zero out-of-bounds elements, zero broken images.

### Alignment check (dedicated, 5 widths)
- 320 / 390 / 768 / 1024 / 1366: overflow 0 on all 27 pages, zero out-of-bounds elements, hero call buttons single-line (53 px at 320, 57 px at 1366 — no wrapping), homepage service cards equal height in row (159 px × 6 sampled), trust chips nowrap with no split names, tables stack on mobile with no horizontal scroll, topbar scrolls away while the main header stays sticky.

### ADDED PHASE — per page, per section, round 1
- Sections measured per page (hero + 8–22 sections + footer, 1366 + 390): overflow 0, hero call button above the fold on every page at both widths (Y 558–836 px of a 900 px viewport; about-us mobile 836 px is the closest, plus the sticky mobile call bar always present), section heading colours only navy (H1, 54 checks), aqua (H2, 720 checks), white (footer H3, 54 checks) — no clashes.
- Images per section: all load, no stretch (object-fit/center-crop to box), no reuse (54 unique hashes). The script's first "oversize" flag was a miscalibrated threshold (1200 px source rendered at 443 px is retina-appropriate, not heavy) — corrected, not counted as a defect.
- User POV (5 seconds): phone in topbar + header + hero button + sticky mobile bar on every page; service and city are in the H1 + lead paragraph above the fold.
- Google POV: 1 H1 per page, heading order clean (no H3 before any H2), 28 unique titles (27 pages + 404; lengths 34–83 chars), metas 134–232 chars, LocalBusiness schema on all pages + FAQPage schema on the 26 pages with FAQs, HTML 19–51 KB per page, first-load JS 98.9 KB, no hidden/duplicate content, no duplicate images.
- Fresh screenshots for this round: screenshots/added1shots (27/27 pass).

### ADDED PHASE — per page, per section, round 2 (fresh)
- Section re-measurement + fresh screenshots (screenshots/added2shots): 27/27 pass, ZERO differences vs round 1 (same hero call Y, same overflow, same section counts). No new defects.

## Defects still open (need the user's word — NOT fixed by inventing anything)
1. Domain: the Doc gives slugs but no domain, so there are no canonical URLs and no sitemap.xml yet. Both must be generated from the real domain once the user gives it (or confirms one). Nothing was invented.
2. Contact form delivery: the Doc lists form fields but no email/backend. The form is present with all 7 fields + "Get Help Now", but on submit it honestly tells the visitor to call (470) 745-9798 because no delivery address is connected. Needs the user's word for a destination (e.g., FormSubmit activation like Tulsa) before it can deliver.
3. Google Maps tiles: see the honest limit above — needs one check in the user's real browser.
4. Homepage meta description is 232 chars (derived from the Doc's first paragraph because Tab 1 has no meta line); Google will truncate it in results. Visible content is unaffected.
5. No deploy, no GitHub push, no domain/DNS change was made (local only, as ordered).

## Screenshots
- screenshots/uiux1/ (27 desktop + 27 mobile, round 1)
- screenshots/uiux2/ (27 + 27, round 2)
- screenshots/align/align.json (5-width alignment measurements)
- screenshots/added1/sections.json + screenshots/added1shots/ (added round 1)
- screenshots/added2/sections.json + screenshots/added2shots/ (added round 2)
- screenshots/contact-hero.jpg, contact-second.jpg (pixel image sheets)

## ROUND 2 (2026-11-02, local only — rest all good, only the ordered changes)

### 1. Service + area images added (homepage, previously text-only)
- 15 service card images (one per service, `mcdonough-card-<slug>.jpg`, 800×500, JPEG 82) + 9 area card images (`mcdonough-area-<city>.jpg`, 800×500) = 24 new images. Total site images now 78 (54 + 24), 9.06 MB, all 78 unique hashes.
- Rendering: service cards now have a 16/10 media box on top (object-fit cover, flush, no white strips, no stretch); the homepage "Areas We Serve" plain bullet list is now a 3-column area-card grid (same card pattern, image + city link). Both grids collapse 3→2→1 columns at 1024/600 px. No other page got a new invented section: service/city pages have no servicecards/areas blocks in the Doc, so their services+areas presence stays header dropdowns + footer lists + their own hero/second images (re-checked below).
- Pixel verification: contact sheets viewed for all 24 new + all 54 existing images. Rejected and replaced on pixels/source: (a) toilet card was a cartoon illustration → photographic flooded bathroom; (b) flood card was a ServiceMaster competitor hero → photographic flooded living room; (c) ceiling card was a roofing-company blog image → photographic dripping ceiling; (d) structural card was a roofing/restoration blog image → photographic basement fans + dehumidifier (from a vacuum blog, cleanest generic source found); (e) commercial card was a Vietnamese storm-news lobby photo → photographic flooded office corridor; (f) slab card was a plumbing-company image → photographic wet tile floor. Retry round also rejected an illustrated structural sketch (icons + 60% RH graphic) and an AI-named "generated-image" product shot before any use.
- Existing 54 re-checked: replaced 4 weak/AI-vibe ones — structural hero was a white-background product render with callouts → photographic basement dehumidifiers; structural second was a blue air mover on black → photographic basement drying setup; toilet hero showed a dry tiled floor with no water → photographic overflowing toilet; emergency second was a mop + bucket (not extraction) → photographic carpet extraction wand. All other heroes/seconds kept: photographic and topic-correct (kept notes: appliance hero is a clean laundry room, commercial hero a clean office lobby, sewage second gloved sink cleaning — topic-adjacent, photographic, no branding; not replaced because no genuine defect).
- Hash check: 78/78 unique inside the site; 31,571 images scanned elsewhere in ~/workspace, ZERO collisions — nothing copied from any other site. No AI word in any filename/alt/metadata; images are not claimed as real job photos. 9 pre-existing 1200×900 heroes are 202–353 KB (retina-appropriate, same as round 1's settled standard); all 24 new cards/areas are ≤142 KB.

### 2. Meta/title trims (ONLY over-limit ones, Doc words preserved, hard ban honoured)
- Method: try replacing " | " with a space (keeps every word, −2 chars); if still over 60, drop the trailing descriptor after " | " (keeps the core title + ZIP where present). Metas: homepage cut to a Doc-words-only prefix ending at a clause; city metas over 160 dropped only the trailing "Call (470) 745-9798." clause (phone still appears in topbar, header, hero and sticky bar on every page).
- Before → after (decoded chars; titles ≤60, metas ≤160 after; full table in the round-2 report):
  - Homepage: title 83 → 46 ("24/7 Water Damage Restoration in McDonough, GA"), meta 227 → 155.
  - Services: emergency 61 → 59, burst 64 → 37, flood 61 → 59, sewage 62 → 60, ceiling 66 → 41, mold 64 → 30, structural 66 → 33, commercial 73 → 49, slab 62 → 60, water-heater 65 → 39, appliance 61 → 59, AC 66 → 34, hardwood 65 → 41, toilet 66 → 37. All service metas already ≤160, unchanged.
  - Cities: Stockbridge 67 → 46, Locust Grove 62 → 60, Hampton 70 → 42, Jonesboro 74 → 44 + meta 165 → 144, Lovejoy 70 → 42, Forest Park 61 → 59 + meta 179 → 158, Conyers 63 → 42 + meta 164 → 143, Griffin 70 → 42 + meta 167 → 146, Jackson 71 → 42 + meta 164 → 143.
  - Unchanged (already in limit): about 45/142, contact 59/135, crawl 60/136. 404 meta (layout default, template artifact) 232 → 155 via the same trimmed homepage description; no 404 story invented.
  - Verified in built out/ HTML (decoded): ZERO titles >60, ZERO metas >160 across all 27 pages + 404.
  - HARD BAN verified after all edits (grep over app/components/data): ZERO occurrences of "free estimate", "certified", "licensed" (or variants) in any title, meta, alt, or visible text — same as before the round.
  - Visible Doc content untouched: 0/27 pages have any changed content block; colours (H1 navy #0B2F4A / H2 aqua #0E8AC0), header, footer and phone (470) 745-9798 unchanged.

### 3. Testing — 2x mazeed + final 10x (all fresh, no reused reports)
- Mazeed round 1 (qa.py, 27 pages × 1366 + 390 + 320/768/1024): overflow 0 everywhere, H1 = 1, links 27 distinct per page, 0 missing links. One flag investigated, not a defect: 16 homepage card/area images read naturalWidth 0 at measurement time — files exist in out/ (78/78) and after a scroll + wait all 26 homepage images load (all ok: True). Cause: lazy below-fold images measured before scrolling. QA script patched (scroll to bottom + back before measuring) and the flag cleared in round 2.
- Mazeed round 2 (patched qa.py, fresh screenshots): 27/27 PASS, 0 failing — overflow 0 at all 5 widths, homepage 26/26 images ok on desktop AND mobile, zero out-of-bounds elements, titles/metas all in limit. Homepage desktop + mobile screenshots viewed: service cards and area cards render loaded, flush, aligned (crops: services Hidden-Leaks/Commercial rows, all 9 area cards).
- Final 10x pass (section.py, per section per page at 1366 + 390): 936 section measurements, overflow 0 everywhere, hero call button visible above the fold on all 27 pages at both widths (Y 558–836 px of 900 px), sticky call bar visible everywhere, heading colours ONLY navy rgb(11,47,74) ×54, aqua rgb(14,138,192) ×720, white footer ×54 — no clashes. The 40 "broken" flags in this pass are the same known no-scroll lazy artifact (homepage cards/areas only, zero on any inner page) and are already disproven by round 2's scroll-verified load; genuine defects in the 10x pass: ZERO. User POV: phone in topbar + header + hero + sticky bar on every page, service/city in H1 + lead above the fold. Google POV: 1 H1, clean heading order, unique in-limit titles/metas, LocalBusiness + FAQPage schema intact, HTML 19–56 KB/page, no hidden/duplicate content.
- Build: `npm run build` succeeds, 27 routes + 404 static, first-load JS 99.6 KB/page (shared 87.2 KB).

### Screenshots (round 2)
- screenshots/round2a/ (mazeed round 1, 54 shots + measurements.json), screenshots/round2b/ (mazeed round 2, 54 shots + measurements.json), screenshots/round2-10x/sections.json (10x section measurements), screenshots/round2-cards.jpg, round2-areas.jpg, round2-heroes.jpg, round2-seconds.jpg, round2-retry.jpg (pixel sheets).

### Still open (unchanged from round 1 — needs the user's word, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination. 3. Google Maps tiles check in the user's real browser. 4. No deploy, no push, no domain/DNS touch (local only).

## ROUND 3 — 10x beautify + optimize (local only, design/optimization only)

### Scope kept
- NO visible Doc content word changed (data/pages.json untouched, mtime 2026-11-02 00:44, pre-round-3).
- NO title/meta changed (verified in built out/ HTML, decoded: ZERO titles >60, ZERO metas >160, same as round 2).
- Banned phrases verified after all edits (grep over app/, components/, data/): ZERO occurrences of "free estimate", "certified", "licensed" or variants.
- NO AI word in any filename/alt/metadata (grep zero). Images not claimed as real job photos.
- Colours, header/footer structure, phone (470) 745-9798 unchanged except the one measured fix below. No deploy, no push, no domain/DNS touch.

### 1. Colour audit (WCAG contrast, measured, not guessed)
| Pair | Ratio | Verdict |
|---|---|---|
| H1 navy #0B2F4A on white | 13.82:1 | AA-normal PASS |
| H2 aqua #0E8AC0 on white / on mist #F3F8FB | 3.88 / 3.63:1 | AA-large PASS (H2 is 30–40px bold, so large-text threshold applies); AA-normal fails, but darkening H2 to aqua-dark would destroy the user-ordered H1-vs-H2 distinctness, so H2 stays aqua — logged, not changed |
| Links aqua-dark #0B6E99 on white / mist | 5.67 / 5.30:1 | AA-normal PASS |
| White on crimson CTA #D9232E / on crimson-dark hover #B81C26 | 4.96 / 6.50:1 | AA-normal PASS |
| Hero eyebrow crimson #D9232E on hero bg #EAF4FA | 4.45:1 | AA-normal FAIL by 0.05 — THE ONE colour defect found |
| Body ink #22303C, muted #4A5A6A, slate #243B53 on white | 13.50 / 7.09 / 11.50:1 | AA-normal PASS |
| Footer/topbar links #DCEBF5 on navy, bottom #B9CFDF on navy, white on navy | 11.35 / 8.59 / 13.82:1 | AA-normal PASS |
| Gold H2 underline #F2A93B on white (decorative, non-text) | 2.00:1 | Not a text pair; kept |
| Brand-mark / step-number white on aqua-navy gradient (large glyphs) | ~3.88:1 | AA-large PASS |
- FIX APPLIED (only colour change): hero eyebrow crimson → crimson-dark #B81C26. New ratio on hero bg: 5.82:1, AA-normal PASS. Verified in built CSS (--crimson-dark:#b81c26, hero-eyebrow uses it). Palette identity unchanged (same red family, H1 navy / H2 aqua distinct, crimson CTA untouched).
- Section rhythm kept: white / mist #F3F8FB alternation, navy CTA band, navy footer — no garish new palette thrown over the approved one.

### 2. Images — re-checked all 78 by viewed pixels, 5 replaced, weight DOWN
- Fresh contact sheets viewed: heroes (27), seconds (27), cards (15), areas (9). All photographic, no illustrated/AI look in the final set.
- REPLACED (pixel-verified full-size after replacement):
  1. appliance hero: clean laundry room, no water → washer edge + puddle on tile floor (600px source, clear leak).
  2. commercial hero: clean office lobby, no damage → flooded office, water dripping from ceiling, desks in water.
  3. commercial second: empty warehouse, no water → wet warehouse floor, boxes, reflective water.
  4. sewage second: gloved sink cleaning (topic-adjacent) → PPE workers mopping + "CAUTION WET FLOOR" sign, different photo from the sewage card.
  5. ac hero: clean AC unit, no leak → AC unit + brown drip stain on wall below (370px source; soft at 1080px full-size view, but sharp enough at the 523px rendered hero width — accepted, logged honestly).
- REJECTED, not used (with reasons): (a) first sewage-second candidate was a tighter crop of the SAME photo as the sewage card (same worker/wand/tank/plant) — rejected for in-site visual reuse, even though its hash differed; (b) ac-second candidate was a personal quote-upload image (cloudfront user upload) — rejected on provenance, attic second kept; (c) a COVID-disinfection photo and competitor restoration/plumbing hosts were skipped by the denylist, as in prior rounds.
- KEPT after re-judging: ac second (attic insulation — adjacent but the AC page's lead image is now the leak photo, and no better vetted candidate was found); slab second (cracked concrete — under-floor leak concept, no better vetted candidate); commercial/ac card images (already leak/water correct). Topic-adjacent list from round 1 is now: only ac second + slab second remain, both logged, neither replaced with a worse/provenance-risky image.
- OPTIMIZATION (script scripts/round3_optimize.py): heroes 1200×900 → 1080×810 (rendered ~523px, 2.06× retina), cards/areas 800×500 → 720×450 (rendered ~366px, 1.97× retina), seconds kept 1100×420 (rendered ~1140px banner), all re-encoded progressive JPEG q78, EXIF stripped.
- WEIGHT: public/images 9.06 MB (round 2) → 7.16 MB after optimization (measured 9.02 → 7.16 in the optimize run, −20.6%). Total out/ export 9.2 MB. First-load JS 99.6 kB (was 98.9 kB, +0.7 kB from focus/hover CSS — negligible).
- UNIQUENESS: 78/78 unique MD5 hashes in-site. No file copied from any other site in ~/workspace (replacements are fresh web-sourced generic photos, vetted by host denylist + pixel check — same licensing honesty limit as round 2: web-sourced vetted, NOT a stock-library licence purchase; a few sources are blogs/company pages, no visible branding in the photos).

### 3. Mobile + header/footer — measured fixes
- BEFORE (baseline, pre-fix, above-fold): Menu button 36px, nav toggles 40px, topbar phone link 24px — all under the 44px primary-control bar.
- FIXES (CSS only, app/globals.css): topbar link display:inline-block + .62rem vertical padding; nav-link/nav-toggle padding .55rem → .70rem; menu button min-height:44px. Plus: visible :focus-visible outline (3px aqua-dark, was missing entirely) and layout-neutral card hover (translateY −3px + shadow, image scale 1.03, overflow hidden so no reflow).
- AFTER (new build, measured): desktop header-call 50px, nav-toggle 44px, hero call/outline 57px, topbar call 44px; mobile menu button 44px, sticky call bar 57px, hero call 53px, mobile menu links 50px, form submit 47px. Dropdowns verified live: hover opens, Escape closes, click toggles, click-away closes. Mobile menu opens. Sticky header top = 0 after scroll, topbar scrolled away (bottom −1878px), call bar visible.
- HONEST LIMIT on tap targets: inline prose links and footer list links remain at text height (24–26px) — prose links are WCAG-exempt as inline text, and footer list links follow the same pattern as all prior approved rounds. Making every footer/card/prose link 44px tall would roughly double footer height and was NOT applied silently; if the user wants that, it is a further design change. Primary controls (the ones a panicked visitor actually taps) are all ≥44px.
- Footer unchanged: Tab 28 exact 4 columns + bottom bar, links and phone intact. Map presentation unchanged (embed + fallback link; tiles still need the user's real-browser check, as in prior rounds).

### 4. Fresh 10x testing (round 3, no reused reports)
- Build: `npm run build` passes, 27 routes + 404 static, out/ 9.2 MB.
- QA round 3 (scripts/qa.py, screenshots/round3/, 54 full-page shots + measurements.json): 27/27 PASS — overflow 0 at 320/390/768/1024/1366, H1 = 1 per page, all images load (homepage 26/26 incl. cards/areas), maps = 1 per page, ZERO missing internal links.
- Per-section 10x pass (scripts/section.py, screenshots/round3-10x/sections.json): 936 section measurements, overflow fails 0, hero call button visible above the fold on all 27 pages at 1366 + 390 (Y 578–856px of 900px; about-us mobile 856px closest, plus sticky call bar), heading colours ONLY navy rgb(11,47,74) ×54, aqua rgb(14,138,192) ×720, white footer ×54 — no clashes. The section script's "badimgs" flags are its known miscalibrated threshold (|natural − rendered| > 400px): every flagged image has ok=True and the natural size is retina headroom (heroes 1080 vs 443 rendered, seconds 1100 vs 358 mobile), NOT a defect — same artifact as round 1, corrected interpretation, not counted.
- User POV: phone in topbar + header + hero + sticky bar on every page; service/city in H1 + lead above the fold. Google POV: 1 H1, clean heading order, unique in-limit titles/metas, LocalBusiness + FAQPage schema intact, HTML per page unchanged in structure, no hidden/duplicate content.
- GENUINE DEFECTS in round 3 testing: ZERO after the fixes above (colour eyebrow + tap targets + focus were the fixes; no new defect was found in the fresh passes, so no second rebuild was needed).
- Screenshots viewed by the agent: round3 contact sheets (heroes/seconds/cards/areas), replacement full-size views (appliance, commercial, sewage, AC heroes/seconds), homepage mobile top crop (topbar/header/hero/call bar) and commercial desktop top crop (header/hero/new flooded-office image) — all clean, no break, no awkward line breaks.

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form still honestly tells visitors to call). 3. Google Maps tiles check in the user's real browser (headless VM cannot render tiles; embed + fallback link in place). 4. If the user wants stock-only image licensing or 44px-tall footer/prose links, those are further constraints, not met/applied in this round.

## ROUND 4 — mazeed 10x killer end level (local only, design/optimization only)

### Scope kept
- NO visible Doc content word changed: data/pages.json untouched (mtime 2026-11-02 00:44, pre-round-3). CSS diff vs round 3 is ONLY the text step + mobile hero padding/H1 trims below.
- NO title/meta changed (verified in built out/ HTML, decoded: ZERO titles >60, ZERO metas >160, same as rounds 2–3).
- Banned phrases verified after all edits (grep over app/, components/, data/): ZERO occurrences of "free estimate", "certified", "licensed" or variants.
- NO AI word in any filename/alt/metadata (grep zero in prior rounds, filenames unchanged in round 4). Images not claimed as real job photos.
- Colours, header/footer structure, phone (470) 745-9798 unchanged except the measured fixes below. No deploy, no push, no domain/DNS touch.

### 1. Text bigger — measured, before → after (computed px, desktop 1366)
- Body: 19px → 21px desktop; 18px → 19px mobile (measured in QA: bodySize 21px desktop / 19px mobile on all 27 pages).
- H1: clamp(2.6rem,5vw,3.6rem) → clamp(2.8rem,5.2vw,3.9rem); measured 57.6px → 62.4px desktop. Mobile H1: 2.4rem (round 3) → 2.6rem → 2.5rem final (see defect fix below; still above round 3).
- H2: clamp(1.9rem,3.4vw,2.5rem) → clamp(2.05rem,3.6vw,2.7rem); measured 40px → 43.2px desktop.
- H3 1.32rem → 1.42rem; hero lead 1.28rem → 1.38rem; buttons 1.02rem → 1.06rem; service/area card titles 1.12rem → 1.18rem; tables 0.98rem → 1.02rem; FAQ summaries 1.08rem → 1.14rem.
- Header/nav text UNCHANGED (no header wrap risk): brand, nav-link/nav-toggle, topbar, dropdown sizes kept from round 3.
- H1 navy #0B2F4A / H2 aqua #0E8AC0 distinctness kept; eyebrow crimson-dark #B81C26 from round 3 kept. Line-height kept 1.7.

### 2. Defect found by the bigger text — and fixed (not hidden)
- About-us mobile hero call button moved from Y=856px (round 3) to Y=903px after the text step — 3px BELOW the 900px fold. First trim (mobile hero padding 2.2/2.4rem → 2.0/2.2rem) brought it to exactly 900px, still not above the fold. Second trim (mobile hero padding → 1.9/2.1rem + mobile H1 2.6rem → 2.5rem, still above round 3's 2.4rem) brought it to Y=892px, verified on the final build. Desktop about hero Y unchanged at 795px. No other page came close to the fold edge (next worst mobile: appliance 799px).
- Honest note: on about mobile the hero call at 892px sits just above the fold edge and is partly covered by the fixed sticky call bar (57px) — the visitor still always sees a call button (the sticky bar) on that screen, exactly as in prior rounds.

### 3. Images killer level — 2 replaced, 1 kept with reasons, weight DOWN
- Re-checked all 78 by viewed pixels at rendered size (fresh round-4 contact sheets: heroes, seconds, cards, areas) + section-pass rendered/natural sizes. Final set all photographic, no illustrated/AI look.
- REPLACED:
  1. AC hero: old source was a 370px photo upscaled to 1080px (soft at full size). Found the SAME photo's true high-res source (1408×938, via a Sanity CDN image on a household water-damage blog page) — same subject, wider framing, now a true 1080×810 file, pixel-verified sharp in situ (AC desktop top crop viewed).
  2. AC second: old dry attic insulation (topic-adjacent, no water, no AC) → air handler + condensate drain pipe + full drip pan with water + wet trail on concrete (1536×1024 source, HVAC-company blog photo, no visible branding), cropped to 1100×420 banner, pixel-verified full-size.
- REJECTED before use (caught by pixel check): first AC-second candidate was a ceiling water-stain photo — pixel comparison proved it is the SAME photo as the existing ceiling-leak hero (same stain, curtain and window), so it was reverted within minutes and never shipped as a duplicate. A 370px square crop of the AC hero itself was also rejected as no improvement.
- KEPT with reasons: slab second (cracked concrete + wet patches) stays — the slab hero already shows wet tile inside, and the second shows the slab itself cracked and wet, a complementary symptom, not a duplicate. Slab-query candidates that could beat it were competitor plumbing images or an AI-named image, both rejected by the denylist. AC card (small Samsung logo on the unit) is a pre-existing product mark in a real photo, not site branding, left as-is.
- WEIGHT: public/images 7.16 MB (round 3) → 7.11 MB (7,108,543 bytes) after replacements + re-encode (AC hero 57,381 → 51,795 bytes; AC second 94,289 → 50,827 bytes). Total out/ export 9.16 MB. First-load JS unchanged at 99.6 kB.
- UNIQUENESS: 78/78 unique MD5 hashes in-site. Workspace-wide hashcheck on the final set: 78 images, 31,612 other-site images scanned, COLLISIONS: none — nothing copied from any other site. Same licensing honesty limit as prior rounds: web-sourced vetted generic photos, NOT a stock-library licence purchase.

### 4. Every section proper optimization end level
- Spacing rhythm kept (section padding, hero padding as fixed above); card heights: homepage desktop service cards equal in row (389/389/389 sampled); mobile single-column cards vary by content length only, as designed.
- Tables: larger text (1.02rem) re-tested — stack on mobile with no horizontal scroll, overflow 0 at all widths.
- Tap targets (measured, final build): desktop header-call 50px, nav-toggle 44px, hero call 60px; mobile menu button 44px, hero call 56px, sticky call bar 57px. Inline prose/footer links remain at text height (round-3 exception, unchanged — user has not ordered the 44px footer change).
- Map presentation unchanged (embed + fallback link; tiles still need the user's real-browser check).

### 5. Fresh 10x testing (round 4, no reused reports)
- Build: `npm run build` passes, 27 routes + 404 static, out/ 9.16 MB.
- QA process honesty: the first round-4 QA run (single browser, qa.py) crashed on a full-page screenshot after 7 pages (Chromium target crash, low memory + orphaned browser; ~900 MB freed by killing the orphan). It was replaced by scripts/round4_qa.py (fresh browser per page) and scripts/round4_qa_part.py / round4_measure.py (slice runs). One script bug of mine (link-check spread) was caught and fixed mid-run; the affected page was re-run clean. A later batched run was SIGTERM-killed at page 21/27 with its buffered output lost — the remaining 6 pages were re-run in foreground slices, and all 27 pages were then re-measured on the FINAL build (measurements-a/b/c), so no result below rests on the killed run.
- Final QA measurements (screenshots/round4/measurements.json, merged from a/b/c on the final build): 27/27 PASS — overflow 0 at 320/390/768/1024/1366, H1 = 1 per page, body 21px desktop / 19px mobile, H1 62.4px navy rgb(11,47,74), H2 43.2px aqua rgb(14,138,192), maps = 1 per page, ZERO missing internal links, ZERO bad images (all images load after scroll).
- Full-page screenshots: screenshots/round4/ (54 shots, desktop + mobile). Note: shots for pages 0–20 predate the final mobile hero padding/H1 trims by a few pixels only (desktop CSS unchanged in those trims); final-build top crops were taken separately and viewed: view-home-m-top.png, view-ac-d-top.png, view-about-m-top.png — all clean, no break, no awkward line breaks. About full-page shots were re-taken on the final build via the QA-part run.
- Per-section 10x pass (scripts/round4_section.py, screenshots/round4-10x/sections.json): 936 section measurements (same section count as round 3 — structure unchanged), overflow fails 0, hero call visible above the fold on all 27 pages at 1366 + 390, sticky call bar visible on mobile everywhere, heading colours ONLY navy rgb(11,47,74) ×54, aqua rgb(14,138,192) ×720, white footer rgb(255,255,255) ×54, empty ×108 (sections with no heading, e.g. CTA/map) — no clashes, bad images 0. Rendered/natural ratios: largest 3.88× is mobile hero retina headroom (1080px natural vs 278px rendered), not a defect; smallest 0.965× is seconds rendered at 1140px vs 1100px natural (3.5% upscale, visually sharp in full views).
- User POV: phone in topbar + header + hero + sticky bar on every page; service/city in H1 + lead above the fold. Google POV: 1 H1, clean heading order, unique in-limit titles/metas, LocalBusiness + FAQPage schema intact, HTML 19,670–56,137 bytes/page, no hidden/duplicate content.
- GENUINE DEFECTS after fixes: ZERO.

### Screenshots (round 4)
- screenshots/round4/ (54 full-page shots + measurements.json + sheet-heroes/seconds/cards/areas.jpg + view-home-m-top.png, view-ac-d-top.png, view-about-m-top.png)
- screenshots/round4-10x/sections.json (936 section measurements)
- Scripts: scripts/round4_qa.py, round4_qa_part.py, round4_measure.py, round4_section.py, screenshots/round4/hashcheck.log (78 images, 31,612 scanned, 0 collisions)

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form still honestly tells visitors to call). 3. Google Maps tiles check in the user's real browser (headless VM cannot render tiles; embed + fallback link in place). 4. If the user wants stock-only image licensing or 44px-tall footer/prose links, those are further constraints, not met/applied in this round.

## ROUND 5 — User review catches + Addendum (images) + Addendum 2 (call bar) — DONE 2026-11-02 (local only, parent-verified pending)
User, after viewing all-page screenshots, caught 3 defects: (1) headings break lines unnecessarily, (2) text unnecessarily small and broken, (3) irrelevant images. Reinforcement: every page 100% relevant best-ever optimized images (or say honestly where not met); header/footer 100% web + mobile friendly, re-verified on all 27 pages. Addendum 2: replace the plain topbar line above the header with a beautiful popping call-number bar; 10x more optimization of every section + header + footer. LOCAL ONLY: no deploy, no push, no domain/DNS touch. No visible Doc content words changed, no title/meta changes, data/pages.json untouched (mtime still 2026-11-02 00:44).

### 1. Audit first (before-state, screenshots/round5/audit.json, same script as after-runs)
- Overflow was 0 everywhere before — "broken" meant breaks + small text, not horizontal overflow.
- Headings before: desktop orphans 1 (about H1), mobile orphans 26 (mostly FAQ H2s ending in lone "Homeowners" etc.); desktop H1 21x3 lines / 6x4 lines (all 4-liners at the 578px hero text column); mobile H1 20x3 / 6x4 / 1x5 (appliance-leak, 11 words).
- Small-text root cause: body is 21px desktop / 19px mobile, but most UI text is rem-based against a 16px root, so it never scaled with the body bumps — topbar 14.08px, hero eyebrow 13.6px, figcaptions 13.6/14.08px, brand subline 10.88px, nav 15.68px, header call 16px, menu button 13.33px (no font-size set at all), card body 16px, tables 16.32px, footer H3 16.8px, footer bottom 14.72px, form fields 16px.

### 2. Headings — fixes + two wrap experiments, both decided by measurement, not theory
- Hero grid widened 1.05fr/.95fr -> 1.18fr/.82fr, gap 2.4rem -> 2rem (hero text column ~578px -> ~654px); hero lead max-width 34rem -> 38rem; heading line-height 1.18 -> 1.22. Result: desktop 4-line H1s 6 -> 1 (appliance-leak only), one H1 3 -> 2 lines.
- EXPERIMENT 1 — text-wrap:pretty: MEASURED WORSE and reverted. Homepage H2 went from last line 4 words (balance) to a lone "GA" (pretty); desktop orphans 1 -> 66, mobile 26 -> 74. Pretty is not used anywhere on this site.
- EXPERIMENT 2 — natural wrap on h1 only: MEASURED WORSE and reverted. H1 line counts unchanged (25x3 / 1x4 / 1x2 desktop) — Georgia italic at 62.4px is wider than estimated, so the theorised 2-line fit does not happen — while desktop H1 orphans rose 1 -> 7 (flood + Hampton/Lovejoy/Conyers/Griffin/Jackson H1s ending in lone "GA").
- FINAL: text-wrap:balance on h1/h2/h3 (audit-after.json = audit-after2 reverted state = measurements-final.json). Desktop orphans 1, mobile orphans 26, identical to before — i.e. the systemic breaks are fixed (4-line H1s, footer wraps, pretty's 66), and what remains is INHERENT, logged not claimed: desktop about H1 ("About McDonough Water Damage Restoration", 3 lines, "Restoration" alone — 5-word title, two very long words, 62.4px in a 654px column; no wrap mode fixes it without changing words or shrinking type, both forbidden); mobile 26 = long verbatim FAQ/city titles at 358px (e.g. "...Questions from McDonough Homeowners" ending in "Homeowners", "Is Black Mold Dangerous?", "Clean Water or Contaminated Water?"). Shrinking mobile H2s to ~24px would reflow some, but that undoes the ordered "text bigger" direction — not done silently.
- Footer H3 regression caught by the same QA and fixed: raising footer H3 to 1.25rem wrapped "Water Damage Services" to 2 lines in the 237px footer column (lone "Services"). Final 1.15rem: one line again, still larger than pre-round-5 1.05rem; H3 back to 117x1 line on desktop.

### 3. Text small/broken — raises (body NOT shrunk anywhere)
Topbar .88rem -> 1rem (superseded by the call bar below), brand strong 1rem -> 1.15rem, brand subline .68rem -> .8rem, nav/toggles .98rem -> 1.05rem, dropdown links .96rem -> 1.02rem then .6rem padding, header call 1rem -> 1.1rem, hero eyebrow .85rem -> .95rem, buttons 1.06rem -> 1.12rem, chips .92rem -> 1rem, figcaptions .85/.88rem -> 1.05rem, card titles 1.18rem -> 1.22rem, card body 1rem -> 1.1rem, tables 1.02rem -> 1.1rem, FAQ summaries 1.14rem -> 1.2rem, footer H3 -> 1.15rem (see above), footer bottom .92rem -> 1rem, form labels/inputs 1rem -> 1.08rem, form button 1.05rem -> 1.12rem, form note .95rem -> 1.02rem, menu button gained font-size 1.05rem, map fallback link .98rem -> 1.05rem, sticky call bar 1.05rem -> 1.12rem. Buttons and tables are out of the sub-17px list entirely on the final build. Remaining sub-17px items are judged intentional, not defects: topbar cue/info labels (15.2px), hero eyebrow label (15.2px), figcaptions (16.8px), map link (16.8px), nav links/toggles/menu (16.8px — 0.2px under the flag threshold; raising nav further risks header wrap at 1024px, where brand + nav + call already fill ~980 of 984px), brand subline (12.8px decorative subline), homepage chips (16px).

### 4. Images — strict first-glance re-audit of all 78, 6 replaced (same filenames, originals in superseded-round5/)
- REPLACED (all photographic, RGB, centre cover-crop to box ratio, LANCZOS resize, progressive JPEG q78, EXIF stripped, pixel-verified on a fresh contact sheet + in situ):
  1. About hero: clipboard inspector outside a house (generic, no water damage at first glance) -> two technicians inspecting a stained wall/baseboard with a moisture meter (1080x810, 106,391 bytes).
  2. About second: cropped man in a jacket, no context -> crew carrying an air mover into a flooded home, van outside (1100x420, 55,175 bytes).
  3. Hardwood hero: light dry-looking wood floor -> wet buckled hardwood + stained baseboard (1080x810, 100,049 bytes).
  4. Burst-pipe second: ceiling drip (a ceiling-leak subject, not a burst pipe) -> blue pipe joint spraying water (1100x420, 62,809 bytes).
  5. AC card: unit with a visible Samsung logo -> wall unit + brown drip stain, no visible logo (720x450, 24,835 bytes; source is an AC-servicing blog photo, no branding visible in the crop).
  6. Locust Grove area card: tree-lined street with a mountain backdrop (wrong for flat Henry County) -> same street cropped to remove the mountain backdrop, street/houses dominate (720x450, 79,173 bytes). HONEST LIMIT: a faint ridge sliver remains at the very top centre behind trees; a fully verified Locust Grove photo was not found without resorting to real-estate/generated sources, which were rejected.
- REJECTED before use: a "ChatGPT-Image"-named crew photo (AI provenance), a flood-restoration-company hero candidate (competitor host), burst-second candidates from restoration/mitigation company hosts, a hardwood candidate that pixel comparison proved was the current card photo family / a staged hand-on-floor shot, and all Locust Grove candidates (real-estate marketing photos, a "generated" neighbourhood image, an unknown listing CDN).
- KEPT with reasons: slab second (cracked concrete + wet patches — the slab itself, complementary to the wet-tile slab hero, not a duplicate); appliance hero (wet tile + washer edge = clearly a laundry leak); commercial heroes (flooded office/warehouse); sewage second (PPE mopping + wet-floor sign); all other heroes/seconds/cards judged clearly that exact service at first glance; all 15 service cards clearly relevant.
- WEIGHT: public/images 7,108,543 bytes (round 4) -> 7,226,041 bytes (+1.7%) — replacements are sized to their boxes at q78, but the new about/hardwood files are larger than the ones they replaced, so weight did not fall this round; still well below round 2's 9.06 MB.
- UNIQUENESS: 78/78 unique MD5 in-site; workspace hashcheck on the final set: 78 images, 31,619 other-site images scanned, COLLISIONS: none. Same licensing honesty limit as prior rounds: web-sourced vetted generic photos, NOT a stock-library licence purchase.
- HONEST LIMIT (addendum: no page falsely claimed 100%): service images are each clearly that exact service at first glance. CITY images are NOT verified photographs of that exact town — the 9 city heroes/seconds and 9 area cards are representative Georgia small-town/suburban imagery (homes, streets, downtowns). No town-specific verified photo was found for any of the 9 towns without resorting to real-estate listing photos or AI-generated images, both rejected. Provably town-specific photos would need the user's own town photos or a licensed per-town stock search — not met by this round.

### 5. Call bar — Addendum 2 (reading stated explicitly for user correction)
- READING APPLIED: the plain navy strip above the header ("Open 24 hours · McDonough & Henry County · Insurance paperwork help" left + "Call (470) 745-9798" right) is removed AS IT STOOD and replaced by a prominent call bar above the header. Phone (470) 745-9798 is the hero: crimson pill, 1.35rem / 21.6px bold white, shadow/glow, on a navy gradient bar with a 3px gold bottom border, plus a "Call Now · Open 24 Hours" cue. The old info is NOT lost: it stays in the same bar as subordinate text on desktop/tablet (and in the footer + homepage hero chips site-wide); on very small screens (<=540px) the small info line is hidden so the bar stays a popping call bar instead of a tall stack — number + cue stay. No new claim added, phone unchanged, header structure unchanged (bar sits outside the sticky header, so it still scrolls away). If the user meant something else (e.g. remove the bar entirely), this reading is stated for his correction — the old strip is not silently kept.
- MEASURED (screenshots/round5/header-check.json, all 27 pages x 1366/1024/390/320, 108 header-area shots in screenshots/round5/header/): call bar 78px tall desktop/tablet (old strip ~44px), 111px mobile (cue + pill stacked); pill 53px desktop / 49px mobile, font 21.6px / 19.2px, number white-space:nowrap (never wraps/breaks); overflow 0 at all 4 widths; header-inner never overflows (no wrap at 1024); after scrolling 1500px, header top = 0 and call-bar bottom < 0 on every page/width (sticky header, scrolling call bar, no double header); footer 4 columns on one row at 1366/1024, stacked single column at 390/320; dropdown hover opens + Escape closes on all pages; mobile menu opens on all pages. Viewed: header/home-1366.png and header/home-390.png — pill pops against navy with gold border, no overflow, number intact.
- Header/footer micro-polish on top: dropdown link padding .5rem -> .6rem (taller tap rows); footer links display:block with .3rem vertical padding (larger tap area without doubling footer height). Footer/prose links still not 44px tall (round-3 exception, unchanged — user has not ordered it).

### 6. Fresh 10x testing on the FINAL build (no reused reports)
- Final QA (scripts/round5_qa.py, screenshots/round5/measurements-final.json): 27/27 pass — overflow 0 at 320/390/768/1024/1366, H1 = 1, maps = 1 per page, zero broken images, dropdowns + mobile menu pass, header sticky + call bar scrolled away, no header-inner overflow, tap targets >=44px (header call 52, hero call 62 desktop / 58 mobile, sticky call bar 59, menu 44, nav toggles 45).
- Per-section 10x (scripts/round4_section.py, screenshots/round5/sections.json): 936 section measurements, overflow fails 0, bad images 0, hero call visible above the fold on all 27 pages at 1366 + 390 (desktop max about 790px; mobile max about 889px — inside the 900px fold, so the taller mobile call bar did NOT push the about hero call below the fold; next worst mobile appliance 799px), sticky call bar visible on mobile everywhere, heading colours ONLY navy rgb(11,47,74) (H1), aqua rgb(14,138,192) (H2), white (CTA band/footer) — no clashes. The 108 "no heading" section entries are the first two non-hero sections per page (lead/intro blocks, paragraph-led by design, same as round 4), not defects.
- QA process honesty: the pretty and natural-wrap regressions above were caught ONLY because the after-measurements were compared against the before-audit with the same script — both were reverted before delivery, and the final screenshots were re-taken after the last revert so the delivered set shows the true final state. Mobile full-page shots show the mobile menu EXPANDED because the QA script opens it to verify it — that is a capture artifact, not the default state (menu is closed by default). Map tiles are blank in the VM test browser (known tunnel block, not a site defect); embed + fallback link in place, still needs the user's real-browser check.
- Build: `npm run build` passes, 27 routes + 404 static, first-load JS unchanged 99.6 kB. Titles/metas all within limit (decoded) on the final build; banned phrases "free estimate" / "certified" / "licensed" = ZERO by grep over app/components/data.

### Screenshots (round 5, final build)
- screenshots/round5/ (54 final full-page shots, desktop + mobile, all 27 pages + measurements-final.json + sections.json + header-check.json + audit.json [before] + audit-after.json + audit-after2.json [reverted experiments] + sheet-heroes/seconds/cards/areas.jpg [before-state image sheets])
- screenshots/round5/header/ (108 header-area shots, 27 pages x 1366/1024/390/320)
- Scripts: scripts/round5_audit.py, round5_qa.py, round5_header.py, hashcheck.py, round4_section.py

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form still honestly tells visitors to call). 3. Google Maps tiles check in the user's real browser. 4. Stock-only image licensing or 44px footer/prose links, if wanted. 5. Correction of the call-bar reading above if he meant something else. 6. Provably town-specific city photos, if wanted (see honest limit in section 4).

## ROUND 6 — 2x fresh testing to set UI/UX — DONE 2026-11-02 (local only)

### Round 6A (fresh, pre-fix) — measurements + visual audit
- QA (scripts/round6_qa.py, screenshots/round6/round6a-measurements.json): 27/27 — overflow 0 at 320/390/768/1024/1366, H1 = 1, maps = 1 per page, zero broken images, body 21px desktop / 19px mobile, dropdown hover + Escape + mobile menu pass on all pages, footer 1 row desktop / 4 stacked mobile. Tap "0" values in the raw file are display:none elements only (menu button + sticky call bar on desktop, header call on mobile) — not defects; live tap targets were verified in Round 5 and re-checked in the header run below.
- Header run (scripts/round6_header.py, screenshots/round6/header-check.json, 108 header-area shots): overflow 0 at all 4 widths, header-inner never overflows, call bar 78px desktop / 111px mobile, pill 53px desktop (21.6px) / 49px mobile (19.2px), phone (470) 745-9798 on every page/width, scroll-away verified (header top = 0, call-bar bottom < 0 after scroll) on all 27 pages, footer 1 row at 1366 / stacked at 390/320, dropdowns + mobile menu pass everywhere.
- Headings (same script, both rounds): genuine orphans = desktop 1 (About H1 only) + mobile 26 (long verbatim FAQ/city titles) — IDENTICAL set to Round 5, NOT fixed and NOT claimed fixed; the single-word footer H3 "About" and single-word About H2 "Services" are not orphans (they are one word by nature) and were excluded from this count. Desktop H1 lines 25x3 / 1x2 / 1x4 (appliance-leak, 11-word title); mobile H1 lines 20x3 / 6x4 / 1x5.
- Small text: only the Round 5 intentional labels remain sub-17px (topbar cue/info 15.2px, eyebrow 15.2px, nav/toggles/menu 16.8px, brand subline 12.8px decorative, footer bottom 16px, map link + figcaptions 16.8px). Buttons/tables/body text are all at or above body scale. No mid-word break or truncation found.
- Images, viewed pixels (all 78, contact sheets in /tmp, not kept): every service hero/second/card is clearly that exact service at first glance. ONE GENUINE DEFECT FOUND: Jackson city hero carried a baked-in third-party watermark, "GEORGIA MLS REAL ESTATE SERVICES", bottom-left (1080x810 file, watermark y~730-810). A bottom-left corner scan of all 78 images confirmed this was the ONLY watermarked file. City heroes/seconds + area cards otherwise remain representative Georgia town/suburban imagery — NOT verified photos of each exact town (Round 5 honest limit, unchanged; Jonesboro's historic-street images are the weakest of the set in town-specificity but are plausible Georgia historic streets, not a different state's landmark).
- Visual (viewed): home desktop + home mobile top/footer, Jackson desktop top — call bar pops, H1s clean, flooded-living-room home hero clearly relevant, footer stacked/readable on mobile, Services dropdown opens with all 15 items readable. Mobile full-page shots show the menu EXPANDED only because the QA script opens it to verify it (capture artifact, not the default state). Sticky call bar overlays the bottom ~57px of viewport content while scrolling — standard sticky-bar behaviour, accepted in Round 5; hero calls still measure above the fold.

### Fix (Round 6A defect only — CSS/images, no content words, no title/meta changes)
- Jackson hero: bottom 90px cropped off the source file (1080x810 -> 1080x720), removing the MLS watermark entirely; same aerial Georgia countryside scene, no new photo, no fake content added. Original watermarked file preserved in superseded-round6/jackson-hero-with-mls-watermark-ORIGINAL.jpg. Re-saved progressive JPEG q78, EXIF stripped. New hash d69f3f403605cf1d6a21a0ab8bcca775 (matches in public/ and out/ after rebuild). Verified in situ on the Round 6B Jackson desktop top crop: aerial clean, no watermark, no branding.
- Image weight: out/images 7,226,041 -> 7,197,139 bytes (-28,902). 78/78 unique MD5 in-site; this round's workspace scan: 0 collisions vs 20,199 other scanned images (scan excluded screenshots/superseded/public copies, so the count differs from Round 5's 31,619 all-files scan; the collision result is the same: none).
- Build after fix: `npm run build` passes, 27 routes + 404, first-load JS unchanged 99.6 kB. data/pages.json untouched (mtime still 2026-11-02 00:44). Banned phrases "free estimate" / "certified" / "licensed" = ZERO by grep over app/components/data/public. Titles: 0 over 60; metas: 0 over 160 (decoded, 28 files incl. 404).

### Round 6B (fresh, post-fix) — re-verify
- QA (scripts/round6_qa.py, screenshots/round6/round6b-measurements.json, 54 fresh full-page shots in screenshots/round6/): 27/27, IDENTICAL measured results to 6A on every axis — overflow 0 at all widths, H1 = 1, maps = 1, zero broken images, body 21/19px, dropdowns + mobile menu pass, footer stacking correct, genuine orphans still exactly 1 desktop + 26 mobile (inherent set, unchanged by design).
- Per-section (scripts/round4_section.py, screenshots/round6/sections-final.json): 936 section measurements, overflow fails 0, bad images 0, hero call visible above the fold on all 27 pages at 1366 + 390 (desktop max About 790px; mobile max About 889px — inside the 900px fold; next worst mobile Jackson 738px), sticky call bar visible on mobile everywhere, heading colours ONLY navy rgb(11,47,74) (H1), aqua rgb(14,138,192) (H2), white (footer/CTA) — no clashes. The 108 "no heading" entries are the lead/intro blocks, paragraph-led by design (same as Rounds 4-5), not defects.
- Round 6A screenshots preserved separately in screenshots/round6a/ (54 shots + round6a-measurements.json); screenshots/round6/ now holds the final post-fix set (54 full-page + 108 header-area + round6a/round6b measurements + sections-final.json + header-check.json).

### Round 6 defect lists (summary)
- Round 6A defects: 1 genuine (Jackson hero MLS watermark) — FIXED and re-verified in 6B. 0 genuine heading defects beyond the known inherent orphans. 0 genuine text-size/wrap defects. 0 overflow/alignment/colour/header/footer defects. 0 broken images/links (maps counted, not tile-rendered — VM tunnel block, unchanged).
- Round 6B defects: 0 genuine defects. The inherent orphans, representative (not exact-town) city photos, stock-only licensing question, and 44px footer/prose links remain OPEN by design, not fixed by this round — see below.

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form still honestly tells visitors to call). 3. Google Maps tiles check in the user's real browser. 4. Stock-only image licensing or 44px footer/prose links, if wanted. 5. Correction of the call-bar reading if he meant something else (Round 5 reading stands). 6. Provably town-specific city photos, if wanted (needs his own town photos or a licensed per-town search).

## ROUND 7 — Section-by-section lovely optimization pass — DONE 2026-11-02 (local only)

Not a testing-only round: every section on all 27 pages was polished in CSS (one PageRenderer + Chrome, so polish applies site-wide per section), then re-verified fresh. No Doc word changes, no title/meta changes, data/pages.json untouched (mtime still 2026-11-02 00:44), banned phrases "free estimate" / "certified" / "licensed" = ZERO, no deploy/push/domain/DNS.

### Per-section polish list (before -> after, all in app/globals.css unless noted)
- Global typography: paragraph margin 1.05em -> 1.15em; list-item margin .45em -> .55em; gold-on-navy text selection added (::selection #F2A93B on #0B2F4A).
- Headings: H2 underline accent 64px -> 72px aqua-to-gold; H3 letter-spacing -.005em + section H3 top rhythm 1.5em (first H3 in a section exempt). H1/H2 sizes, colours, balance wrap UNCHANGED (Round 5 measured balance as best; pretty/natural were worse).
- Call bar + header: topbar pill + header call gain hover lift (translateY(-1px)) with transition; brand mark gains soft aqua shadow; dropdown current-page item padding .5rem -> .6rem in components/Chrome.tsx to match dropdown links exactly (no words changed).
- Hero: inner padding 3rem/3.2rem -> 3.4rem/3.5rem desktop; lead line-height 1.7 -> 1.72; chips vertical padding .4rem -> .5rem; hero image gains 1px line border for definition on the light hero background.
- Buttons/CTAs: padding .85rem -> .95rem vertical, 1.6rem -> 1.7rem horizontal; hover lift added (call + outline). No size reduction anywhere.
- Sections: padding 3.2rem -> 3.8rem desktop, 2.4rem -> 2.8rem mobile; mist sections gain 1px top/bottom line borders for cleaner alternation rhythm.
- Steps (5-things/process): number circle 2rem -> 2.2rem, left padding 3.2rem -> 3.5rem, item vertical padding 1rem -> 1.15rem, item gap 1.05em -> 1.15em.
- Service + area cards: grid gap 1.3rem -> 1.5rem; card body padding 1.4rem -> 1.6rem (service) / 1.1rem -> 1.3rem (area); card title 1.22rem -> 1.28rem; card paragraph top margin .6em -> .7em. Hover lift/scale unchanged.
- Tables: header padding .8rem -> .95rem, cell padding .75rem -> .9rem; row hover tint #EAF4FA added.
- FAQ: summary padding 1rem -> 1.15rem, font 1.2rem -> 1.25rem, hover mist background, open summary mist background + aqua-dark text.
- CTA band: padding 2.4rem/2rem -> 2.9rem/2.4rem, 4px gold top accent added.
- Map + figures: iframe height 420px -> 440px desktop; figure image height 420px -> 440px desktop, caption padding .55rem -> .7rem. Mobile map height unchanged (320px).
- Footer: 3px gold top border (matches call bar), inner top padding 3rem -> 3.5rem, column gap 2rem -> 2.4rem, bottom bar padding 1.1rem -> 1.35rem, footer H3 letter-spacing .01em.
- Form (contact): card padding 1.8rem -> 2.1rem, label gap .9rem -> 1rem, input padding .75rem -> .85rem, button padding .85rem -> .95rem + crimson shadow + hover lift (no words, no new fields, delivery still honestly call-only).
- Mobile rhythm: section padding 2.8rem (above); hero mobile padding polish REVERTED (see regression note below).

### Images (optimization only — no replacements, no new photos, no provenance risk)
- The 3 heroes over 200KB re-encoded q78 -> q74 progressive, EXIF stripped, same dimensions: Stockbridge hero 248,726 -> 241,333 B (-3.0%), Hampton hero 213,239 -> 206,235 B (-3.3%), Jackson hero 200,448 -> 194,720 B (-2.9%). Originals preserved in superseded-round7/. All other 75 images already q78 and sized to their boxes; re-encoding them further would trade visible quality for bytes, not done.
- Total image weight: 7,197,139 -> 7,177,014 bytes (-20,125, -0.28%). All 78 RGB, 78/78 unique MD5 in-site, 0 collisions vs 31,620 other-site images (scripts/hashcheck.py full run). Rendered sizes confirmed by the section run (e.g. hero 372x279 from 1080x810 source, figure 1140x440 from 1100x420 source, cards 362x226 from 720x450) — sources stay ~2x rendered width for sharpness, not bloated.
- Relevance: no image replaced because Rounds 5-6 already verified all 78 by viewed pixels and the only genuine defect (Jackson watermark) was fixed in Round 6; the 3 re-encodes are the same scenes, pixel-identical content. City-photo honesty UNCHANGED: city heroes/seconds + area cards remain representative Georgia town/suburban imagery, NOT verified photos of each exact town.

### Polish-caused regression found and fixed (owned plainly)
- First Round 7 build FAILED twice on CSS syntax: my scripted edits closed the .btn, FAQ summary, and form-button rules early (a `}` inserted before the rule's remaining declarations). Caught by the build itself, fixed line by line, then the whole file brace-checked (final depth 0, zero mid-rule stray braces) and rebuilt clean: `npm run build` passes, 30 static routes (27 pages + 404 + extras), out/images 7,177,014 bytes.
- Mobile hero padding polish (2.1rem/2.4rem) pushed the About mobile hero call to 899px — 1px inside the 900px fold, too tight. Reverted to Round 6 mobile hero padding (1.9rem/2.1rem) with a comment in the CSS. Final section run on the final build: About mobile hero call 896px (inside the fold, but tight — next worst mobile page is 804px; the sticky call bar still keeps a call visible regardless, same honest limit as Round 4).

### Fresh re-verify on the FINAL build (no reused reports)
- QA (scripts/round7_qa.py, screenshots/round7/measurements.json, 54 full-page shots): 27/27 — overflow 0 at 320/390/768/1024/1366, H1 = 1, maps = 1 per page, zero broken images, body 21px desktop / 19px mobile, dropdown hover + Escape + mobile menu pass, sticky header + scrolling call bar verified. Orphans IDENTICAL inherent set: desktop 1 (About H1) + mobile 26 (long verbatim FAQ/city titles) — NOT claimed fixed. Small-text list identical to Rounds 5-6 intentional labels only (topbar cue/info 15.2px, eyebrow 15.2px, nav/toggles/menu 16.8px, brand subline 12.8px decorative, footer bottom 16px, map link + figcaptions 16.8px).
- Header run (scripts/round7_header.py, screenshots/round7/header-check.json, 108 header-area shots): identical to Round 6 on every axis — overflow 0 at 1366/1024/390/320, call bar 78px desktop / 111px mobile, pill 53px (21.6px) / 49px (19.2px), phone (470) 745-9798 on every page/width, header-inner never overflows, scroll header top = 0, dropdowns pass. No header/footer regression from the gap/padding changes.
- Per-section FINAL (scripts/round4_section.py, screenshots/round7/sections-final.json): 936 section measurements, overflow fails 0, bad images 0, hero call visible above the fold on all 27 pages at 1366 + 390 (desktop max About 802px; mobile max About 896px, next worst 804px), heading colours ONLY navy rgb(11,47,74) (H1), aqua rgb(14,138,192) (H2), white (footer/CTA) — no clashes. The 108 "no heading" entries are lead/intro blocks, paragraph-led by design (same as Rounds 4-6), not defects.
- Visual (viewed): home 1366 header crop (call bar pops, gold border, brand shadow, H1 3 lines clean) + home desktop hero crop (lead rhythm, buttons, chips, flooded-hardwood hero clearly relevant, Services dropdown with all 15 items). Full-page home shots are 1366x15566 / 390x28014 and did not render in the viewer at full size, so verification rests on the crops + measurements, stated honestly. Mobile full-page shots show the menu expanded only because the QA script opens it (capture artifact, not default state). Map tiles blank in the VM test browser (known tunnel block, not a site defect; embed + fallback link in place).
- Honesty note on screenshots: the 54 full-page + 108 header shots in screenshots/round7/ predate the final mobile-hero-padding revert by ~10px on mobile only (desktop CSS unchanged by that revert); the FINAL section numbers above ARE on the final build.

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form still honestly tells visitors to call). 3. Google Maps tiles check in the user's real browser. 4. Stock-only image licensing or 44px footer/prose links, if wanted. 5. Correction of the call-bar reading if he meant something else (Round 5 reading stands). 6. Provably town-specific city photos, if wanted (needs his own town photos or a licensed per-town search).

## ROUND 8 — 10x audit using the new audit list — DONE 2026-11-02 (local only)

Sequence followed exactly as ordered: the audit list document was created FIRST
(`AUDIT-LIST-10X.md`), THEN the 10x audit was run using it. No Doc word changes,
no title/meta changes, data/pages.json untouched, banned phrases ZERO, no
deploy/push/domain/DNS. All Round 8 runs are on the final post-fix build (the
self-link fix below was built before the QA/header/section runs).

### The audit list document
- `AUDIT-LIST-10X.md`: reusable 10x checklist built from this site's OWN mistakes,
  not a generic list. 14 baked-in checks, each with past failure + new rule +
  measurement + pass/fail + proof required, plus audit order (build → serve fresh
  build → 3 measurement scripts → static HTML checks → view pixels → fix scoped →
  re-verify fresh → report). Standing exceptions are named in it so a later round
  cannot silently claim them fixed.
- **Correction owned in the document itself:** its first draft of check 2 wrongly
  claimed no `<img>` carries width/height attributes. The Round 8 checks script
  proved the opposite (see below); check 2 was corrected in the document before
  the audit report was written: attributes exist by design AND are safe only
  because `img{height:auto}` survives in the base rule plus explicit container
  heights with `object-fit:cover`.

### Audit results, check by check (all 14)
1. **200 is not proof:** static checks served `out/` on unique port 8955 with the
   homepage-title guard passing first; 27/27 pages HTTP 200 with a real H1, every
   `<img>` src resolving (0 missing), plus 54 real-browser full-page renders with
   0 broken images. PASS.
2. **Height + aspect:** all 78 `<img>` tags carry width/height attributes matching
   their boxes (hero 760×570, second 1100×420, cards 800×500); `height:auto`
   confirmed present in the base img rule; section run rendered heights match
   boxes (hero 372×279 desktop 4:3, cards 362×226 16:10, figures 440px desktop);
   0 zero-height renders. PASS (with the corrected rule, not the draft rule).
3. **Viewed pixels + hash + corners + logos:** all 78 images viewed on 4 fresh
   contact sheets (heroes, seconds, cards, areas). All 15 service cards and all
   service heroes/seconds clearly that exact service at first glance; AC card
   logo-free; Jackson hero clean, no MLS watermark; no visible watermarks or
   logos at sheet scale. No image files changed in Round 8, so Round 7's hash
   result stands: 78/78 unique, 0 collisions vs 31,620 other-site images.
   0 image replacements. City-photo honesty UNCHANGED: city heroes/seconds +
   area cards are representative Georgia town/suburban imagery, NOT verified
   photos of each exact town. Sheet-scale viewing cannot catch tiny corner text
   with certainty — stated as a limit; full-size corner verification for Jackson
   was done in Round 6 and no city file has changed since.
4. **No reuse:** all proof (54 full-page + 108 header shots, measurements,
   header-check, sections, checks-final) is from the final post-fix build;
   pre-fix checks output kept separately as `checks.json` and labelled pre-fix.
5. **Unique port + title guard:** QA port 8955, header port 8956, section port
   8957, checks port 8955 (sequential, never simultaneous); homepage guard
   ("McDonough Water Damage Restoration" + real H1) passed before measuring.
6. **Script crashes:** NONE in Round 8 — QA, header and section runs all exited 0
   with complete outputs (27 pages, 54 shots, 108 header shots, 936 sections).
   Nothing was reused from a partial run.
7. **Wrap experiments:** none run in Round 8 (no wrap/width/font change was made
   except the contact anchor fix, which cannot affect line breaks). Orphan
   baseline re-measured with the same QA script: desktop 1 (About H1) + mobile 26
   (long verbatim FAQ/city titles) — IDENTICAL to Rounds 5–7, not claimed fixed.
   H1 lines identical too (desktop 25×3 / 1×2 / 1×4; mobile 20×3 / 6×4 / 1×5).
8. **Lazy-load:** section run scrolls top → bottom → top before measuring; its
   img results agree with QA (0 incomplete after scroll). No image declared
   broken. PASS.
9. **Menu artifact:** mobile QA shots show the menu expanded because the script
   opens it to verify it — labelled here as a capture artifact, not the default
   state; menu open/close checks pass.
10. **Map tiles:** blank in the VM browser (known tunnel block, not a site
    defect). Checked instead: maps = 1 iframe per page on 27/27 pages with the
    correct place query + visible "Open <place> in Google Maps ↗" fallback link.
    Tile rendering in a real browser remains an open item.
11. **Sticky call bar:** hero call visible above the fold on 27/27 pages at 1366
    + 390 (desktop max About 802px; mobile max About 896px, next worst 804px).
    About mobile stays tight (same as Round 7 final); the sticky bar overlay
    limit stands as reported before.
12. **Verbatim / banned / self-links / markers / limits:** banned phrases 0,
    bracket markers 0, titles 0 over 60, metas 0 over 160 (decoded, worst meta
    158 chars) — EXCEPT one genuine defect found and fixed (below). Body
    self-links 0 on the final build.
13. **Scoped edits:** the one fix below touched exactly two lines in
    `components/PageRenderer.tsx` (form-card id + hero button href); placement
    verified in the built contact HTML (anchor + id both present) and by the
    re-run checks (self = []).
14. **Taps / header wrap / scroll-away / overflow:** header run 27/27 — overflow 0
    at 1366/1024/390/320, header-inner never overflows (no wrap at 1024),
    scroll header top = 0 with call-bar bottom < 0 on every page, call bar 78px
    desktop / pill 53px (21.6px), dropdown hover + Escape pass. QA overflow 0 at
    320/390/768/1024/1366. Small-text list identical to Rounds 5–7 intentional
    labels only (topbar cue/info 15.2px, eyebrow 15.2px, nav/toggles/menu 16.8px,
    brand subline 12.8px decorative, footer bottom 16px, map link + figcaptions
    16.8px). Body 21px desktop / 19px mobile unchanged.

### The ONE genuine defect found and fixed (check 12)
- **Contact page body self-link:** the hero "Request Help" button on
  `/contact-us/` linked to `/contact-us/` — the page linking to itself from its
  own body, against the standing rule (on every other page that button correctly
  leads to the contact page; on the contact page itself it just reloaded).
- **Fix (no word changes):** `components/PageRenderer.tsx` — the form card gained
  `id="contact-form"`, and the hero button href became conditional:
  `#contact-form` on the contact page only, `/contact-us/` everywhere else.
  Rebuilt, re-checked: contact page self-links [] (was [`/contact-us/`]),
  anchor + id both present in built HTML, and all three re-verification runs
  above are on this final build.
- **Pre-fix checks output preserved** as `screenshots/round8/checks.json`
  (self = [`/contact-us/`] on the contact page); final output is
  `screenshots/round8/checks-final.json` (self = [] everywhere).

### Per-section final (Round 8)
- 936 section measurements, overflow fails 0, bad images 0, heading colours ONLY
  navy rgb(11,47,74) (H1), aqua rgb(14,138,192) (H2), white (footer/CTA) — no
  clashes. The 108 "no heading" entries are lead/intro blocks, paragraph-led by
  design (same as Rounds 4–7), not defects. 156 image measurements (both
  viewports), all ok.
- Visual (viewed): Round 8 home 1366 header crop — byte-identical to the Round 7
  header crop (header untouched by the fix, as expected): call bar pops, gold
  border, brand shadow, H1 3 lines clean. Four image contact sheets viewed (above).

### Still needing the user's word (unchanged, nothing invented)
1. Domain for canonicals + sitemap. 2. Contact form delivery destination (form
   still honestly tells visitors to call). 3. Google Maps tiles check in the
   user's real browser. 4. Stock-only image licensing or 44px footer/prose
   links, if wanted. 5. Correction of the call-bar reading if he meant something
   else (Round 5 reading stands). 6. Provably town-specific city photos, if
   wanted (needs his own town photos or a licensed per-town search).
