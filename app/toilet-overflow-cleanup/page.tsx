import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Toilet Overflow Cleanup McDonough, GA",
  description: "Toilet overflowed or bathroom leaking into the ceiling below in McDonough? We clean, sanitize and dry it properly, 24/7. Call (470) 745-9798.",
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
