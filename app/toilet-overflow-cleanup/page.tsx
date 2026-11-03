import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Toilet Overflow Cleanup McDonough, GA",
  description: "Toilet overflowed or bathroom leaking into the ceiling below in McDonough? We clean, sanitize and dry it properly, 24/7. Call (470) 745-9798.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/toilet-overflow-cleanup/" },
  openGraph: {
    title: "Toilet Overflow Cleanup McDonough, GA",
    description: "Toilet overflowed or bathroom leaking into the ceiling below in McDonough? We clean, sanitize and dry it properly, 24/7. Call (470) 745-9798.",
    url: "https://mcdonoughwaterdamagerestoration.us/toilet-overflow-cleanup/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
    images: [{ url: "https://mcdonoughwaterdamagerestoration.us/images/mcdonough-toilet-overflow-cleanup-hero.jpg", alt: "Toilet overflow cleanup in McDonough, GA" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Toilet Overflow Cleanup McDonough, GA",
    description: "Toilet overflowed or bathroom leaking into the ceiling below in McDonough? We clean, sanitize and dry it properly, 24/7. Call (470) 745-9798.",
    images: ["https://mcdonoughwaterdamagerestoration.us/images/mcdonough-toilet-overflow-cleanup-hero.jpg"],
  },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/toilet-overflow-cleanup/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-toilet-overflow-cleanup-hero.jpg" || undefined}
      heroAlt={"Toilet overflow cleanup in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-toilet-overflow-cleanup-second.jpg" || undefined}
      secondAlt={"Bathroom leak cleanup in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
