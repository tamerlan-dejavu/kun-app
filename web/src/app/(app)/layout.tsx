import type { ReactNode } from "react";
import { AppShell } from "@/components/layout/AppShell";

// Закрытая часть приложения. Проверка сессии — в src/middleware.ts,
// незавершённый онбординг -> /onboarding (TODO).
export default function AppLayout({ children }: { children: ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
