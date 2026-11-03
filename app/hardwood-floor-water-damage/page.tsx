import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Hardwood Floor Water Damage McDonough, GA",
  description: "Wet, cupping or buckling hardwood floors in your McDonough home? We dry wood floors in place whenever they can be saved. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/hardwood-floor-water-damage/" },
  openGraph: {
    title: "Hardwood Floor Water Damage McDonough, GA",
    description: "Wet, cupping or buckling hardwood floors in your McDonough home? We dry wood floors in place whenever they can be saved. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/hardwood-floor-water-damage/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-hardwood-floor-water-damage-hero.jpg", alt: "Hardwood floor water damage in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Hardwood Floor Water Damage McDonough, GA",
    description: "Wet, cupping or buckling hardwood floors in your McDonough home? We dry wood floors in place whenever they can be saved. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-hardwood-floor-water-damage-hero.jpg"],
  },
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
