import type { Metadata } from "next";
import "./globals.css";
import { Header, Footer } from "../components/Chrome";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

export const metadata: Metadata = {
  title: "McDonough Water Damage Restoration | 24/7 Water Damage Help",
  description: "Water damage restoration in McDonough, GA starts the moment you call. Local water mitigation technicians remove the water, find the moisture you can't see.",
  icons: {
    icon: [
      { url: `${BASE}/favicon.ico`, sizes: "any" },
      { url: `${BASE}/favicon-48x48.png`, type: "image/png", sizes: "48x48" },
    ],
    apple: [{ url: `${BASE}/apple-touch-icon.png`, sizes: "180x180" }],
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#main">Skip to content</a>
        <Header current="" />
        <main id="main">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
