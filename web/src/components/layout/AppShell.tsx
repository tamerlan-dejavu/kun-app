import type { ReactNode } from "react";
import { BottomNav } from "./BottomNav";

// Mobile-first; на десктопе контент в колонке до 480 px (раздел 4 ТЗ).
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto min-h-dvh max-w-app pb-24">
      <main>{children}</main>
      <BottomNav />
    </div>
  );
}
