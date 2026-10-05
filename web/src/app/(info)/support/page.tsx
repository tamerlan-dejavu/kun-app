import type { Metadata } from "next";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Поддержка" };

// /support — доступна без входа. TODO: текст (согласовать с юристом).
export default function Page() {
  return <TextPage />;
}
