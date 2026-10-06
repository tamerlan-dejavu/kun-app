import type { ReactNode } from "react";

// Каркас (шапка/подвал) задаёт каждая страница сама: чату подвал не нужен.
export default function GatheringLayout({ children }: { children: ReactNode }) {
  return children;
}
