import type { ReactNode } from "react";
import { SiteShell } from "@/components/layout/SiteShell";

// FAQ, правила, соглашение, конфиденциальность, поддержка — доступны без входа.
export default function InfoLayout({ children }: { children: ReactNode }) {
  return (
    <SiteShell>
      <div className="max-w-3xl">{children}</div>
    </SiteShell>
  );
}
