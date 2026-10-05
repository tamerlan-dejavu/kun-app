import type { ReactNode } from "react";
import { BottomNav } from "./BottomNav";

// Mobile-first; на десктопе контент в колонке до 480px.
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto min-h-dvh max-w-app pb-20">
      <main>{children}</main>
      <BottomNav />
    </div>
  );
}
