import type { Metadata, Viewport } from "next";
import { Inter_Tight, JetBrains_Mono } from "next/font/google";
import type { ReactNode } from "react";
import { QueryProvider } from "@/components/providers/QueryProvider";
import "./globals.css";

// Гротеск для заголовков и текста, моноширинный — для дат, координат, категорий
const grotesk = Inter_Tight({
  subsets: ["latin", "cyrillic"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--font-grotesk",
});
const mono = JetBrains_Mono({ subsets: ["latin", "cyrillic"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: { default: "KUN", template: "%s — KUN" },
  description: "Собери компанию в кино, на прогулку или в клуб",
  manifest: "/manifest.webmanifest",
  // ||, а не ??: build-arg без значения приходит пустой строкой, а new URL("") падает
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://localhost"),
};

export const viewport: Viewport = {
  themeColor: "#F3F0E8",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru" className={`${grotesk.variable} ${mono.variable}`}>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
