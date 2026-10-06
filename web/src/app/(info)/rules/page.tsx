import type { Metadata } from "next";
import { rules } from "@/content/ru/rules";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Правила сообщества" };

// /rules — доступна без входа (раздел 3.1 ТЗ)
export default function Page() {
  return <TextPage doc={rules} />;
}
