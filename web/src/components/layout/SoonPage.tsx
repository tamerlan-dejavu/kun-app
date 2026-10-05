import { t } from "@/i18n";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "./PageHeader";

// Разделы, которые ещё в работе (создание сбора, профиль, настройки).
export function SoonPage({ title }: { title: string }) {
  return (
    <>
      <PageHeader title={title} />
      <EmptyState title={t("soon.title")} hint={t("soon.text")} />
    </>
  );
}
