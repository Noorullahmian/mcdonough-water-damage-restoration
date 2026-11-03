import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Burst Pipe Water Damage McDonough, GA",
  description: "Pipe burst in your McDonough home? Shut off the water and call (470) 745-9798. We dry walls, ceilings and floors after frozen or broken pipes, 24/7.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/burst-pipe-water-damage/" },
  openGraph: {
    title: "Burst Pipe Water Damage McDonough, GA",
    description: "Pipe burst in your McDonough home? Shut off the water and call (470) 745-9798. We dry walls, ceilings and floors after frozen or broken pipes, 24/7.",
    url: "https://mcdonoughwaterdamagerestoration.us/burst-pipe-water-damage/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-burst-pipe-water-damage-hero.jpg", alt: "Burst pipe water damage in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Burst Pipe Water Damage McDonough, GA",
    description: "Pipe burst in your McDonough home? Shut off the water and call (470) 745-9798. We dry walls, ceilings and floors after frozen or broken pipes, 24/7.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-burst-pipe-water-damage-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/burst-pipe-water-damage/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-burst-pipe-water-damage-hero.jpg" || undefined}
      heroAlt={"Burst pipe water damage in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-burst-pipe-water-damage-second.jpg" || undefined}
      secondAlt={"Burst pipe repair in a McDonough home" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
