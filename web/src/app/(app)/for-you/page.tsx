import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { ForYouList } from "@/components/forYou/ForYouList";

export const metadata: Metadata = { title: "Для тебя" };

// /for-you — персональный подбор (ТЗ, «Персональный подбор»)
export default function ForYouPage() {
  return (
    <>
      <PageTitle title={t("forYou.title")} />
      <ForYouList />
    </>
  );
}
