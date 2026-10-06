import Link from "next/link";
import { t } from "@/i18n";
import { Container } from "./Container";

const LINKS = [
  { href: "/rules", label: "landing.rules" },
  { href: "/terms", label: "landing.terms" },
  { href: "/privacy", label: "landing.privacy" },
  { href: "/support", label: "landing.support" },
] as const;

export function SiteFooter() {
  return (
    <footer className="border-t border-line py-10">
      <Container className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <p className="font-heading text-brand">KUN</p>
        <nav className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-ink-muted">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="hover:text-ink">
              {t(l.label)}
            </Link>
          ))}
        </nav>
        <p className="text-sm text-ink-muted">© {new Date().getFullYear()} {t("landing.copyright")}</p>
      </Container>
    </footer>
  );
}
