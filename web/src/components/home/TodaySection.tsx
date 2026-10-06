import Link from "next/link";
import { t } from "@/i18n";
import type { CitySnapshot } from "@/lib/api/city";
import { ButtonLink } from "@/components/ui/Button";
import { Container } from "@/components/layout/Container";

const tz = "Asia/Almaty";
const hhmm = (iso: string) => new Intl.DateTimeFormat("ru-RU", { timeZone: tz, hour: "2-digit", minute: "2-digit" }).format(new Date(iso));
const ddmm = (iso: string) => new Intl.DateTimeFormat("ru-RU", { timeZone: tz, day: "2-digit", month: "2-digit" }).format(new Date(iso));

// 02 — Сегодня: огромная дата и расписание с горизонтальными линиями.
export function TodaySection({ city }: { city: CitySnapshot | null }) {
  const [y, m, d] = (city?.date ?? new Date().toISOString().slice(0, 10)).split("-");
  const rows = city?.schedule ?? [];
  return (
    <section id="today" className="scroll-mt-20 border-y-2 border-ink bg-surface py-16 md:py-24">
      <Container>
        <div className="mb-10 flex flex-col gap-4 md:mb-14 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="section-no mb-4">02 <span className="text-ink-muted">— {t("home.todayKicker")}</span></p>
            <p className="whitespace-nowrap font-mono text-[clamp(2.25rem,6.5vw,5.5rem)] font-bold leading-none tracking-tighter">
              {d} / {m} / {y}
            </p>
          </div>
          <h2 className="max-w-[12ch] text-3xl uppercase leading-[0.95] md:text-right md:text-5xl">
            {city?.is_today === false && rows.length ? t("home.nextTitle") : t("home.todayTitle")}
          </h2>
        </div>

        {rows.length === 0 ? (
          <div className="flex flex-col items-start gap-4 border-t-2 border-ink pt-6">
            <p className="text-lg">{t("home.todayEmpty")}</p>
            <ButtonLink href="/new">{t("nav.create")}</ButtonLink>
          </div>
        ) : (
          <ol className="border-t-2 border-ink">
            {rows.map((g) => (
              <li key={g.slug} className="border-b-2 border-ink">
                <Link
                  href={`/g/${g.slug}`}
                  className="group grid grid-cols-[auto_1fr] items-baseline gap-x-6 gap-y-1 py-5 transition-colors hover:bg-brand md:grid-cols-[7rem_1fr_12rem_6rem] md:px-3"
                >
                  <span className="font-mono text-2xl font-bold md:text-3xl">
                    {city?.is_today ? hhmm(g.starts_at) : `${ddmm(g.starts_at)}`}
                  </span>
                  <span className="text-xl font-bold leading-tight transition-transform group-hover:translate-x-2 md:text-2xl">
                    {g.title}
                  </span>
                  <span className="meta col-start-2 md:col-start-auto">
                    {g.category.emoji} {g.category.name} · {g.district}
                  </span>
                  <span className="meta col-start-2 font-bold md:col-start-auto md:text-right">
                    {t("home.todaySeats", { n: g.participants_count, m: g.seats })}
                  </span>
                </Link>
              </li>
            ))}
          </ol>
        )}
      </Container>
    </section>
  );
}
