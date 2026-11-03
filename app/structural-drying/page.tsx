import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Water Damage Drying McDonough, GA",
  description: "Walls, floors or ceilings still wet after a leak in McDonough? We dry your home to a measured standard with commercial equipment. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/structural-drying/" },
  openGraph: {
    title: "Water Damage Drying McDonough, GA",
    description: "Walls, floors or ceilings still wet after a leak in McDonough? We dry your home to a measured standard with commercial equipment. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/structural-drying/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-structural-drying-hero.jpg", alt: "Structural drying in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Water Damage Drying McDonough, GA",
    description: "Walls, floors or ceilings still wet after a leak in McDonough? We dry your home to a measured standard with commercial equipment. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-structural-drying-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/structural-drying/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-structural-drying-hero.jpg" || undefined}
      heroAlt={"Structural drying in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-structural-drying-second.jpg" || undefined}
      secondAlt={"Moisture readings during structural drying in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
