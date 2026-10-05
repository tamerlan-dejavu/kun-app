import type { ReactNode } from "react";

// Страница сбора открывается и гостем по ссылке — без нижней навигации приложения.
export default function GatheringLayout({ children }: { children: ReactNode }) {
  return <div className="mx-auto min-h-dvh max-w-app">{children}</div>;
}
