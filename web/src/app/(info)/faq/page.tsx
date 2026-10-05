import type { Metadata } from "next";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Вопросы и ответы" };

// /faq — доступна без входа. TODO: текст (согласовать с юристом).
export default function Page() {
  return <TextPage />;
}
