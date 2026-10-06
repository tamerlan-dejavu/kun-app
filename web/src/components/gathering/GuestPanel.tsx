import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { ShareButton } from "./ShareButton";

// Гостю: без имён, фото и точного адреса (раздел 3.1 ТЗ).
export function GuestPanel({ slug, title }: { slug: string; title: string }) {
  return (
    <section className="card space-y-3 p-6">
      <p className="text-ink-muted">{t("gathering.guestHidden")}</p>
      <ButtonLink href={`/login?next=/g/${slug}`} block>
        {t("gathering.loginToJoin")}
      </ButtonLink>
      <ShareButton slug={slug} title={title} />
    </section>
  );
}
