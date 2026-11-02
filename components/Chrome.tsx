"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export const PHONE = "(470) 745-9798";
export const TEL = "tel:+14707459798";

const SERVICES: Array<[string, string]> = [
  ["Emergency Water Extraction", "/emergency-water-extraction/"],
  ["Burst & Frozen Pipes", "/burst-pipe-water-damage/"],
  ["Flood & Storm Cleanup", "/flood-damage-cleanup/"],
  ["Sewage Backup Cleanup", "/sewage-backup-cleanup/"],
  ["Ceiling & Roof Leaks", "/ceiling-leak-water-damage/"],
  ["Mold Remediation", "/mold-remediation/"],
  ["Structural Drying", "/structural-drying/"],
  ["Commercial Water Damage", "/commercial-water-damage/"],
  ["Crawl Space Water Damage", "/crawl-space-water-damage/"],
  ["Slab Leak Water Damage", "/slab-leak-water-damage/"],
  ["Water Heater Leaks", "/water-heater-leak-cleanup/"],
  ["Washer, Dishwasher & Fridge Leaks", "/appliance-leak-water-damage/"],
  ["AC & HVAC Leaks", "/ac-leak-water-damage/"],
  ["Hardwood Floor Drying", "/hardwood-floor-water-damage/"],
  ["Toilet Overflow & Bathroom Leaks", "/toilet-overflow-cleanup/"],
];
const AREAS: Array<[string, string]> = [
  ["Stockbridge, GA", "/water-damage-restoration-stockbridge-ga/"],
  ["Locust Grove, GA", "/water-damage-restoration-locust-grove-ga/"],
  ["Hampton, GA", "/water-damage-restoration-hampton-ga/"],
  ["Jonesboro, GA", "/water-damage-restoration-jonesboro-ga/"],
  ["Lovejoy, GA", "/water-damage-restoration-lovejoy-ga/"],
  ["Forest Park, GA", "/water-damage-restoration-forest-park-ga/"],
  ["Conyers, GA", "/water-damage-restoration-conyers-ga/"],
  ["Griffin, GA", "/water-damage-restoration-griffin-ga/"],
  ["Jackson, GA", "/water-damage-restoration-jackson-ga/"],
];

function Dropdown({ label, items, current }: { label: string; items: Array<[string, string]>; current: string }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const onDoc = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("mousedown", onDoc);
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("mousedown", onDoc); document.removeEventListener("keydown", onKey); };
  }, []);
  return (
    <div className="nav-item" ref={ref}
      onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}>
      <button type="button" className="nav-toggle" aria-expanded={open}
        onClick={() => setOpen((v) => !v)}>{label} ▾</button>
      {open && (
        <div className="dropdown" role="menu">
          {items.map(([name, href]) => href === current ? (
            <span key={href} style={{ display: "block", padding: ".6rem .75rem", fontWeight: 800, color: "#0E8AC0" }}>{name}</span>
          ) : (
            <Link key={href} href={href} onClick={() => setOpen(false)}>{name}</Link>
          ))}
        </div>
      )}
    </div>
  );
}

export function Header({ current: _current }: { current: string }) {
  const pathname = usePathname();
  const current = pathname ? (pathname.endsWith("/") ? pathname : `${pathname}/`) : "/";
  const [open, setOpen] = useState(false);
  return (
    <>
      <div className="topbar"><div className="topbar-inner">
        <span className="topbar-cue"><span className="topbar-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" /></svg></span>Call Now · Open 24 Hours</span>
        <a className="topbar-call" href={TEL}>{PHONE}</a>
        <span className="topbar-info">McDonough &amp; Henry County</span>
      </div></div>
      <header className="site-header">
      <div className="header-inner">
        <Link href="/" className="brand" aria-label="McDonough Water Damage Restoration home">
          <span className="brand-mark" aria-hidden="true">M</span>
          <span className="brand-text"><strong>McDonough Water Damage</strong><small>Restoration · 24/7</small></span>
        </Link>
        <nav className="main-nav" aria-label="Main">
          <Link href="/" className="nav-link">Home</Link>
          <Dropdown label="Services" items={SERVICES} current={current} />
          <Dropdown label="Service Areas" items={AREAS} current={current} />
          <Link href="/about-us/" className="nav-link">About</Link>
          <Link href="/contact-us/" className="nav-link">Contact</Link>
        </nav>
        <a className="header-call" href={TEL}>Call {PHONE}</a>
        <button type="button" className="menu-btn" aria-expanded={open} onClick={() => setOpen((v) => !v)}>Menu</button>
      </div>
      <div className={`mobile-nav${open ? " open" : ""}`}>
        <Link href="/" onClick={() => setOpen(false)}>Home</Link>
        <details><summary>Services</summary>{SERVICES.map(([n, h]) => <Link key={h} href={h} onClick={() => setOpen(false)}>{n}</Link>)}</details>
        <details><summary>Service Areas</summary>{AREAS.map(([n, h]) => <Link key={h} href={h} onClick={() => setOpen(false)}>{n}</Link>)}</details>
        <Link href="/about-us/" onClick={() => setOpen(false)}>About</Link>
        <Link href="/contact-us/" onClick={() => setOpen(false)}>Contact</Link>
        <Link href={TEL}>Call {PHONE}</Link>
      </div>
      </header>
    </>
  );
}

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div>
          <h3>About</h3>
          <p className="footer-brand"><span className="brand-mark" aria-hidden="true">M</span><strong style={{ color: "#fff" }}>McDonough Water Damage Restoration</strong></p>
          <p>24/7 water damage restoration for homes and businesses in McDonough and the south metro Atlanta area: water extraction, structural drying, sewage cleanup, mold remediation and repairs.</p>
          <p>Phone: <a className="footer-phone" href={TEL}>{PHONE}</a><br />Hours: Open 24 hours, 7 days a week<br />Service area: McDonough, GA 30252 &amp; 30253 and Henry County</p>
        </div>
        <div>
          <h3>Water Damage Services</h3>
          <ul>
            <li><Link href="/">Water Damage Restoration in McDonough</Link></li>
            {SERVICES.slice(0, 8).map(([n, h]) => <li key={h}><Link href={h}>{n}</Link></li>)}
          </ul>
        </div>
        <div>
          <h3>Hidden Leaks</h3>
          <ul>{SERVICES.slice(8).map(([n, h]) => <li key={h}><Link href={h}>{n}</Link></li>)}</ul>
        </div>
        <div>
          <h3>Service Areas</h3>
          <ul>{AREAS.map(([n, h]) => <li key={h}><Link href={h}>{n}</Link></li>)}</ul>
        </div>
      </div>
      <div className="footer-bottom">
        © 2026 McDonough Water Damage Restoration · <Link href="/about-us/">About</Link> · <Link href="/contact-us/">Contact</Link> · <Link href="/privacy-policy/">Privacy Policy</Link> · <Link href="/terms-of-use/">Terms</Link>
      </div>
      <a className="callbar" href={TEL}>📞 Call Now {PHONE}</a>
    </footer>
  );
}

export function MapEmbed({ place, title }: { place: string; title: string }) {
  const src = `https://www.google.com/maps?q=${encodeURIComponent(place)}&output=embed`;
  const openUrl = `https://www.google.com/maps?q=${encodeURIComponent(place)}`;
  return (
    <div>
      <div className="map-frame">
        <iframe title={title} src={src} loading="lazy" referrerPolicy="no-referrer-when-downgrade" allowFullScreen />
      </div>
      <p style={{ marginTop: ".7rem", fontSize: "1.05rem" }}>
        <a href={openUrl} target="_blank" rel="noreferrer">Open {place} in Google Maps ↗</a>
      </p>
    </div>
  );
}
