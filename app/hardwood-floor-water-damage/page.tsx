import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Hardwood Floor Water Damage McDonough, GA",
  description: "Wet, cupping or buckling hardwood floors in your McDonough home? We dry wood floors in place whenever they can be saved. Call (470) 745-9798.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/hardwood-floor-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-hardwood-floor-water-damage-hero.jpg" || undefined}
      heroAlt={"Hardwood floor water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-hardwood-floor-water-damage-second.jpg" || undefined}
      secondAlt={"Hardwood floor drying in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
