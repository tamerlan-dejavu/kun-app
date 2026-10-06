import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageHeader } from "@/components/layout/PageHeader";
import { MyGatheringsList } from "@/components/gathering/MyGatheringsList";

export const metadata: Metadata = { title: "Мои сборы" };

// /my — мои сборы: будущие и прошедшие
export default function MyGatheringsPage() {
  return (
    <>
      <PageHeader title={t("my.title")} />
      <div className="px-4">
        <MyGatheringsList />
      </div>
    </>
  );
}
