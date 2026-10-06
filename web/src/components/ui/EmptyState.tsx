import type { ReactNode } from "react";

// «Пусто»: крупная типографика вместо иллюстрации; место для маскота — рамка слева.
export function EmptyState({ title, hint, action }: { title: string; hint?: string; action?: ReactNode }) {
  return (
    <div className="card flex flex-col items-start gap-4 p-8 md:flex-row md:items-center md:p-10">
      <div aria-hidden className="meta flex h-20 w-20 shrink-0 items-center justify-center border-2 border-dashed border-ink">
        ×
      </div>
      <div className="space-y-2">
        <p className="font-heading text-2xl font-extrabold uppercase tracking-tight">{title}</p>
        {hint && <p className="max-w-lg text-ink-muted">{hint}</p>}
        {action && <div className="pt-2">{action}</div>}
      </div>
    </div>
  );
}
