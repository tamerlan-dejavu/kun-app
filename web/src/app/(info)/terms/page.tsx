import type { Metadata } from "next";
import { terms } from "@/content/ru/terms";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Пользовательское соглашение" };

// /terms — доступна без входа (раздел 3.1 ТЗ)
export default function Page() {
  return <TextPage doc={terms} />;
}
