import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mold Remediation McDonough, GA",
  description: "Musty smell or mold after a leak in your McDonough home? We contain it, remove it and fix the moisture behind it. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/mold-remediation/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/mold-remediation/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-mold-remediation-hero.jpg" || undefined}
      heroAlt={"Mold remediation in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-mold-remediation-second.jpg" || undefined}
      secondAlt={"Mold removal after water damage in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
