import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Slab Leak Water Damage McDonough, GA Under-Floor Leak Drying",
  description: "Warm spots on the floor, wet carpet with no visible leak, or a spiking water bill in McDonough? We dry slab leak water damage. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/slab-leak-water-damage/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/slab-leak-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-slab-leak-water-damage-hero.jpg" || undefined}
      heroAlt={"Slab leak water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-slab-leak-water-damage-second.jpg" || undefined}
      secondAlt={"Slab leak wet floor in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
