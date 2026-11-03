import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact Us 24/7 | Emergency Water Damage Help McDonough, GA",
  description: "Water damage in McDonough or Henry County? Call (470) 745-9798 any hour or send a request, and a local water damage crew is on the way.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/contact-us/" },
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/contact-us/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-contact-us-hero.jpg" || undefined}
      heroAlt={"Emergency water damage help in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-contact-us-second.jpg" || undefined}
      secondAlt={"Water damage crew in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
