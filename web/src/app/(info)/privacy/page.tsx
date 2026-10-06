import type { Metadata } from "next";
import { privacy } from "@/content/ru/privacy";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Политика конфиденциальности" };

// /privacy — доступна без входа (раздел 3.1 ТЗ)
export default function Page() {
  return <TextPage doc={privacy} />;
}
