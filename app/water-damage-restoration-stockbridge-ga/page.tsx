import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Stockbridge, GA 30281",
  description: "Burst pipe, ceiling leak or flooded floor in Stockbridge? Local water damage crews extract, dry and restore homes across 30281, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-stockbridge-ga/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-stockbridge-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-stockbridge-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Stockbridge, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-stockbridge-ga-second.jpg" || undefined}
      secondAlt={"Stockbridge, GA home exterior" || undefined}
      mapPlace={"Stockbridge, GA"}
      mapTitle={"Map of Stockbridge, GA"}
      eyebrow={"Stockbridge, GA · Open 24 Hours"}
    />
  );
}
