import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Hampton, GA 30228",
  description: "Storm damage, crawl space water or a burst pipe in Hampton? Local water damage crews extract, dry and restore homes across 30228, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-hampton-ga/" },
  openGraph: {
    title: "Water Damage Restoration Hampton, GA 30228",
    description: "Storm damage, crawl space water or a burst pipe in Hampton? Local water damage crews extract, dry and restore homes across 30228, 24/7. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-hampton-ga/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-hampton-ga-hero.jpg", alt: "Water damage restoration in Hampton, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Water Damage Restoration Hampton, GA 30228",
    description: "Storm damage, crawl space water or a burst pipe in Hampton? Local water damage crews extract, dry and restore homes across 30228, 24/7. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-hampton-ga-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-hampton-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-hampton-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Hampton, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-hampton-ga-second.jpg" || undefined}
      secondAlt={"Hampton, GA home" || undefined}
      mapPlace={"Hampton, GA"}
      mapTitle={"Map of Hampton, GA"}
      eyebrow={"Hampton, GA · Open 24 Hours"}
    />
  );
}
