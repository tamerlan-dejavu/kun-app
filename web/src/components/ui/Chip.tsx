"use client";

import clsx from "clsx";
import type { ReactNode } from "react";

/** Фильтр-переключатель: моноширинная метка; выбранный — терракотовый «нажатый». aria-pressed — для скринридера. */
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
        "inline-flex min-h-tap shrink-0 items-center gap-1.5 rounded-chip border-2 border-ink px-3.5 font-mono text-xs font-bold uppercase tracking-wider transition-[transform,box-shadow] duration-100",
        selected
          ? "translate-x-0.5 translate-y-0.5 bg-brand text-ink shadow-none"
          : "bg-surface text-ink shadow-sm hover:translate-x-px hover:translate-y-px hover:shadow-[2px_2px_0_#111]",
      )}
    >
      {children}
    </button>
  );
}
