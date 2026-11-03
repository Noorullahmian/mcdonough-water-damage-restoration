import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Ceiling Water Damage Repair McDonough, GA",
  description: "Water dripping from your ceiling in McDonough? We find the source, dry the attic and ceiling, and repair the damage, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/ceiling-leak-water-damage/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/ceiling-leak-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-ceiling-leak-water-damage-hero.jpg" || undefined}
      heroAlt={"Ceiling leak water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-ceiling-leak-water-damage-second.jpg" || undefined}
      secondAlt={"Roof leak ceiling damage in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
