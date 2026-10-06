"use client";

import clsx from "clsx";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { t } from "@/i18n";
import { Icon, type IconName } from "@/components/ui/Icon";

const ITEMS: { href: string; label: Parameters<typeof t>[0]; icon: IconName }[] = [
  { href: "/for-you", label: "nav.forYou", icon: "near" },
  { href: "/feed", label: "nav.feed", icon: "feed" },
  { href: "/my", label: "nav.my", icon: "list" },
  { href: "/profile", label: "nav.profile", icon: "user" },
];

export function BottomNav() {
  const pathname = usePathname();
  return (
    <nav
      aria-label={t("nav.main")}
      className="fixed inset-x-0 bottom-0 z-30 border-t-2 border-ink bg-canvas md:hidden"
    >
      <ul className="mx-auto flex max-w-lg justify-around pb-[env(safe-area-inset-bottom)]">
        {ITEMS.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <li key={item.href}>
              <Link
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={clsx(
                  "flex min-h-tap min-w-[72px] flex-col items-center gap-0.5 px-3 py-2 text-xs font-semibold",
                  active ? "border-t-[3px] border-brand text-ink" : "border-t-[3px] border-transparent text-ink-muted",
                )}
              >
                <Icon name={item.icon} />
                {t(item.label)}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
