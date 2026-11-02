import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Jonesboro, GA 30238",
  description: "Sewer backup, burst pipe or flooded floors in Jonesboro? Local water damage crews extract, disinfect and dry homes across 30238 and 30236, 24/7.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-jonesboro-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-jonesboro-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Jonesboro, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-jonesboro-ga-second.jpg" || undefined}
      secondAlt={"Jonesboro, GA home" || undefined}
      mapPlace={"Jonesboro, GA"}
      mapTitle={"Map of Jonesboro, GA"}
      eyebrow={"Jonesboro, GA · Open 24 Hours"}
    />
  );
}
