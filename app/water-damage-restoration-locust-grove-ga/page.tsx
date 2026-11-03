import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Locust Grove, GA 30248 24/7 Cleanup",
  description: "Water heater leak, slab leak or storm damage in Locust Grove? Local water damage crews extract, dry and restore homes across 30248, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-locust-grove-ga/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-locust-grove-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-locust-grove-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Locust Grove, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-locust-grove-ga-second.jpg" || undefined}
      secondAlt={"Locust Grove, GA home" || undefined}
      mapPlace={"Locust Grove, GA"}
      mapTitle={"Map of Locust Grove, GA"}
      eyebrow={"Locust Grove, GA · Open 24 Hours"}
    />
  );
}
