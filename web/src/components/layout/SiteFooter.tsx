import Link from "next/link";
import { t } from "@/i18n";
import { Container } from "./Container";

const LINKS = [
  { href: "/faq", label: "landing.faq" },
  { href: "/rules", label: "landing.rules" },
  { href: "/terms", label: "landing.terms" },
  { href: "/privacy", label: "landing.privacy" },
  { href: "/support", label: "landing.support" },
] as const;

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-line bg-surface/60 py-10">
      <Container className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="font-heading text-brand">KUN</p>
          <p className="mt-1 text-sm text-ink-muted">{t("landing.tagline")}</p>
        </div>
        <nav aria-label={t("landing.footerNav")} className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-ink-muted">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="hover:text-ink">
              {t(l.label)}
            </Link>
          ))}
        </nav>
        <p className="whitespace-nowrap text-sm text-ink-muted">
          © {new Date().getFullYear()} {t("landing.copyright")}
        </p>
      </Container>
    </footer>
  );
}
