import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageHeader } from "@/components/layout/PageHeader";
import { FeedList } from "@/components/gathering/FeedList";

export const metadata: Metadata = { title: "Лента" };

// /feed — лента сборов (раздел 3.3 ТЗ)
export default function FeedPage() {
  return (
    <>
      <PageHeader title={t("feed.title")} />
      <div className="px-4">
        <FeedList />
      </div>
    </>
  );
}
