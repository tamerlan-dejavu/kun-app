import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { AppPreview } from "./AppPreview";
import { Container } from "./Container";

export function Hero() {
  return (
    <section className="py-12 md:py-20">
      <Container className="grid items-center gap-12 md:grid-cols-2 md:gap-16">
        <div>
          <p className="mb-5 inline-flex rounded-chip bg-sand-100 px-3 py-1.5 text-sm font-semibold text-sand-800">
            {t("landing.eyebrow")}
          </p>
          <h1 className="mb-5 text-4xl leading-[1.1] md:text-6xl">{t("landing.title")}</h1>
          <p className="mb-8 max-w-xl text-lg text-ink-muted md:text-xl">{t("landing.lead")}</p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <ButtonLink href="/feed" className="px-8 text-lg">
              {t("common.start")}
            </ButtonLink>
            <ButtonLink href="#how" variant="secondary" className="px-8 text-lg">
              {t("landing.ctaSecondary")}
            </ButtonLink>
          </div>
          <p className="mt-6 max-w-md text-sm text-ink-muted">{t("landing.proof")}</p>
        </div>
        <AppPreview />
      </Container>
    </section>
  );
}
