import clsx from "clsx";
import type { ReactNode } from "react";

const tones = {
  brand: "bg-brand-100 text-brand-800",
  neutral: "bg-line/70 text-ink-muted",
  success: "bg-green-50 text-success",
  danger: "bg-red-50 text-danger",
};

export function Badge({ tone = "neutral", children }: { tone?: keyof typeof tones; children: ReactNode }) {
  return (
    <span className={clsx("inline-flex items-center gap-1 rounded-chip px-2.5 py-1 text-xs font-semibold", tones[tone])}>
      {children}
    </span>
  );
}
