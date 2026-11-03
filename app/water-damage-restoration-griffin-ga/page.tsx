import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Griffin, GA 30223",
  description: "Crawl space water, burst pipe or flooding in Griffin? Local water damage crews extract and dry older and newer homes across Spalding County, 24/7.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-griffin-ga/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-griffin-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-griffin-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Griffin, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-griffin-ga-second.jpg" || undefined}
      secondAlt={"Griffin, GA home" || undefined}
      mapPlace={"Griffin, GA"}
      mapTitle={"Map of Griffin, GA"}
      eyebrow={"Griffin, GA · Open 24 Hours"}
    />
  );
}
