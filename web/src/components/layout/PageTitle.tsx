import Link from "next/link";
import type { ReactNode } from "react";
import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";

// Заголовок страницы приложения: крупный гротеск в верхнем регистре, «назад» — квадратная кнопка.
export function PageTitle({ title, backHref, action }: { title: string; backHref?: string; action?: ReactNode }) {
  return (
    <div className="mb-8 flex items-center gap-4 border-b-2 border-ink pb-6 md:mb-10">
      {backHref && (
        <Link
          href={backHref}
          aria-label={t("common.back")}
          className="flex h-tap w-11 shrink-0 items-center justify-center border-2 border-ink bg-surface shadow-sm transition-[transform,box-shadow] duration-100 hover:translate-x-px hover:translate-y-px hover:shadow-[2px_2px_0_#111]"
        >
          <Icon name="back" />
        </Link>
      )}
      <h1 className="min-w-0 flex-1 truncate text-3xl uppercase leading-none md:text-6xl">{title}</h1>
      {action}
    </div>
  );
}
