import PageRenderer from "../components/PageRenderer";
import pages from "../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "24/7 Water Damage Restoration in McDonough, GA",
  description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/" },
  openGraph: {
    title: "24/7 Water Damage Restoration in McDonough, GA",
    description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
    url: "https://mcdonoughwaterdamagerestoration.us/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-home-hero.jpg", alt: "Water damage restoration in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "24/7 Water Damage Restoration in McDonough, GA",
    description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-home-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/");
  // Round 9: the site's single org definition lives ONLY here (other pages reference
  // it by @id, never duplicate it). Facts are exactly the ones already on the site:
  // name, phone, 24-hour opening, McDonough ZIPs + Henry County, existing description.
  // No address, geo, logo, socials, ratings or prices — the site states none of those.
  const SITE_URL = "https://mcdonoughwaterdamagerestoration.us";
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "HomeAndConstructionBusiness",
        "@id": `${SITE_URL}/#organization`,
        name: "McDonough Water Damage Restoration",
        url: `${SITE_URL}/`,
        telephone: "+1-470-745-9798",
        openingHours: "Mo-Su 00:00-24:00",
        areaServed: { "@type": "AdministrativeArea", name: "McDonough, GA 30252 and 30253 and Henry County" },
        description: "24/7 water damage restoration for homes and businesses in McDonough and the south metro Atlanta area.",
      },
      {
        "@type": "WebSite",
        "@id": `${SITE_URL}/#website`,
        url: `${SITE_URL}/`,
        name: "McDonough Water Damage Restoration",
        publisher: { "@id": `${SITE_URL}/#organization` },
        inLanguage: "en",
      },
    ],
  };
  return (
    <>
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-home-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-home-second.jpg" || undefined}
      secondAlt={"Structural drying equipment in a McDonough home" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"Open 24 Hours · McDonough & Henry County"}
    />
    <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
    </>
  );
}
