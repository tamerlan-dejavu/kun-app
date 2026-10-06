import type { Metadata } from "next";
import { support } from "@/content/ru/support";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Поддержка" };

// /support — доступна без входа (раздел 3.1 ТЗ)
export default function Page() {
  return <TextPage doc={support} />;
}
