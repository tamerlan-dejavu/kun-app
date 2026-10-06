import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";

export function Hero() {
  return (
    <section className="relative overflow-hidden px-5 pb-10 pt-14">
      {/* Место для маскота (ещё не выбран) */}
      <div aria-hidden className="absolute -right-16 -top-16 h-64 w-64 rounded-full bg-brand-200" />
      <div aria-hidden className="absolute -right-4 top-24 h-24 w-24 rounded-full bg-brand" />
      <div className="relative">
        <p className="mb-6 font-heading text-2xl text-brand-700">KUN</p>
        <h1 className="mb-4 text-4xl leading-tight">{t("landing.title")}</h1>
        <p className="mb-8 max-w-sm text-lg text-ink-muted">{t("landing.lead")}</p>
        <ButtonLink href="/feed" block>
          {t("common.start")}
        </ButtonLink>
      </div>
    </section>
  );
}
