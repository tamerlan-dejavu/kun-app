import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { Container } from "@/components/layout/Container";

export function FinalSection() {
  return (
    <section className="border-t-2 border-ink bg-brand py-16 md:py-24">
      <Container className="flex flex-col items-start gap-8 md:flex-row md:items-end md:justify-between">
        <h2 className="max-w-[14ch] text-5xl uppercase leading-[0.9] md:text-7xl">{t("home.finalTitle")}</h2>
        <ButtonLink href="/feed" variant="dark" className="px-8 text-base">
          {t("home.finalCta")}
        </ButtonLink>
      </Container>
    </section>
  );
}
