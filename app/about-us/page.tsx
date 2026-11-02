import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Us | McDonough Water Damage Restoration",
  description: "Local water damage restoration for McDonough and Henry County homes and businesses: how the work is done, what to expect and the areas served.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/about-us/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-about-us-hero.jpg" || undefined}
      heroAlt={"About McDonough Water Damage Restoration" || undefined}
      secondImg={"/images/mcdonough-about-us-second.jpg" || undefined}
      secondAlt={"Moisture inspection in a McDonough home" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
