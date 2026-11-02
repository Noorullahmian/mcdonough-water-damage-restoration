import PageRenderer from "../components/PageRenderer";
import pages from "../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "24/7 Water Damage Restoration in McDonough, GA",
  description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-home-hero.jpg" || undefined}
      heroAlt={"Water damage restoration in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-home-second.jpg" || undefined}
      secondAlt={"Structural drying equipment in a McDonough home" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"Open 24 Hours · McDonough & Henry County"}
    />
  );
}
