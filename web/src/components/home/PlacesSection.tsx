import clsx from "clsx";
import { t } from "@/i18n";
import { photos } from "@/content/photos";
import type { CitySnapshot } from "@/lib/api/city";
import { CityPhoto } from "@/components/city/CityPhoto";
import { SectionHead } from "@/components/city/SectionHead";
import { Container } from "@/components/layout/Container";

// 01 — Места: карточки разного размера, первая — крупная с фото.
export function PlacesSection({ places }: { places: CitySnapshot["places"] }) {
  return (
    <section id="places" className="scroll-mt-20 pb-16 pt-24 md:pb-24 md:pt-40">
      <Container>
        <SectionHead no="01" kicker={t("home.placesKicker")} title={t("home.placesTitle")}>
          {t("home.placesLead")}
        </SectionHead>
        {places.length === 0 ? (
          <p className="card p-6 text-ink-muted">{t("home.placesEmpty")}</p>
        ) : (
          <div className="grid gap-6 md:grid-cols-6">
            {places.map((p, i) => (
              <article
                key={`${p.place_name}-${p.district}`}
                className={clsx(
                  "card relative flex flex-col justify-between gap-6 p-5",
                  i === 0 && "md:col-span-4 md:row-span-2",
                  i === 1 && "bg-brand md:col-span-2",
                  i === 2 && "md:col-span-2",
                  i > 2 && "md:col-span-3",
                )}
              >
                <span aria-hidden className="absolute -top-4 right-4 border-2 border-ink bg-canvas px-2 font-mono text-sm font-bold">
                  {String(i + 1).padStart(2, "0")}
                </span>
                {i === 0 && <CityPhoto slot={photos.places1} className="shadow-none" />}
                {i === 2 && <CityPhoto slot={photos.places2} className="shadow-none" />}
                <div>
                  <p className="meta mb-2">{p.district || "—"}</p>
                  <h3 className={clsx("leading-tight", i === 0 ? "text-3xl md:text-5xl" : "text-xl")}>{p.place_name}</h3>
                </div>
                <p className="meta flex gap-4">
                  <span>{t("home.placesCount", { n: p.gatherings })}</span>
                  {p.upcoming > 0 && <span className="font-bold">{t("home.placesUpcoming", { n: p.upcoming })}</span>}
                </p>
              </article>
            ))}
          </div>
        )}
      </Container>
    </section>
  );
}
