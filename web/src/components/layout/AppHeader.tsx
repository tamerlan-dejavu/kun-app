"use client";

import clsx from "clsx";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { Avatar } from "@/components/ui/Avatar";
import { buttonClass } from "@/components/ui/Button";
import { Container } from "./Container";
import { Coords, Logo } from "./Brand";

const LINKS = [
  { href: "/feed", label: "nav.feed" },
  { href: "/map", label: "nav.map" },
  { href: "/my", label: "nav.my" },
] as const;

// Шапка вошедшего: разделы, «+ Создать», координаты, профиль.
export function AppHeader() {
  const pathname = usePathname();
  const me = useMe();
  return (
    <header className="sticky top-0 z-30 border-b-2 border-ink bg-canvas">
      <Container className="flex h-16 items-center gap-8">
        <Logo href="/feed" />
        <nav aria-label={t("nav.main")} className="hidden h-full gap-6 md:flex">
          {LINKS.map((l) => {
            const active = pathname.startsWith(l.href);
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={clsx(
                  "meta flex items-center border-b-[3px] font-bold",
                  active ? "border-brand" : "border-transparent hover:border-ink",
                )}
              >
                {t(l.label)}
              </Link>
            );
          })}
        </nav>
        <div className="ml-auto flex items-center gap-5">
          <Coords />
          <Link href="/new" className={clsx(buttonClass("primary"), "hidden md:inline-flex")}>
            {t("nav.create")}
          </Link>
          <Link href="/profile" aria-label={t("nav.profile")} className="flex min-h-tap items-center gap-2">
            <Avatar name={me.data?.name} photo={me.data?.photo} size="sm" />
            <span className="meta hidden font-bold lg:inline">{me.data?.name}</span>
          </Link>
        </div>
      </Container>
    </header>
  );
}
