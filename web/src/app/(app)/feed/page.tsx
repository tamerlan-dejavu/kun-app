import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { FeedList } from "@/components/gathering/FeedList";

export const metadata: Metadata = { title: "Лента" };

// /feed — лента сборов (раздел 3.3 ТЗ)
export default function FeedPage() {
  return (
    <>
      <PageTitle title={t("feed.title")} />
      <FeedList />
    </>
  );
}
