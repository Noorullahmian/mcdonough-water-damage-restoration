import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Restoration Lovejoy, GA 30250",
  description: "Hidden leak, washer overflow or flooding in Lovejoy? Local water damage crews extract, dry and restore homes across 30250, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/water-damage-restoration-lovejoy-ga/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-damage-restoration-lovejoy-ga/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-damage-restoration-lovejoy-ga-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in Lovejoy, GA" || undefined}
      secondImg={"/images/mcdonough-water-damage-restoration-lovejoy-ga-second.jpg" || undefined}
      secondAlt={"Lovejoy, GA home" || undefined}
      mapPlace={"Lovejoy, GA"}
      mapTitle={"Map of Lovejoy, GA"}
      eyebrow={"Lovejoy, GA · Open 24 Hours"}
    />
  );
}
