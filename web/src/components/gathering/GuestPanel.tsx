import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { ShareButton } from "./ShareButton";

// Гостю: без имён, фото и точного адреса (раздел 3.1 ТЗ).
export function GuestPanel({ slug, title }: { slug: string; title: string }) {
  return (
    <section className="space-y-3 rounded-card bg-surface p-6 shadow-card">
      <p className="text-ink-muted">{t("gathering.guestHidden")}</p>
      <ButtonLink href={`/login?next=/g/${slug}`} block>
        {t("gathering.loginToJoin")}
      </ButtonLink>
      <ShareButton slug={slug} title={title} />
    </section>
  );
}
