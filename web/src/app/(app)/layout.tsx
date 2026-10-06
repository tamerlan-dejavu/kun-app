import type { ReactNode } from "react";
import { SiteShell } from "@/components/layout/SiteShell";

// Закрытая часть приложения. Проверка сессии — в src/middleware.ts,
// незавершённый онбординг -> /onboarding (TODO).
export default function AppLayout({ children }: { children: ReactNode }) {
  return <SiteShell>{children}</SiteShell>;
}
