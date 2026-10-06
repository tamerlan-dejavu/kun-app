import clsx from "clsx";
import type { ReactNode } from "react";
import { hasSession } from "@/lib/api/server";
import { AppHeader } from "./AppHeader";
import { BottomNav } from "./BottomNav";
import { Container } from "./Container";
import { GuestHeader } from "./GuestHeader";
import { SiteFooter } from "./SiteFooter";

type Props = {
  children: ReactNode;
  /** Обернуть контент в Container (лендинг рисует полосы на всю ширину сам). */
  contained?: boolean;
  /** Подвал и нижние вкладки на телефоне — чат их отключает: ему нужна вся высота. */
  footer?: boolean;
  bottomNav?: boolean;
};

// Каркас любой страницы: шапка (гостя или вошедшего) + контент + подвал.
// На телефоне у вошедшего ещё нижние вкладки (md:hidden).
export async function SiteShell({ children, contained = true, footer = true, bottomNav = true }: Props) {
  const loggedIn = await hasSession();
  const showBottomNav = loggedIn && bottomNav;
  return (
    <div className={clsx("flex min-h-dvh flex-col", showBottomNav && "pb-20 md:pb-0")}>
      {loggedIn ? <AppHeader /> : <GuestHeader />}
      <main className="flex-1">
        {contained ? <Container className="py-6 md:py-10">{children}</Container> : children}
      </main>
      {footer && <SiteFooter />}
      {showBottomNav && <BottomNav />}
    </div>
  );
}
