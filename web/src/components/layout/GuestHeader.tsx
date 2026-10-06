import Link from "next/link";
import { t } from "@/i18n";
import { buttonClass } from "@/components/ui/Button";
import { Container } from "./Container";

const LINKS = [
  { href: "/#how", label: "landing.navHow" },
  { href: "/#where", label: "landing.navWhere" },
  { href: "/#safety", label: "landing.navSafety" },
] as const;

// Шапка для гостя: разделы лендинга, «Войти» и «Начать».
export function GuestHeader() {
  return (
    <header className="sticky top-0 z-20 border-b border-line/70 bg-canvas/90 backdrop-blur">
      <Container className="flex h-16 items-center gap-6">
        <Link href="/" className="font-heading text-xl text-brand">
          KUN
        </Link>
        <nav aria-label={t("landing.nav")} className="hidden flex-1 gap-6 md:flex">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="text-sm font-semibold text-ink-muted hover:text-ink">
              {t(l.label)}
            </Link>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-2">
          <Link href="/login" className={buttonClass("ghost")}>
            {t("landing.login")}
          </Link>
          <Link href="/feed" className={buttonClass("primary")}>
            {t("common.start")}
          </Link>
        </div>
      </Container>
    </header>
  );
}
