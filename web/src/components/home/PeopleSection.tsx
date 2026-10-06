import Link from "next/link";
import { t } from "@/i18n";
import { photos } from "@/content/photos";
import type { CitySnapshot } from "@/lib/api/city";
import { CityPhoto } from "@/components/city/CityPhoto";
import { SectionHead } from "@/components/city/SectionHead";
import { Container } from "@/components/layout/Container";

const hhmm = (iso: string) =>
  new Intl.DateTimeFormat("ru-RU", { timeZone: "Asia/Almaty", weekday: "short", hour: "2-digit", minute: "2-digit" }).format(new Date(iso));

// 03 — Люди: анонимно (имена и фото — после входа), карточки со смещением как стопка.
export function PeopleSection({ people }: { people: CitySnapshot["people"] }) {
  return (
    <section id="people" className="scroll-mt-20 py-16 md:py-24">
      <Container className="grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <SectionHead no="03" size="lg" kicker={t("home.peopleKicker")} title={t("home.peopleTitle")}>
            {t("home.peopleLead")}
          </SectionHead>
          <CityPhoto slot={photos.people} className="hidden lg:block" />
        </div>
        <div className="lg:col-span-7 lg:pt-24">
          {people.length === 0 ? (
            <p className="card p-6 text-ink-muted">{t("home.peopleEmpty")}</p>
          ) : (
            <ul className="space-y-5">
              {people.map((p, i) => (
                <li key={p.slug} style={{ marginLeft: `${(i % 3) * 1.5}rem` }}>
                  <Link href={`/g/${p.slug}`} className="card-link grid grid-cols-[auto_1fr] gap-x-5 gap-y-3 p-5">
                    <span className="row-span-2 flex h-14 w-14 items-center justify-center border-2 border-ink bg-brand text-2xl" aria-hidden>
                      {p.category.emoji}
                    </span>
                    <div className="min-w-0">
                      <p className="meta mb-1 font-bold text-brand-700">{t("home.peopleFree", { n: p.free_seats })}</p>
                      <p className="truncate text-lg font-bold">{p.title}</p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="meta mr-2">{hhmm(p.starts_at)} · {p.district}</span>
                      {p.interests.map((i) => (
                        <span key={i} className="meta border-[1.5px] border-ink px-1.5 py-0.5">
                          {i}
                        </span>
                      ))}
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </Container>
    </section>
  );
}
