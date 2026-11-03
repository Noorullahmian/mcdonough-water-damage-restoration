"use client";
import React from "react";
import Link from "next/link";
import { MapEmbed, PHONE, TEL } from "./Chrome";
import cardImages from "../data/card-images.json";

// GitHub Pages project sites live under a subpath (e.g. /mcdonough-water-damage-restoration).
// Build with NEXT_PUBLIC_BASE_PATH set to that subpath and plain <img> srcs get the same
// prefix here (next/link already prefixes navigation automatically). Root deploys build
// without the env var and this prefix is empty, so the same code serves both.
const BP = process.env.NEXT_PUBLIC_BASE_PATH || "";
const imgSrc = (s?: string) => (s && s.startsWith("/") ? BP + s : s);

// Live site base (real domain, live on Vercel). Used ONLY as
// schema @id/url identifiers; if a real domain is ever confirmed, repoint this one const.
const SITE_URL = "https://mcdonoughwaterdamagerestoration.us";
const ORG_ID = `${SITE_URL}/#organization`;
const SITE_ID = `${SITE_URL}/#website`;
// Service display names, copied verbatim from the homepage's own service cards.
const SERVICE_NAMES: Record<string, string> = {
  "emergency-water-extraction": "Emergency Water Extraction",
  "burst-pipe-water-damage": "Burst & Frozen Pipe Water Damage",
  "flood-damage-cleanup": "Flood & Storm Damage Cleanup",
  "sewage-backup-cleanup": "Sewage Backup Cleanup",
  "ceiling-leak-water-damage": "Ceiling & Roof Leak Water Damage",
  "structural-drying": "Structural Drying & Dehumidification",
  "mold-remediation": "Mold Remediation",
  "hardwood-floor-water-damage": "Hardwood Floor Water Damage",
  "crawl-space-water-damage": "Crawl Space Water Damage",
  "slab-leak-water-damage": "Slab Leak Water Damage",
  "water-heater-leak-cleanup": "Water Heater Leak Cleanup",
  "appliance-leak-water-damage": "Washing Machine, Dishwasher & Fridge Leaks",
  "ac-leak-water-damage": "AC & HVAC Leak Water Damage",
  "toilet-overflow-cleanup": "Toilet Overflow & Bathroom Leaks",
  "commercial-water-damage": "Commercial Water Damage Restoration",
};

export type Block =
  | { type: "p"; text: string }
  | { type: "step"; text: string }
  | { type: "h2"; text: string }
  | { type: "h3"; text: string }
  | { type: "cta" }
  | { type: "ul"; items: string[] }
  | { type: "table"; rows: string[][] }
  | { type: "faq"; q: string; a: string }
  | { type: "servicecards"; items: Array<{ name: string; slug: string; desc: string }> }
  | { type: "form"; fields: string[]; submit: string }
  | { type: "mapmarker" };

export type PageData = {
  tab: number; slug: string; title: string; meta: string; h1: string; blocks: Block[];
};

const LINK_PHRASES: Array<[RegExp, string]> = [
  [/washing machine, dishwasher & fridge leaks/gi, "/appliance-leak-water-damage/"],
  [/washing machine and appliance leaks/gi, "/appliance-leak-water-damage/"],
  [/washer, dishwasher & fridge leaks/gi, "/appliance-leak-water-damage/"],
  [/emergency water extraction/gi, "/emergency-water-extraction/"],
  [/burst & frozen pipe water damage/gi, "/burst-pipe-water-damage/"],
  [/burst pipe water damage/gi, "/burst-pipe-water-damage/"],
  [/flood & storm damage cleanup/gi, "/flood-damage-cleanup/"],
  [/flood damage cleanup/gi, "/flood-damage-cleanup/"],
  [/sewage backup cleanup/gi, "/sewage-backup-cleanup/"],
  [/ceiling & roof leak water damage/gi, "/ceiling-leak-water-damage/"],
  [/ceiling leak water damage/gi, "/ceiling-leak-water-damage/"],
  [/structural drying/gi, "/structural-drying/"],
  [/commercial water damage/gi, "/commercial-water-damage/"],
  [/crawl space water damage/gi, "/crawl-space-water-damage/"],
  [/slab leak water damage/gi, "/slab-leak-water-damage/"],
  [/water heater leak cleanup/gi, "/water-heater-leak-cleanup/"],
  [/ac & hvac leak water damage/gi, "/ac-leak-water-damage/"],
  [/ac leak water damage/gi, "/ac-leak-water-damage/"],
  [/hardwood floor water damage/gi, "/hardwood-floor-water-damage/"],
  [/toilet overflow & bathroom leaks/gi, "/toilet-overflow-cleanup/"],
  [/toilet overflow cleanup/gi, "/toilet-overflow-cleanup/"],
  [/mold remediation/gi, "/mold-remediation/"],
  [/water damage restoration in mcdonough/gi, "/"],
];
const CITY_LINKS: Array<[string, string]> = [
  ["Stockbridge", "/water-damage-restoration-stockbridge-ga/"],
  ["Locust Grove", "/water-damage-restoration-locust-grove-ga/"],
  ["Hampton", "/water-damage-restoration-hampton-ga/"],
  ["Jonesboro", "/water-damage-restoration-jonesboro-ga/"],
  ["Lovejoy", "/water-damage-restoration-lovejoy-ga/"],
  ["Forest Park", "/water-damage-restoration-forest-park-ga/"],
  ["Conyers", "/water-damage-restoration-conyers-ga/"],
  ["Griffin", "/water-damage-restoration-griffin-ga/"],
  ["Jackson", "/water-damage-restoration-jackson-ga/"],
];

function linkify(text: string, self: string, used: Set<string>, keyPrefix: string): React.ReactNode {
  // Split on link phrases, first occurrence per target per page only.
  let parts: React.ReactNode[] = [text];
  for (const [re, href] of LINK_PHRASES) {
    if (href === self || used.has(href)) continue;
    const next: React.ReactNode[] = [];
    let linked = false;
    parts.forEach((part, pi) => {
      if (typeof part !== "string" || linked) { next.push(part); return; }
      // Round 9 fix: part.match() with a /g/ regex returns no .index, so the old code
      // took the no-match branch every time and this function linked NOTHING sitewide
      // (Round 8's "self-links []" was vacuous). A non-global exec returns the index.
      const m = new RegExp(re.source, "i").exec(part);
      if (!m || m.index === undefined) { next.push(part); return; }
      linked = true; used.add(href);
      const before = part.slice(0, m.index);
      const after = part.slice(m.index + m[0].length);
      if (before) next.push(before);
      next.push(<Link key={`${keyPrefix}-${href}-${pi}`} href={href}>{m[0]}</Link>);
      if (after) next.push(after);
    });
    parts = next;
  }
  return <>{parts.map((p, i) => <React.Fragment key={i}>{p}</React.Fragment>)}</>;
}

function cityLink(name: string, self: string): React.ReactNode {
  const hit = CITY_LINKS.find(([n]) => name.startsWith(n));
  if (!hit || hit[1] === self) return name;
  return <Link href={hit[1]}>{name}</Link>;
}

function leadBold(text: string): React.ReactNode {
  const idx = text.indexOf(". ");
  if (idx > 0 && idx < 60) {
    return <><strong>{text.slice(0, idx + 1)}</strong>{text.slice(idx + 1)}</>;
  }
  return text;
}

export function ContactForm({ fields, submit }: { fields: string[]; submit: string }) {
  const [sent, setSent] = React.useState(false);
  return (
    <div className="form-card" id="contact-form">
      {sent ? (
        <div>
          <p><strong>Thank you. For an active leak or sewage, please call right away — calling is always faster.</strong></p>
          <p><a className="btn btn-call" href={TEL}>Call {PHONE}</a></p>
          <p className="form-note">Online requests are not yet connected to a delivery address. Until the site owner connects one, calling is the confirmed way to reach a crew.</p>
        </div>
      ) : (
        <form onSubmit={(e) => { e.preventDefault(); setSent(true); }}>
          {fields.map((f, i) => (
            <label key={i}>{f}
              {f.toLowerCase().includes("anything else") || f.toLowerCase().includes("what happened")
                ? <textarea rows={4} name={`field-${i}`} />
                : f.toLowerCase().includes("still coming")
                  ? <select name={`field-${i}`}><option>Yes</option><option>No</option><option>Not sure</option></select>
                  : f.toLowerCase().includes("home or business")
                    ? <select name={`field-${i}`}><option>Home</option><option>Business</option></select>
                    : <input name={`field-${i}`} type={f.toLowerCase().includes("phone") ? "tel" : "text"} />}
            </label>
          ))}
          <button type="submit">{submit}</button>
          <p className="form-note">For active leaks or sewage, calling is always faster: <a href={TEL}>{PHONE}</a></p>
        </form>
      )}
    </div>
  );
}

export default function PageRenderer({ page, heroImg, heroAlt, secondImg, secondAlt, mapPlace, mapTitle, eyebrow }: {
  page: PageData; heroImg?: string; heroAlt?: string; secondImg?: string; secondAlt?: string; mapPlace: string; mapTitle: string; eyebrow: string;
}) {
  const used = new Set<string>();
  const self = page.slug;
  const blocks = page.blocks;
  const leadIdx = blocks.findIndex((b) => b.type === "p");
  const lead = leadIdx >= 0 ? (blocks[leadIdx] as { text: string }).text : "";
  const trustIdx = blocks.findIndex((b, i) => i <= 3 && b.type === "p" && b.text.startsWith("Open 24 hours"));
  const trust = trustIdx >= 0 ? (blocks[trustIdx] as { text: string }).text : "";
  const trustChips = trust ? trust.split("·").map((s) => s.trim()).filter(Boolean) : [];
  const rest = blocks.filter((_, i) => i !== leadIdx && i !== trustIdx);
  const faqs = page.blocks.filter((b): b is { type: "faq"; q: string; a: string } => b.type === "faq");
  const hasMapMarker = blocks.some((b) => b.type === "mapmarker");
  let sectionCount = 0;
  let secondInserted = false;
  const renderBlock = (b: Block, i: number): React.ReactNode => {
    switch (b.type) {
      case "p": return <p key={i}>{linkify(b.text, self, used, `p${i}`)}</p>;
      case "step": return null; // handled in step groups below
      case "h2": return <h2 key={i}>{b.text}</h2>;
      case "h3": return <h3 key={i}>{b.text}</h3>;
      case "cta": return <p key={i}><a className="btn btn-call" href={TEL}>Call {PHONE}</a></p>;
      case "ul": {
        // Homepage "Areas We Serve" list (all items are city names) renders as image cards, not a plain list.
        const cityItems = b.items.map((it) => CITY_LINKS.find(([n]) => it === `${n}, GA`));
        if (cityItems.length > 1 && cityItems.every(Boolean)) {
          return (
            <div className="area-grid" key={i}>{cityItems.map((city, j) => {
              const href = city![1];
              const citySlug = href.replace("/water-damage-restoration-", "").replace(/\//g, "");
              const area = (cardImages as Record<string, { src: string; alt: string }>)[`area:${citySlug}`];
              const label = b.items[j];
              return (
                <article className="area-card" key={j}>
                  {area && <div className="area-card-media"><img src={imgSrc(area.src)} alt={area.alt} loading="lazy" width="800" height="500" /></div>}
                  <div className="area-card-body">
                    {href === self ? <span style={{ fontWeight: 800, color: "#0B2F4A" }}>{label}</span> : <Link href={href}>{label}</Link>}
                  </div>
                </article>
              );
            })}</div>
          );
        }
        return (
          <ul key={i}>{b.items.map((it, j) => {
            const city = CITY_LINKS.find(([n]) => it === `${n}, GA`);
            if (city && city[1] !== self) return <li key={j}><Link href={city[1]}>{it}</Link></li>;
            return <li key={j}>{linkify(it, self, used, `ul${i}-${j}`)}</li>;
          })}</ul>
        );
      }
      case "table": {
        const [head, ...rows] = b.rows;
        return (
          <div className="table-wrap" key={i}><table>
            <thead><tr>{head.map((c, j) => <th key={j}>{c}</th>)}</tr></thead>
            <tbody>{rows.map((r, ri) => (
              <tr key={ri}>{r.map((c, ci) => <td key={ci} data-label={head[ci] || ""}>{c}</td>)}</tr>
            ))}</tbody>
          </table></div>
        );
      }
      case "faq": return null;
      case "servicecards": return (
        <div className="svc-grid" key={i}>{b.items.map((it, j) => {
          const card = (cardImages as Record<string, { src: string; alt: string }>)[`card:${it.slug}`];
          return (
            <article className="svc-card" key={j}>
              {card && <div className="svc-card-media"><img src={imgSrc(card.src)} alt={card.alt} loading="lazy" width="800" height="500" /></div>}
              <div className="svc-card-body">
                {it.slug === self.replace(/\/$/, "/") || `/${it.slug}/` === self
                  ? <span style={{ fontWeight: 800, color: "#0B2F4A", fontSize: "1.12rem" }}>{it.name}:</span>
                  : <Link href={`/${it.slug}/`}>{it.name}:</Link>}
                <p>{it.desc}</p>
              </div>
            </article>
          );
        })}</div>
      );
      case "form": return <ContactForm key={i} fields={b.fields} submit={b.submit} />;
      case "mapmarker": return <div key={i}><MapEmbed place={mapPlace} title={mapTitle} /></div>;
      default: return null;
    }
  };
  // Group consecutive steps and faqs for section rendering
  const groups: Array<{ kind: "blocks"; items: Array<[Block, number]> } | { kind: "steps"; items: string[] } | { kind: "faqs"; items: Array<{ q: string; a: string }> }> = [];
  let cur: Array<[Block, number]> = [];
  const flush = () => { if (cur.length) { groups.push({ kind: "blocks", items: cur }); cur = []; } };
  rest.forEach((b, ri) => {
    if (b.type === "step") {
      flush();
      const last = groups[groups.length - 1];
      if (last && last.kind === "steps") last.items.push(b.text);
      else groups.push({ kind: "steps", items: [b.text] });
    } else if (b.type === "faq") {
      flush();
      const last = groups[groups.length - 1];
      if (last && last.kind === "faqs") last.items.push(b);
      else groups.push({ kind: "faqs", items: [b] });
    } else {
      if (b.type === "h2" || b.type === "h3") {
        // steps/faq groups already flushed by their own handling; keep blocks flowing
      }
      cur.push([b, ri]);
    }
  });
  flush();
  // Render: split into sections at each h2 inside block groups
  const sections: React.ReactNode[] = [];
  let secBlocks: React.ReactNode[] = [];
  let secKey = 0;
  const pushSection = () => {
    if (!secBlocks.length) return;
    const cls = sectionCount % 2 === 0 ? "section" : "section mist";
    sections.push(<section className={cls} key={secKey++}><div className="section-inner">{secBlocks}</div></section>);
    sectionCount += 1; secBlocks = [];
    if (!secondInserted && secondImg) {
      sections.push(
        <section className="section" key={secKey++}><div className="section-inner">
          <figure className="figure"><img src={imgSrc(secondImg)} alt={secondAlt || ""} loading="lazy" width="1100" height="420" /><figcaption>{secondAlt || ""}</figcaption></figure>
        </div></section>
      );
      secondInserted = true;
    }
  };
  // User order (live review, 2026-11-03): the extra Call button that sat right after the hero
  // (the cta block at index 1 on every page) must sit BELOW the intro paragraphs, not above
  // them. So in the FIRST blocks group, cta blocks move to just BEFORE the first h2/h3 in
  // that group (after the intro paragraphs) — NOT to the end of the group, because a blocks
  // group keeps flowing past its first h2, and end-of-group would drop the button into the
  // next section (measured wrong on the first attempt: button landed in the steps section).
  // No words change, no other cta (e.g. the closing one at the end of each page) moves.
  {
    const first = groups.find((g) => g.kind === "blocks");
    if (first && first.kind === "blocks") {
      const h2Idx = first.items.findIndex(([b]) => b.type === "h2" || b.type === "h3");
      const end = h2Idx >= 0 ? h2Idx : first.items.length;
      const head = first.items.slice(0, end);
      const ctas = head.filter(([b]) => b.type === "cta");
      if (ctas.length) first.items = [...head.filter(([b]) => b.type !== "cta"), ...ctas, ...first.items.slice(end)];
    }
  }
  groups.forEach((g) => {
    if (g.kind === "steps") {
      secBlocks.push(<ol className="steps" key={`steps-${secKey}-${secBlocks.length}`}>{g.items.map((s, j) => <li key={j}>{leadBold(s)}</li>)}</ol>);
    } else if (g.kind === "faqs") {
      secBlocks.push(<div key={`faq-${secKey}-${secBlocks.length}`}>{g.items.map((f, j) => (
        <details className="faq-item" key={j}><summary>{f.q}</summary><p>{linkify(f.a, self, used, `faq${j}`)}</p></details>
      ))}</div>);
    } else {
      g.items.forEach(([b, ri]) => {
        if (b.type === "h2" && secBlocks.length) pushSection();
        const node = renderBlock(b, ri);
        if (node) secBlocks.push(node);
      });
    }
  });
  pushSection();
  // ---- Round 9 schema: one @graph per page. WebPage + BreadcrumbList on every page;
  // Service on service pages (that service) and city pages (water damage restoration in
  // that city, with a catalog of ONLY the services this page's own text actually links);
  // homepage Service with a catalog of its own service-card menu (15 services, deduped);
  // FAQPage exactly equal to the visible FAQs (same blocks, same text). The org node
  // itself lives ONLY on the homepage (app/page.tsx, @id ORG_ID); here it is referenced,
  // never duplicated. No ratings, prices, certifications, address, geo, logo or socials
  // anywhere — nothing the site itself does not state.
  const pageUrl = `${SITE_URL}${self}`;
  const shortName = page.title.split(" | ")[0];
  const crumbs: Array<Record<string, unknown>> = [
    { "@type": "ListItem", position: 1, name: "Home", item: `${SITE_URL}/` },
  ];
  if (self !== "/") crumbs.push({ "@type": "ListItem", position: 2, name: shortName, item: pageUrl });
  const areaHome: Array<Record<string, string>> = [
    { "@type": "City", name: "McDonough, GA" },
    { "@type": "AdministrativeArea", name: "Henry County, GA" },
  ];
  const graph: Array<Record<string, unknown>> = [
    {
      "@type": "WebPage", "@id": `${pageUrl}#webpage`, url: pageUrl, name: page.title,
      isPartOf: { "@id": SITE_ID }, about: { "@id": ORG_ID },
      breadcrumb: { "@id": `${pageUrl}#breadcrumb` }, inLanguage: "en",
    },
    { "@type": "BreadcrumbList", "@id": `${pageUrl}#breadcrumb`, itemListElement: crumbs },
  ];
  const slugKey = self.replace(/\//g, "");
  const cityHit = CITY_LINKS.find(([, href]) => href === self);
  if (self === "/") {
    const seen = new Set<string>();
    const catalog: Array<Record<string, unknown>> = [];
    page.blocks.forEach((b) => {
      if (b.type !== "servicecards") return;
      b.items.forEach((it) => {
        if (seen.has(it.slug)) return;
        seen.add(it.slug);
        catalog.push({
          "@type": "Offer", itemOffered: {
            "@type": "Service", name: it.name, url: `${SITE_URL}/${it.slug}/`,
            provider: { "@id": ORG_ID }, areaServed: areaHome,
          },
        });
      });
    });
    graph.push({
      "@type": "Service", "@id": `${pageUrl}#service`, name: "Water Damage Restoration",
      description: page.meta, provider: { "@id": ORG_ID }, areaServed: areaHome,
      hasOfferCatalog: {
        "@type": "OfferCatalog", name: "Water Damage Restoration Services",
        itemListElement: catalog,
      },
    });
  } else if (SERVICE_NAMES[slugKey]) {
    graph.push({
      "@type": "Service", "@id": `${pageUrl}#service`, name: SERVICE_NAMES[slugKey],
      description: page.meta, provider: { "@id": ORG_ID }, areaServed: areaHome,
    });
  } else if (cityHit) {
    const cityName = `${cityHit[0]}, GA`;
    const linked: Array<Record<string, unknown>> = [...used]
      .filter((h) => { const k = h.replace(/\//g, ""); return !!SERVICE_NAMES[k]; })
      .map((h) => {
        const k = h.replace(/\//g, "");
        return {
          "@type": "Offer", itemOffered: {
            "@type": "Service", name: SERVICE_NAMES[k], url: `${SITE_URL}/${k}/`,
            provider: { "@id": ORG_ID }, areaServed: [{ "@type": "City", name: cityName }],
          },
        };
      });
    const cityService: Record<string, unknown> = {
      "@type": "Service", "@id": `${pageUrl}#service`,
      name: `Water Damage Restoration in ${cityName}`,
      description: page.meta, provider: { "@id": ORG_ID },
      areaServed: [{ "@type": "City", name: cityName }],
    };
    if (linked.length) {
      cityService.hasOfferCatalog = {
        "@type": "OfferCatalog", name: `Water Damage Restoration Services in ${cityName}`,
        itemListElement: linked,
      };
    }
    graph.push(cityService);
  }
  const faqSchema = faqs.length ? {
    "@type": "FAQPage",
    mainEntity: faqs.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
  } : null;
  if (faqSchema) graph.push(faqSchema);
  const pageSchema = { "@context": "https://schema.org", "@graph": graph };
  return (
    <>
      <section className="hero"><div className="hero-inner">
        <div>
          <p className="hero-eyebrow">{eyebrow}</p>
          <h1>{page.h1}</h1>
          {lead && <p className="lead">{lead}</p>}
          <div className="hero-actions">
            <a className="btn btn-call" href={TEL}>Call {PHONE}</a>
            <Link className="btn btn-outline" href={page.slug === "/contact-us/" ? "#contact-form" : "/contact-us/"}>Request Help</Link>
          </div>
          {trustChips.length > 0 && <div className="chips">{trustChips.map((c, i) => <span className="chip" key={i}>{c}</span>)}</div>}
        </div>
        {heroImg && <figure className="hero-img"><img src={imgSrc(heroImg)} alt={heroAlt || ""} width="760" height="570" /><figcaption>{heroAlt || ""}</figcaption></figure>}
      </div></section>
      {sections}
      {!hasMapMarker && (
        <section className="section mist"><div className="section-inner">
          <h2>Service Area Map</h2>
          <MapEmbed place={mapPlace} title={mapTitle} />
        </div></section>
      )}
      {pageSchema && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(pageSchema) }} />}
    </>
  );
}
