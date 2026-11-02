import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Heater Leak Cleanup McDonough, GA",
  description: "Water heater leaking or burst in your McDonough garage, closet or attic? Shut off the water and call (470) 745-9798. We extract and dry it, 24/7.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/water-heater-leak-cleanup/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-water-heater-leak-cleanup-hero.jpg" || undefined}
      heroAlt={"Water heater leak cleanup in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-water-heater-leak-cleanup-second.jpg" || undefined}
      secondAlt={"Water heater leak in a McDonough garage" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
