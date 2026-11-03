import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of Use | McDonough Water Damage Restoration",
  description: "The terms and conditions for using the McDonough Water Damage Restoration website.",
  alternates: { canonical: "https://mcdonoughwaterdamagerestoration.us/terms-of-use/" },
  openGraph: {
    title: "Terms of Use | McDonough Water Damage Restoration",
    description: "The terms and conditions for using the McDonough Water Damage Restoration website.",
    url: "https://mcdonoughwaterdamagerestoration.us/terms-of-use/",
    siteName: "McDonough Water Damage Restoration",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Terms of Use | McDonough Water Damage Restoration",
    description: "The terms and conditions for using the McDonough Water Damage Restoration website.",
  },
  robots: { index: false, follow: true },
};

export default function Page() {
  return (
    <>
      <section className="section">
        <div className="section-inner">
          <h1>Terms of Use</h1>
          <p>Effective date: November 3, 2026</p>
          <p>Welcome to mcdonoughwaterdamagerestoration.us (the &quot;Site&quot;), operated by McDonough Water Damage Restoration (&quot;we,&quot; &quot;us&quot; or &quot;our&quot;). By using this Site, you agree to these Terms of Use. If you do not agree, please do not use the Site.</p>
          <h2>Use of the Site</h2>
          <p>You may use this Site for lawful purposes only. You agree not to:</p>
          <ul>
            <li>Submit false or misleading information</li>
            <li>Attempt to access areas of the Site you are not authorized to access</li>
            <li>Interfere with the Site&apos;s operation or security</li>
            <li>Copy, reproduce or resell Site content without our written permission</li>
          </ul>
          <h2>Website Content</h2>
          <p>The content on this Site is for general information only. Price ranges are general estimates, not quotes. Information about insurance, utilities and building materials is general and is not legal, insurance or professional advice. Every property is different, and the details of any job are confirmed after an on-site inspection.</p>
          <h2>Service Requests</h2>
          <p>Contacting us through the Site or by phone does not by itself create a service agreement. The scope, pricing and terms of any work are confirmed with you in writing before work begins.</p>
          <h2>Emergencies</h2>
          <p>If anyone is in danger, or if there is a gas smell, an electrical hazard, a fire or a ceiling at risk of collapse, leave the area and call 911 first.</p>
          <h2>Intellectual Property</h2>
          <p>All content on this Site, including text, images, logos and design, belongs to us or is used with permission and is protected by copyright and other laws. You may view and print pages for personal, non-commercial use only.</p>
          <h2>Links to Other Websites</h2>
          <p>This Site may contain links to other websites. We do not control those websites and are not responsible for their content or practices.</p>
          <h2>Disclaimer of Warranties</h2>
          <p>This Site is provided &quot;as is&quot; and &quot;as available.&quot; We make no warranties of any kind, express or implied, about the accuracy, completeness or availability of the Site or its content.</p>
          <h2>Limitation of Liability</h2>
          <p>To the fullest extent permitted by law, we are not liable for any indirect, incidental, special or consequential damages arising from your use of this Site.</p>
          <h2>Indemnification</h2>
          <p>You agree to indemnify and hold us harmless from any claims or losses resulting from your misuse of the Site or violation of these Terms.</p>
          <h2>Privacy</h2>
          <p>Your use of this Site is also governed by our <Link href="/privacy-policy/">Privacy Policy</Link>.</p>
          <h2>Governing Law</h2>
          <p>These Terms are governed by the laws of the State of Georgia.</p>
          <h2>Changes to These Terms</h2>
          <p>We may update these Terms from time to time. Changes will be posted on this page with a new effective date. Continued use of the Site means you accept the updated Terms.</p>
          <h2>Contact Us</h2>
          <p>If you have questions about these Terms, call <a href="tel:+14707459798">(470) 745-9798</a> or visit our <Link href="/contact-us/">contact page</Link>.</p>
          <p>McDonough Water Damage Restoration · McDonough, GA · (470) 745-9798</p>
        </div>
      </section>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org",
        "@graph": [
          { "@type": "WebPage", "@id": "https://mcdonoughwaterdamagerestoration.us/terms-of-use/#webpage", url: "https://mcdonoughwaterdamagerestoration.us/terms-of-use/", name: "Terms of Use | McDonough Water Damage Restoration", isPartOf: { "@id": "https://mcdonoughwaterdamagerestoration.us/#website" }, about: { "@id": "https://mcdonoughwaterdamagerestoration.us/#organization" }, breadcrumb: { "@id": "https://mcdonoughwaterdamagerestoration.us/terms-of-use/#breadcrumb" }, inLanguage: "en" },
          { "@type": "BreadcrumbList", "@id": "https://mcdonoughwaterdamagerestoration.us/terms-of-use/#breadcrumb", itemListElement: [
            { "@type": "ListItem", position: 1, name: "Home", item: "https://mcdonoughwaterdamagerestoration.us/" },
            { "@type": "ListItem", position: 2, name: "Terms of Use", item: "https://mcdonoughwaterdamagerestoration.us/terms-of-use/" },
          ] },
        ],
      }) }} />
    </>
  );
}
