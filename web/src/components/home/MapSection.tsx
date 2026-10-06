import { t } from "@/i18n";
import type { CitySnapshot } from "@/lib/api/city";
import { CityMap } from "@/components/city/CityMap";
import { SectionHead } from "@/components/city/SectionHead";
import { Container } from "@/components/layout/Container";

// 04 — Карта: своя схема города, а не встроенные Google Maps.
export function MapSection({ points }: { points: CitySnapshot["points"] }) {
  return (
    <section id="map" className="scroll-mt-20 border-t-2 border-ink bg-sand-50 py-16 md:py-24">
      <Container>
        <SectionHead no="04" kicker={t("home.mapKicker")} title={t("home.mapTitle")}>
          {t("home.mapLead")}
        </SectionHead>
        <figure className="card overflow-hidden p-0 md:-mx-6 lg:-mx-12">
          <CityMap points={points} label={t("home.mapLabel")} />
          <figcaption className="meta flex justify-between border-t-2 border-ink px-4 py-3">
            <span>{t("home.mapCaption")}</span>
            <span>{t("home.coords")}</span>
          </figcaption>
        </figure>
      </Container>
    </section>
  );
}
