import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Jackson, GA 30233",
  description: "Septic backup, lake house leak or storm damage in Jackson? Local water damage crews extract, disinfect and dry homes across Butts County, 24/7.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-jackson-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-jackson-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Jackson, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-jackson-ga-second.jpg" || undefined}
      secondAlt={"Jackson, GA home" || undefined}
      mapPlace={"Jackson, GA"}
      mapTitle={"Map of Jackson, GA"}
      eyebrow={"Jackson, GA · Open 24 Hours"}
    />
  );
}
