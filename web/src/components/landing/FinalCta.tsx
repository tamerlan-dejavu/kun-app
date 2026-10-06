import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { Container } from "./Container";

export function FinalCta() {
  return (
    <section className="py-14 md:py-20">
      <Container>
        <div className="flex flex-col items-start gap-6 rounded-[32px] bg-surface p-8 shadow-card md:flex-row md:items-center md:justify-between md:p-12">
          <div>
            <h2 className="mb-2 text-2xl md:text-3xl">{t("landing.finalTitle")}</h2>
            <p className="text-ink-muted">{t("landing.finalText")}</p>
          </div>
          <ButtonLink href="/feed" className="shrink-0 px-8 text-lg">
            {t("common.start")}
          </ButtonLink>
        </div>
      </Container>
    </section>
  );
}
