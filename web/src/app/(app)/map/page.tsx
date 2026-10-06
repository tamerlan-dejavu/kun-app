import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { FeedMap } from "@/components/city/FeedMap";

export const metadata: Metadata = { title: "Карта" };

// /map — открытые сборы на схеме города (вошедшим — точные координаты)
export default function MapPage() {
  return (
    <>
      <PageTitle title={t("nav.map")} />
      <FeedMap />
    </>
  );
}
