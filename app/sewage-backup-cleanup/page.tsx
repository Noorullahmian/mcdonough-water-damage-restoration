import PageRenderer from "../../components/PageRenderer";
import pages from "../../data/pages.json";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sewage Backup Cleanup McDonough, GA 24/7 Black Water Removal",
  description: "Sewage coming up in your McDonough home? Stop using water and call (470) 745-9798. We remove, disinfect and dry sewage-damaged areas, 24/7.",
};

export default function Page() {
  const page = (pages as any[]).find((x) => x.slug === "/sewage-backup-cleanup/");
  return (
    <PageRenderer
      page={page}
      heroImg={"/images/mcdonough-sewage-backup-cleanup-hero.jpg" || undefined}
      heroAlt={"Sewage backup cleanup in McDonough, GA" || undefined}
      secondImg={"/images/mcdonough-sewage-backup-cleanup-second.jpg" || undefined}
      secondAlt={"Safe sewage cleanup in McDonough, GA" || undefined}
      mapPlace={"McDonough, GA"}
      mapTitle={"Map of McDonough, GA"}
      eyebrow={"McDonough, GA · Open 24 Hours"}
    />
  );
}
