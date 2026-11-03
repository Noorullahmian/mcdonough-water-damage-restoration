import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Conyers, GA 30094",
  description: "Flooding, crawl space water or a burst pipe in Conyers? Local water damage crews extract, disinfect and dry homes across Rockdale County, 24/7.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-conyers-ga/" },
  openGraph: {
    title: "Water Damage Restoration Conyers, GA 30094",
    description: "Flooding, crawl space water or a burst pipe in Conyers? Local water damage crews extract, disinfect and dry homes across Rockdale County, 24/7.",
    url: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-conyers-ga/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-conyers-ga-hero.jpg", alt: "Water damage restoration in Conyers, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Water Damage Restoration Conyers, GA 30094",
    description: "Flooding, crawl space water or a burst pipe in Conyers? Local water damage crews extract, disinfect and dry homes across Rockdale County, 24/7.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-conyers-ga-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-conyers-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-conyers-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Conyers, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-conyers-ga-second.jpg" || undefined}
      secondAlt={"Conyers, GA home" || undefined}
      mapPlace={"Conyers, GA"}
      mapTitle={"Map of Conyers, GA"}
      eyebrow={"Conyers, GA · Open 24 Hours"}
    />
  );
}
