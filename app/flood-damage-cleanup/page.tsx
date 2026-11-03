import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Flood Damage Cleanup McDonough, GA Storm Water Removal 24/7",
  description: "House flooded after heavy rain in McDonough? We remove floodwater, sanitize and dry your home, 24/7 across Henry County. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/flood-damage-cleanup/" },
  openGraph: {
    title: "Flood Damage Cleanup McDonough, GA Storm Water Removal 24/7",
    description: "House flooded after heavy rain in McDonough? We remove floodwater, sanitize and dry your home, 24/7 across Henry County. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/flood-damage-cleanup/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-flood-damage-cleanup-hero.jpg", alt: "Flood damage cleanup in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Flood Damage Cleanup McDonough, GA Storm Water Removal 24/7",
    description: "House flooded after heavy rain in McDonough? We remove floodwater, sanitize and dry your home, 24/7 across Henry County. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-flood-damage-cleanup-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/flood-damage-cleanup/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-flood-damage-cleanup-hero.jpg" || undefined}
      heroAlt={"Flood damage cleanup in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-flood-damage-cleanup-second.jpg" || undefined}
      secondAlt={"Storm flooding near McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
