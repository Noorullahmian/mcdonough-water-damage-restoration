import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AC Leak Water Damage McDonough, GA",
  description: "AC leaking water into your ceiling or closet in McDonough? We dry the attic, ceiling and walls and stop mold, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/ac-leak-water-damage/" },
  openGraph: {
    title: "AC Leak Water Damage McDonough, GA",
    description: "AC leaking water into your ceiling or closet in McDonough? We dry the attic, ceiling and walls and stop mold, 24/7. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/ac-leak-water-damage/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-ac-leak-water-damage-hero.jpg", alt: "AC leak water damage in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "AC Leak Water Damage McDonough, GA",
    description: "AC leaking water into your ceiling or closet in McDonough? We dry the attic, ceiling and walls and stop mold, 24/7. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-ac-leak-water-damage-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/ac-leak-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-ac-leak-water-damage-hero.jpg" || undefined}
      heroAlt={"AC leak water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-ac-leak-water-damage-second.jpg" || undefined}
      secondAlt={"Attic AC unit in a McDonough home" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
