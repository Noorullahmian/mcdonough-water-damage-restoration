import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Emergency Water Removal McDonough, GA 24/7 Water Extraction",
  description: "Standing water in your McDonough home? Our team pumps it out, extracts carpets and starts drying the same visit, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/emergency-water-extraction/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/emergency-water-extraction/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-emergency-water-extraction-hero.jpg" || undefined}
      heroAlt={"Emergency water extraction in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-emergency-water-extraction-second.jpg" || undefined}
      secondAlt={"Water extraction from carpet in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
