"use client";
import React from "react";
import Link from "next/link";
import { MapEmbed, PHONE, TEL } from "./Chrome";
import cardImages from "../data/card-images.json";

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
      const m = part.match(re);
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
                  {area && <div className="area-card-media"><img src={area.src} alt={area.alt} loading="lazy" width="800" height="500" /></div>}
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
              {card && <div className="svc-card-media"><img src={card.src} alt={card.alt} loading="lazy" width="800" height="500" /></div>}
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
          <figure className="figure"><img src={secondImg} alt={secondAlt || ""} loading="lazy" width="1100" height="420" /><figcaption>{secondAlt || ""}</figcaption></figure>
        </div></section>
      );
      secondInserted = true;
    }
  };
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
  const faqSchema = faqs.length ? {
    "@context": "https://schema.org", "@type": "FAQPage",
    mainEntity: faqs.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
  } : null;
  return (
    <>
      <section className="hero"><div className="hero-inner">
        <div>
          <p className="hero-eyebrow">{eyebrow}</p>
          <h1>{page.h1}</h1>
          {lead && <p className="lead">{lead}</p>}
          <div className="hero-actions">
            <a className="btn btn-call" href={TEL}>Call {PHONE}</a>
            <a className="btn btn-outline" href={page.slug === "/contact-us/" ? "#contact-form" : "/contact-us/"}>Request Help</a>
          </div>
          {trustChips.length > 0 && <div className="chips">{trustChips.map((c, i) => <span className="chip" key={i}>{c}</span>)}</div>}
        </div>
        {heroImg && <figure className="hero-img"><img src={heroImg} alt={heroAlt || ""} width="760" height="570" /><figcaption>{heroAlt || ""}</figcaption></figure>}
      </div></section>
      {sections}
      {!hasMapMarker && (
        <section className="section mist"><div className="section-inner">
          <h2>Service Area Map</h2>
          <MapEmbed place={mapPlace} title={mapTitle} />
        </div></section>
      )}
      {faqSchema && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />}
    </>
  );
}
