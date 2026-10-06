import clsx from "clsx";
import type { ReactNode } from "react";

// Метка: моноширинная, с рамкой. Не путать с кнопкой — без тени.
const tones = {
  brand: "border-ink bg-brand text-ink",
  sand: "border-ink bg-sand-100 text-ink",
  neutral: "border-ink bg-surface text-ink",
  success: "border-success bg-surface text-success",
  danger: "border-danger bg-surface text-danger",
  dark: "border-ink bg-ink text-canvas",
};

export function Badge({ tone = "neutral", children }: { tone?: keyof typeof tones; children: ReactNode }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1 rounded-chip border-[1.5px] px-2 py-0.5 font-mono text-[11px] font-bold uppercase tracking-wider",
        tones[tone],
      )}
    >
      {children}
    </span>
  );
}
