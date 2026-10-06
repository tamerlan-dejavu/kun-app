import Link from "next/link";
import type { ReactNode } from "react";
import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";

export function PageHeader({
  title,
  backHref,
  action,
}: {
  title: string;
  backHref?: string;
  action?: ReactNode;
}) {
  return (
    <header className="sticky top-0 z-10 flex min-h-[56px] items-center gap-2 bg-canvas/95 px-2 backdrop-blur">
      {backHref ? (
        <Link
          href={backHref}
          aria-label={t("common.back")}
          className="flex h-tap w-11 items-center justify-center rounded-full hover:bg-sand-50"
        >
          <Icon name="back" />
        </Link>
      ) : (
        <span className="w-2" />
      )}
      <h1 className="min-w-0 flex-1 truncate text-lg">{title}</h1>
      {action}
    </header>
  );
}
