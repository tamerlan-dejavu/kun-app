import type { ReactNode } from "react";

// Состояние «пусто» с подсказкой, что делать. Место для маскота (ещё не выбран).
export function EmptyState({
  title,
  hint,
  action,
}: {
  title: string;
  hint?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center gap-3 px-6 py-14 text-center">
      <div aria-hidden className="mb-2 h-20 w-20 rounded-full bg-sand-100" />
      <p className="font-heading text-lg">{title}</p>
      {hint && <p className="text-ink-muted">{hint}</p>}
      {action}
    </div>
  );
}
