import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Crawl Space Water Removal McDonough, GA | Crawl Space Drying",
  description: "Standing water or a musty, wet crawl space under your McDonough home? We pump it out, dry it and stop the moisture. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/crawl-space-water-damage/" },
  openGraph: {
    title: "Crawl Space Water Removal McDonough, GA | Crawl Space Drying",
    description: "Standing water or a musty, wet crawl space under your McDonough home? We pump it out, dry it and stop the moisture. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/crawl-space-water-damage/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-crawl-space-water-damage-hero.jpg", alt: "Crawl space water damage in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Crawl Space Water Removal McDonough, GA | Crawl Space Drying",
    description: "Standing water or a musty, wet crawl space under your McDonough home? We pump it out, dry it and stop the moisture. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-crawl-space-water-damage-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/crawl-space-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-crawl-space-water-damage-hero.jpg" || undefined}
      heroAlt={"Crawl space water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-crawl-space-water-damage-second.jpg" || undefined}
      secondAlt={"Crawl space drying in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
