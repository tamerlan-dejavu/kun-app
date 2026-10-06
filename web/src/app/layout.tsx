import type { Metadata, Viewport } from "next";
import { Manrope, Unbounded } from "next/font/google";
import type { ReactNode } from "react";
import { QueryProvider } from "@/components/providers/QueryProvider";
import "./globals.css";

const manrope = Manrope({ subsets: ["latin", "cyrillic"], variable: "--font-manrope" });
const unbounded = Unbounded({ subsets: ["latin", "cyrillic"], variable: "--font-unbounded" });

export const metadata: Metadata = {
  title: { default: "KUN", template: "%s — KUN" },
  description: "Собери компанию в кино, на прогулку или в клуб",
  manifest: "/manifest.webmanifest",
  // ||, а не ??: build-arg без значения приходит пустой строкой, а new URL("") падает
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://localhost"),
};

export const viewport: Viewport = {
  themeColor: "#537179",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru" className={`${manrope.variable} ${unbounded.variable}`}>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
