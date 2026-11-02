import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Washing Machine & Appliance Leak Water Damage McDonough, GA",
  description: "Washer overflow, dishwasher leak or fridge line leak in your McDonough home? We dry floors, cabinets and ceilings below, 24/7. Call (470) 745-9798.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/appliance-leak-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-appliance-leak-water-damage-hero.jpg" || undefined}
      heroAlt={"Appliance leak water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-appliance-leak-water-damage-second.jpg" || undefined}
      secondAlt={"Washing machine leak in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
