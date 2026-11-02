#!/usr/bin/env python3
"""Parse ~/workspace/new-doc-site/extracted.txt into pages.json.
Rules: visible words verbatim; en dash between letters -> hyphen (month ranges);
spaced dashes -> comma; middot kept only in trust chips (handled in renderer);
bracket markers are instructions, never visible (form fields rendered as a form,
map marker rendered as a map, submit label as button label).
No invented words. Tables preserved. FAQ parsed only inside Questions sections.
"""
import re, json, os
SRC = os.path.expanduser("~/workspace/new-doc-site/extracted.txt")
OUT = os.path.expanduser("~/workspace/mcdonough-water-damage/data/pages.json")
LOG = os.path.expanduser("~/workspace/mcdonough-water-damage/scripts/parse-log.txt")

def dedash(s):
    s = s.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
    s = s.replace("\u2014", ",").replace("\u2013", "-")  # remaining en dashes are Dec-Feb style ranges
    return s

text = open(SRC, encoding="utf-8").read()
parts = re.split(r"===== TAB (\d+) =====", text)
tabs = {}
for i in range(1, len(parts), 2):
    tabs[int(parts[i])] = parts[i+1].strip()

SERVICE_MAP = [  # (phrase, slug) longest first
 ("washing machine, dishwasher & fridge leaks", "appliance-leak-water-damage"),
 ("washing machine and appliance leaks", "appliance-leak-water-damage"),
 ("washer, dishwasher & fridge leaks", "appliance-leak-water-damage"),
 ("emergency water extraction", "emergency-water-extraction"),
 ("burst & frozen pipe water damage", "burst-pipe-water-damage"),
 ("burst pipe water damage", "burst-pipe-water-damage"),
 ("flood & storm damage cleanup", "flood-damage-cleanup"),
 ("flood damage cleanup", "flood-damage-cleanup"),
 ("sewage backup cleanup", "sewage-backup-cleanup"),
 ("ceiling & roof leak water damage", "ceiling-leak-water-damage"),
 ("ceiling leak water damage", "ceiling-leak-water-damage"),
 ("structural drying", "structural-drying"),
 ("commercial water damage", "commercial-water-damage"),
 ("crawl space water damage", "crawl-space-water-damage"),
 ("slab leak water damage", "slab-leak-water-damage"),
 ("water heater leak cleanup", "water-heater-leak-cleanup"),
 ("water heater leaks", "water-heater-leak-cleanup"),
 ("ac & hvac leak water damage", "ac-leak-water-damage"),
 ("ac leak water damage", "ac-leak-water-damage"),
 ("hardwood floor water damage", "hardwood-floor-water-damage"),
 ("toilet overflow & bathroom leaks", "toilet-overflow-cleanup"),
 ("toilet overflow cleanup", "toilet-overflow-cleanup"),
 ("mold remediation", "mold-remediation"),
 ("water damage restoration in mcdonough", ""),
]
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
CITY_MAP = {
 "Stockbridge, GA": "water-damage-restoration-stockbridge-ga",
 "Locust Grove, GA": "water-damage-restoration-locust-grove-ga",
 "Hampton, GA": "water-damage-restoration-hampton-ga",
 "Jonesboro, GA": "water-damage-restoration-jonesboro-ga",
 "Lovejoy, GA": "water-damage-restoration-lovejoy-ga",
 "Forest Park, GA": "water-damage-restoration-forest-park-ga",
 "Conyers, GA": "water-damage-restoration-conyers-ga",
 "Griffin, GA": "water-damage-restoration-griffin-ga",
 "Jackson, GA": "water-damage-restoration-jackson-ga",
}

def is_call_line(l):
    return l.strip() == "Call (470) 745-9798"

def parse_tab(n, raw):
    lines = [dedash(l.rstrip()) for l in raw.split("\n")]
    # drop empty, keep order
    lines = [l for l in lines if l.strip()]
    slug = title = meta = None
    idx = 0
    if n == 1:
        slug = "/"
    else:
        m = re.match(r"URL:\s*(/\S+/)\s*·\s*Title:\s*(.*?)\s*·\s*Meta:\s*(.*)$", lines[0])
        assert m, f"Tab {n} setup line not parsed: {lines[0][:200]}"
        slug, title, meta = m.group(1), m.group(2), m.group(3)
        idx = 1
    h1 = lines[idx]; idx += 1
    if n == 1:
        title = h1 + " | McDonough Water Damage Restoration"
        meta = lines[idx+1] if False else "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see, dry your home with commercial equipment and stop mold before it starts."
    blocks = []
    i = idx
    in_faq = False
    # step-section detection
    def is_step_heading(h):
        hl = h.lower()
        return any(k in hl for k in ["do these", "do this first", "first hour", "how a water damage job works",
                                     "how emergency water extraction works", "how restoration works",
                                     "what happens after you reach out", "while you wait"])
    step_mode = False
    while i < len(lines):
        l = lines[i]
        # bracket markers
        if l == "[Form fields]":
            # following lines until [Submit button...] are field labels
            fields = []
            j = i + 1
            submit = "Get Help Now"
            while j < len(lines) and not lines[j].startswith("[Submit button:"):
                fields.append(lines[j]); j += 1
            if j < len(lines):
                submit = re.sub(r"^\[Submit button:\s*(.*?)\]$", r"\1", lines[j]); j += 1
            blocks.append({"type": "form", "fields": fields, "submit": submit})
            i = j; continue
        if l.startswith("[Embed Google Map"):
            blocks.append({"type": "mapmarker"}); i += 1; continue
        if l.startswith("["):
            i += 1; continue
        if is_call_line(l):
            blocks.append({"type": "cta"}); i += 1; continue
        # table: consecutive | lines
        if " | " in l:
            rows = []
            while i < len(lines) and " | " in lines[i]:
                rows.append([c.strip() for c in lines[i].split(" | ")]); i += 1
            blocks.append({"type": "table", "rows": rows}); continue
        # FAQ handling
        if in_faq and l.endswith("?") and len(l) < 160:
            # look ahead: answer paragraph, then either another ? or end/CTA
            ans = lines[i+1] if i+1 < len(lines) else ""
            # final CTA check: after answer comes Call line and end of tab
            if i+2 < len(lines) and is_call_line(lines[i+2]) and i+3 >= len(lines):
                in_faq = False; step_mode = False
                blocks.append({"type": "h2", "text": l}); i += 1; continue
            blocks.append({"type": "faq", "q": l, "a": ans})
            i += 2; continue
        # consecutive short lines -> list (3+ in a row, each <120 chars, no trailing period, not call)
        run = []
        j = i
        while j < len(lines) and len(lines[j]) < 130 and not lines[j].endswith(".") and not lines[j].endswith("?") \
                and " | " not in lines[j] and not is_call_line(lines[j]) and not lines[j].startswith("["):
            run.append(lines[j]); j += 1
        if len(run) >= 3:
            # if first of run is a heading followed by list items? No: run itself is the list.
            blocks.append({"type": "ul", "items": run}); i = j; continue
        # single short line followed by a paragraph/list/table -> heading
        if len(l) < 130 and not l.endswith(".") and i+1 < len(lines):
            nxt = lines[i+1]
            if len(nxt) >= 40 or " | " in nxt or len(nxt) < 130:
                # group label if next is a service-card line or list run
                if nxt.startswith(tuple(SERVICE_NAMES.keys())) or (len(nxt) < 130 and not nxt.endswith(".")):
                    blocks.append({"type": "h3", "text": l})
                else:
                    blocks.append({"type": "h2", "text": l})
                if "question" in l.lower() or l.lower().endswith("faq"):
                    in_faq = True
                else:
                    in_faq = False
                step_mode = is_step_heading(l)
                i += 1; continue
        # service-card line: Name: description, name in SERVICE_NAMES
        matched = None
        for name, sl in SERVICE_NAMES.items():
            if l.startswith(name + ":"):
                matched = (name, sl, l[len(name)+1:].strip()); break
        if matched:
            blocks.append({"type": "servicecard", "name": matched[0], "slug": matched[1], "desc": matched[2]})
            i += 1; continue
        # plain paragraph (or step paragraph)
        if step_mode:
            blocks.append({"type": "step", "text": l})
        else:
            blocks.append({"type": "p", "text": l})
        i += 1
    # merge consecutive servicecards into a group for rendering
    merged = []
    for b in blocks:
        if b["type"] == "servicecard" and merged and merged[-1]["type"] == "servicecards":
            merged[-1]["items"].append(b)
        elif b["type"] == "servicecard":
            merged.append({"type": "servicecards", "items": [b]})
        else:
            merged.append(b)
    return {"tab": n, "slug": slug, "title": title, "meta": meta, "h1": h1, "blocks": merged}

pages = []
for n in range(1, 28):
    if n == 28:
        continue
    pages.append(parse_tab(n, tabs[n]))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(pages, open(OUT, "w"), indent=1, ensure_ascii=False)
# verbatim report: word counts + block counts
log = []
for p in pages:
    src_words = len(re.findall(r"\S+", tabs[p["tab"]]))
    out_words = len(re.findall(r"\S+", json.dumps(p, ensure_ascii=False)))
    kinds = {}
    for b in p["blocks"]:
        kinds[b["type"]] = kinds.get(b["type"], 0) + 1
    log.append(f"Tab {p['tab']} {p['slug']} H1={p['h1'][:80]} blocks={kinds}")
open(LOG, "w").write("\n".join(log) + f"\nTotal pages: {len(pages)}\n")
print(f"pages={len(pages)}")
for l in log: print(l)
