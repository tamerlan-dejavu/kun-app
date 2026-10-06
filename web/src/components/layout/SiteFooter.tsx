import Link from "next/link";
import { t } from "@/i18n";
import { Container } from "./Container";

const INFO = [
  { href: "/faq", label: "landing.faq" },
  { href: "/rules", label: "landing.rules" },
  { href: "/terms", label: "landing.terms" },
  { href: "/privacy", label: "landing.privacy" },
  { href: "/support", label: "landing.support" },
] as const;

const CITY = [
  { href: "/#today", label: "nav.today" },
  { href: "/#people", label: "nav.people" },
  { href: "/#map", label: "nav.map" },
] as const;

// Подвал — чёрная плита с огромным словом KUN, выходящим за край.
export function SiteFooter() {
  return (
    <footer className="mt-auto overflow-hidden border-t-2 border-ink bg-ink text-canvas">
      <Container className="grid gap-10 py-12 md:grid-cols-4">
        <p className="max-w-xs text-canvas/80 md:col-span-2">{t("footer.tagline")}</p>
        <nav aria-label={t("footer.city")}>
          <p className="meta mb-3 text-brand">{t("footer.city")}</p>
          <ul className="space-y-2">
            {CITY.map((l) => (
              <li key={l.href}>
                <Link href={l.href} className="hover:underline hover:underline-offset-4">
                  {t(l.label)}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <nav aria-label={t("footer.info")}>
          <p className="meta mb-3 text-brand">{t("footer.info")}</p>
          <ul className="space-y-2">
            {INFO.map((l) => (
              <li key={l.href}>
                <Link href={l.href} className="hover:underline hover:underline-offset-4">
                  {t(l.label)}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </Container>
      <Container className="flex items-end justify-between gap-4 pb-4">
        <p aria-hidden className="select-none font-heading text-[clamp(5rem,22vw,18rem)] font-black leading-[0.75] tracking-tighter text-canvas/95">
          KUN
        </p>
        <p className="meta whitespace-nowrap pb-2 text-canvas/70">
          © {new Date().getFullYear()} · {t("home.coords")}
        </p>
      </Container>
    </footer>
  );
}
