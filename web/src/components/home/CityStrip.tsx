import { t } from "@/i18n";
import type { CitySnapshot } from "@/lib/api/city";

// Чёрная полоса: цифры дня. Статичная — без бесконечной анимации бегущей строки.
export function CityStrip({ city }: { city: CitySnapshot | null }) {
  const date = new Intl.DateTimeFormat("ru-RU", { timeZone: "Asia/Almaty", day: "2-digit", month: "2-digit", year: "numeric" })
    .format(new Date())
    .replaceAll(".", " / ");
  return (
    <div className="border-b-2 border-ink bg-ink text-canvas">
      <div className="meta mx-auto flex max-w-6xl flex-wrap items-center gap-x-8 gap-y-2 px-5 py-4 md:px-8">
        <span className="text-brand">■ {t("home.strip")}</span>
        <span>{date}</span>
        {city && <span>{t("home.stripToday", { n: city.today_count })}</span>}
        {city && <span>{t("home.stripOpen", { n: city.open_count })}</span>}
        <span className="ml-auto hidden md:inline">{t("home.coords")}</span>
      </div>
    </div>
  );
}
