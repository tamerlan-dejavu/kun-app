import type { ReactNode } from "react";

// Состояние «пусто» с подсказкой, что делать. Место для маскота.
export function EmptyState({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <div className="flex flex-col items-center gap-4 py-12 text-center">
      {/* TODO: маскот */}
      <p>{title}</p>
      {action}
    </div>
  );
}
