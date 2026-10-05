import type { ReactNode } from "react";

export default function InfoLayout({ children }: { children: ReactNode }) {
  return <main className="mx-auto max-w-app p-4">{children}</main>;
}
