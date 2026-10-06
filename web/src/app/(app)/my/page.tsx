import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { MyGatheringsList } from "@/components/gathering/MyGatheringsList";

export const metadata: Metadata = { title: "Мои сборы" };

// /my — мои сборы: будущие и прошедшие
export default function MyGatheringsPage() {
  return (
    <>
      <PageTitle title={t("my.title")} />
      <MyGatheringsList />
    </>
  );
}
