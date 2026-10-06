import Link from "next/link";
import type { ReactNode } from "react";
import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";

// Заголовок страницы: «назад», h1, действие справа.
export function PageTitle({
  title,
  backHref,
  action,
}: {
  title: string;
  backHref?: string;
  action?: ReactNode;
}) {
  return (
    <div className="mb-6 flex items-center gap-3 md:mb-8">
      {backHref && (
        <Link
          href={backHref}
          aria-label={t("common.back")}
          className="-ml-2 flex h-tap w-11 shrink-0 items-center justify-center rounded-full hover:bg-sand-50"
        >
          <Icon name="back" />
        </Link>
      )}
      <h1 className="min-w-0 flex-1 truncate text-2xl md:text-4xl">{title}</h1>
      {action}
    </div>
  );
}
