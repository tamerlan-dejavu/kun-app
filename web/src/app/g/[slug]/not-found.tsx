import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";

export default function GatheringNotFound() {
  return (
    <EmptyState
      title={t("gathering.notFound")}
      hint={t("gathering.notFoundHint")}
      action={<ButtonLink href="/feed">{t("my.toFeed")}</ButtonLink>}
    />
  );
}
