import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mold Remediation McDonough, GA",
  description: "Musty smell or mold after a leak in your McDonough home? We contain it, remove it and fix the moisture behind it. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/mold-remediation/" },
  openGraph: {
    title: "Mold Remediation McDonough, GA",
    description: "Musty smell or mold after a leak in your McDonough home? We contain it, remove it and fix the moisture behind it. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/mold-remediation/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-mold-remediation-hero.jpg", alt: "Mold remediation in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Mold Remediation McDonough, GA",
    description: "Musty smell or mold after a leak in your McDonough home? We contain it, remove it and fix the moisture behind it. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-mold-remediation-hero.jpg"],
  },
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
