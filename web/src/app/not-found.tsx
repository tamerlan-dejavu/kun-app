import { t } from "@/i18n";
import { SiteShell } from "@/components/layout/SiteShell";
import { ButtonLink } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";

export default function NotFound() {
  return (
    <SiteShell>
      <EmptyState
        title={t("common.notFound")}
        action={<ButtonLink href="/">{t("common.home")}</ButtonLink>}
      />
    </SiteShell>
  );
}
