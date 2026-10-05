"use client";

import clsx from "clsx";
import type { ReactNode } from "react";

/** Переключатель-фильтр. aria-pressed — скринридер объявит, выбран ли. */
export function Chip({
  selected,
  onClick,
  children,
}: {
  selected: boolean;
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={onClick}
      className={clsx(
        "inline-flex min-h-tap shrink-0 items-center gap-1.5 rounded-chip border px-4 text-sm font-semibold transition-colors",
        selected
          ? "border-brand bg-brand text-ink"
          : "border-line bg-surface text-ink-muted hover:text-ink",
      )}
    >
      {children}
    </button>
  );
}
