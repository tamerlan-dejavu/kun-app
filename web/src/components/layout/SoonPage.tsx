import { t } from "@/i18n";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageTitle } from "./PageTitle";

// Разделы, которые ещё в работе (создание сбора, профиль, настройки).
export function SoonPage({ title }: { title: string }) {
  return (
    <>
      <PageTitle title={title} />
      <EmptyState title={t("soon.title")} hint={t("soon.text")} />
    </>
  );
}
