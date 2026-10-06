import clsx from "clsx";
import type { ReactNode } from "react";

// Ширина контента лендинга: на десктопе до 1152 px, поля 20 px на телефоне и 32 px шире.
export function Container({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={clsx("mx-auto w-full max-w-6xl px-5 md:px-8", className)}>{children}</div>;
}
