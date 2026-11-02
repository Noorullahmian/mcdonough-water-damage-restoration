#!/usr/bin/env python3
"""Parse doc-tabs.json with authoritative paragraph styles. Verbatim words only."""
import re, json, os
SRC = os.path.expanduser("~/workspace/new-doc-site/doc-tabs.json")
OUT = os.path.expanduser("~/workspace/mcdonough-water-damage/data/pages.json")
LOG = os.path.expanduser("~/workspace/mcdonough-water-damage/scripts/parse-log.txt")

def dedash(s):
    s = s.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
    s = s.replace("\u2014", ",").replace("\u2013", "-")
    return s

d = json.load(open(SRC))
SERVICE_NAMES = {
 "Emergency Water Extraction": "emergency-water-extraction",
 "Burst & Frozen Pipe Water Damage": "burst-pipe-water-damage",
 "Flood & Storm Damage Cleanup": "flood-damage-cleanup",
 "Sewage Backup Cleanup": "sewage-backup-cleanup",
 "Ceiling & Roof Leak Water Damage": "ceiling-leak-water-damage",
 "Structural Drying & Dehumidification": "structural-drying",
 "Mold Remediation": "mold-remediation",
 "Hardwood Floor Water Damage": "hardwood-floor-water-damage",
 "Crawl Space Water Damage": "crawl-space-water-damage",
 "Slab Leak Water Damage": "slab-leak-water-damage",
 "Water Heater Leak Cleanup": "water-heater-leak-cleanup",
 "Washing Machine, Dishwasher & Fridge Leaks": "appliance-leak-water-damage",
 "AC & HVAC Leak Water Damage": "ac-leak-water-damage",
 "Toilet Overflow & Bathroom Leaks": "toilet-overflow-cleanup",
 "Commercial Water Damage Restoration": "commercial-water-damage",
}
def is_step_heading(h):
    hl = h.lower()
    return any(k in hl for k in ["do these", "do this first", "first hour", "how a water damage job works",
                                 "what happens after you reach out", "while you wait"])

def para_text(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", [])).strip()

pages = []
for ti, tab in enumerate(d["tabs"], 1):
    if ti == 28:
        continue
    body = tab["documentTab"]["body"]["content"]
    slug = title = meta = h1 = None
    blocks = []
    last_h2 = ""
    in_faq = False
    step_mode = False
    pending_faq_q = None
    for el in body:
        if "table" in el:
            rows = []
            for r in el["table"].get("tableRows", []):
                cells = []
                for c in r.get("tableCells", []):
                    cells.append(" ".join(para_text(x["paragraph"]) for x in c.get("content", []) if "paragraph" in x).strip())
                rows.append([dedash(c) for c in cells])
            blocks.append({"type": "table", "rows": rows}); continue
        if "paragraph" not in el:
            continue
        p = el["paragraph"]
        style = p["paragraphStyle"].get("namedStyleType")
        txt = dedash(para_text(p))
        if not txt:
            continue
        if style == "HEADING_1":
            h1 = txt; continue
        if txt.startswith("URL:") and ti != 1:
            m = re.match(r"URL:\s*(/\S+/)\s*·\s*Title:\s*(.*?)\s*·\s*Meta:\s*(.*)$", txt)
            assert m, f"Tab {ti} setup: {txt[:200]}"
            slug, title, meta = m.group(1), m.group(2), m.group(3); continue
        if txt == "Call (470) 745-9798":
            blocks.append({"type": "cta"}); continue
        if txt == "[Form fields]":
            blocks.append({"type": "formstart"}); continue
        if txt.startswith("[Submit button:"):
            blocks.append({"type": "formsubmit", "submit": re.sub(r"^\[Submit button:\s*(.*?)\]$", r"\1", txt)}); continue
        if txt.startswith("[Embed Google Map"):
            blocks.append({"type": "mapmarker"}); continue
        if txt.startswith("["):
            continue
        if style == "HEADING_2":
            last_h2 = txt; in_faq = ("faq" in txt.lower()) or ("questions" in txt.lower())
            step_mode = False
            blocks.append({"type": "h2", "text": txt}); continue
        if style == "HEADING_3":
            if in_faq:
                pending_faq_q = txt; continue
            blocks.append({"type": "h3", "text": txt}); continue
        # NORMAL
        if pending_faq_q is not None:
            blocks.append({"type": "faq", "q": pending_faq_q, "a": txt}); pending_faq_q = None; continue
        if "bullet" in p:
            # service card?
            matched = None
            for name, sl in SERVICE_NAMES.items():
                if txt.startswith(name + ":"):
                    matched = (name, sl, txt[len(name)+1:].strip()); break
            if matched:
                blocks.append({"type": "servicecard", "name": matched[0], "slug": matched[1], "desc": matched[2]})
            elif step_mode or is_step_heading(last_h2):
                step_mode = True
                blocks.append({"type": "step", "text": txt})
            else:
                blocks.append({"type": "ulitem", "text": txt})
            continue
        # non-bullet paragraph: a step-heading parent with bullets handled above; plain p
        # Detect step-mode start for non-bullet? No: process paragraphs stay p.
        blocks.append({"type": "p", "text": txt})
    # post-process: merge ulitems, servicecards; form assembly
    merged = []
    for b in blocks:
        if b["type"] == "ulitem":
            if merged and merged[-1]["type"] == "ul":
                merged[-1]["items"].append(b["text"])
            else:
                merged.append({"type": "ul", "items": [b["text"]]})
        elif b["type"] == "servicecard":
            if merged and merged[-1]["type"] == "servicecards":
                merged[-1]["items"].append(b)
            else:
                merged.append({"type": "servicecards", "items": [b]})
        else:
            merged.append(b)
    # form assembly: formstart ... ulitems? Form fields in Doc are NORMAL non-bullet lines after [Form fields]
    # They were parsed as p blocks between formstart and formsubmit; convert them.
    final = []
    fi = 0
    while fi < len(merged):
        if merged[fi]["type"] == "formstart":
            fields = []
            fj = fi + 1
            submit = "Get Help Now"
            while fj < len(merged) and merged[fj]["type"] != "formsubmit":
                if merged[fj]["type"] == "p":
                    fields.append(merged[fj]["text"])
                elif merged[fj]["type"] == "ul":
                    fields.extend(merged[fj]["items"])
                fj += 1
            if fj < len(merged):
                submit = merged[fj]["submit"]; fj += 1
            final.append({"type": "form", "fields": fields, "submit": submit})
            fi = fj
        else:
            final.append(merged[fi]); fi += 1
    if ti == 1:
        slug = "/"
        title = h1 + " | McDonough Water Damage Restoration"
        meta = "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see, dry your home with commercial equipment and stop mold before it starts."
    pages.append({"tab": ti, "slug": slug, "title": title, "meta": meta, "h1": h1, "blocks": final})

json.dump(pages, open(OUT, "w"), indent=1, ensure_ascii=False)
log = []
for p in pages:
    kinds = {}
    for b in p["blocks"]:
        kinds[b["type"]] = kinds.get(b["type"], 0) + 1
    log.append(f"Tab {p['tab']} {p['slug']} H1={p['h1']} blocks={kinds}")
open(LOG, "w").write("\n".join(log) + f"\nTotal pages: {len(pages)}\n")
print(f"pages={len(pages)}")
for l in log: print(l)
