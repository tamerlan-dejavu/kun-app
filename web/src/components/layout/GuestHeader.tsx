import Link from "next/link";
import { t } from "@/i18n";
import { buttonClass } from "@/components/ui/Button";
import { Container } from "./Container";
import { Coords, Logo } from "./Brand";

const LINKS = [
  { href: "/#places", label: "nav.places" },
  { href: "/#today", label: "nav.today" },
  { href: "/#people", label: "nav.people" },
  { href: "/#map", label: "nav.map" },
] as const;

// Шапка гостя: минимальная навигация моноширинным, справа — координаты и вход.
export function GuestHeader() {
  return (
    <header className="sticky top-0 z-30 border-b-2 border-ink bg-canvas">
      <Container className="flex h-16 items-center gap-8">
        <Logo href="/" />
        <nav aria-label={t("landing.nav")} className="hidden gap-6 md:flex">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="meta font-bold hover:text-brand-700 hover:underline hover:underline-offset-4">
              {t(l.label)}
            </Link>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-5">
          <Coords />
          <Link href="/login" className="meta font-bold hover:underline hover:underline-offset-4">
            {t("landing.login")}
          </Link>
          <Link href="/new" className={buttonClass("primary")}>
            {t("nav.create")}
          </Link>
        </div>
      </Container>
    </header>
  );
}
