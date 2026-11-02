import type { Metadata } from "next";
import "./globals.css";
import { Header, Footer } from "../components/Chrome";

export const metadata: Metadata = {
  title: "McDonough Water Damage Restoration | 24/7 Water Damage Help",
  description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: "McDonough Water Damage Restoration",
    telephone: "+1-470-745-9798",
    openingHours: "Mo-Su 00:00-24:00",
    areaServed: { "@type": "AdministrativeArea", name: "McDonough, GA 30252 and 30253 and Henry County" },
    description: "24/7 water damage restoration for homes and businesses in McDonough and the south metro Atlanta area.",
  };
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#main">Skip to content</a>
        <Header current="" />
        <main id="main">{children}</main>
        <Footer />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      </body>
    </html>
  );
}
