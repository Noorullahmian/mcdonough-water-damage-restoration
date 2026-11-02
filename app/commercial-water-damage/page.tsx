import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Commercial Water Damage Restoration McDonough, GA",
  description: "Water damage at your McDonough business, office or rental? We remove water, dry the building and keep downtime low, 24/7. Call (470) 745-9798.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/commercial-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-commercial-water-damage-hero.jpg" || undefined}
      heroAlt={"Commercial water damage restoration in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-commercial-water-damage-second.jpg" || undefined}
      secondAlt={"Commercial water damage cleanup in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
