import type { Metadata } from "next";
import { faq } from "@/content/ru/faq";
import { FaqPage } from "@/components/info/FaqPage";

export const metadata: Metadata = { title: "Вопросы и ответы" };

// /faq — доступна без входа (раздел 3.1 ТЗ)
export default function Page() {
  return <FaqPage doc={faq} />;
}
