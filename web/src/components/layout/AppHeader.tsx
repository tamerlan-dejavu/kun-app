"use client";

import clsx from "clsx";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { Avatar } from "@/components/ui/Avatar";
import { buttonClass } from "@/components/ui/Button";
import { Container } from "./Container";

const LINKS = [
  { href: "/feed", label: "nav.feed" },
  { href: "/my", label: "nav.my" },
] as const;

// Шапка для вошедшего: разделы приложения, «Создать сбор», профиль.
export function AppHeader() {
  const pathname = usePathname();
  const me = useMe();
  return (
    <header className="sticky top-0 z-20 border-b border-line/70 bg-canvas/90 backdrop-blur">
      <Container className="flex h-16 items-center gap-8">
        <Link href="/feed" className="font-heading text-xl text-brand">
          KUN
        </Link>
        <nav aria-label={t("nav.main")} className="hidden h-full gap-6 md:flex">
          {LINKS.map((l) => {
            const active = pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={clsx(
                  "flex items-center border-b-2 text-sm font-semibold",
                  active ? "border-brand text-ink" : "border-transparent text-ink-muted hover:text-ink",
                )}
              >
                {t(l.label)}
              </Link>
            );
          })}
        </nav>
        <div className="ml-auto flex items-center gap-3">
          <Link href="/new" className={clsx(buttonClass("primary"), "hidden md:inline-flex")}>
            {t("nav.create")}
          </Link>
          <Link
            href="/profile"
            aria-label={t("nav.profile")}
            className="flex min-h-tap items-center gap-2 rounded-chip pr-1 hover:bg-sand-50"
          >
            <Avatar name={me.data?.name} photo={me.data?.photo} size="sm" />
            <span className="hidden text-sm font-semibold lg:inline">{me.data?.name}</span>
          </Link>
        </div>
      </Container>
    </header>
  );
}
