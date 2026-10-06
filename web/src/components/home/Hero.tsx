import { t } from "@/i18n";
import { photos } from "@/content/photos";
import { ButtonLink } from "@/components/ui/Button";
import { CityPhoto } from "@/components/city/CityPhoto";
import { Container } from "@/components/layout/Container";

// Editorial-первый экран: огромная типографика слева, фото справа выходит за нижний край.
export function Hero() {
  return (
    <section className="relative overflow-x-clip border-b-2 border-ink">
      <Container className="grid gap-10 pb-0 pt-10 md:grid-cols-12 md:pt-16">
        <div className="relative z-10 md:col-span-8">
          <p className="meta mb-6 flex items-center gap-3">
            <span className="inline-block h-3 w-3 bg-brand" aria-hidden />
            {t("home.kicker")}
          </p>
          <h1 className="text-[9vw] uppercase leading-[0.86] tracking-[-0.04em] md:text-[clamp(3rem,7.2vw,7rem)]">
            <span className="block">{t("home.title1")}</span>
            <span className="block text-brand md:whitespace-nowrap">{t("home.title2")}</span>
            <span className="block">{t("home.title3")}</span>
            <span className="block">{t("home.title4")}</span>
          </h1>
          <div className="mt-10 grid gap-6 pb-12 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-end md:pb-20">
            <p className="max-w-md border-l-[3px] border-brand pl-4 text-lg font-medium">{t("home.lead")}</p>
            <div className="flex flex-wrap gap-3">
              <ButtonLink href="/feed" className="px-6 text-base">
                {t("home.cta")}
              </ButtonLink>
              <ButtonLink href="#how" variant="secondary">
                {t("home.ctaHow")}
              </ButtonLink>
            </div>
          </div>
        </div>

        <div className="relative md:col-span-4">
          {/* Индекс раздела — графический элемент вне сетки */}
          <div className="meta absolute -left-4 top-0 z-20 hidden -translate-x-full flex-col gap-1 border-2 border-ink bg-canvas p-3 lg:flex">
            <span className="text-lg font-bold">{t("home.index")}</span>
            <span>{t("home.indexCity")}</span>
            <span className="text-brand-700">{t("home.indexToday")}</span>
          </div>
          <div className="md:-mb-24 md:mt-28 md:translate-x-6">
            <CityPhoto slot={photos.hero} priority />
          </div>
          <p className="meta absolute -right-2 top-8 hidden origin-top-right -rotate-90 lg:block">
            {t("home.coords")}
          </p>
        </div>
      </Container>
    </section>
  );
}
