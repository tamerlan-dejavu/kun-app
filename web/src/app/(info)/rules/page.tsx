import type { Metadata } from "next";
import { TextPage } from "@/components/info/TextPage";

export const metadata: Metadata = { title: "Правила сообщества" };

// /rules — доступна без входа. TODO: текст (согласовать с юристом).
export default function Page() {
  return <TextPage />;
}
