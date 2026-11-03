import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Forest Park, GA 30297 24/7 Cleanup",
  description: "Old pipes burst, sewer backup or flooded business in Forest Park? Local water damage crews extract, disinfect and dry homes and properties across 30297, 24/7.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-forest-park-ga/" },
  openGraph: {
    title: "Water Damage Restoration Forest Park, GA 30297 24/7 Cleanup",
    description: "Old pipes burst, sewer backup or flooded business in Forest Park? Local water damage crews extract, disinfect and dry homes and properties across 30297, 24/7.",
    url: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-forest-park-ga/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-forest-park-ga-hero.jpg", alt: "Water damage restoration in Forest Park, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Water Damage Restoration Forest Park, GA 30297 24/7 Cleanup",
    description: "Old pipes burst, sewer backup or flooded business in Forest Park? Local water damage crews extract, disinfect and dry homes and properties across 30297, 24/7.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-water-damage-restoration-forest-park-ga-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-forest-park-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-forest-park-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Forest Park, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-forest-park-ga-second.jpg" || undefined}
      secondAlt={"Forest Park, GA home" || undefined}
      mapPlace={"Forest Park, GA"}
      mapTitle={"Map of Forest Park, GA"}
      eyebrow={"Forest Park, GA · Open 24 Hours"}
    />
  );
}
