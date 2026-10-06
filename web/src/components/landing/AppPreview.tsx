import { landing, t } from "@/i18n";
import { Badge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import { SeatsMeter } from "@/components/gathering/SeatsMeter";

// Иллюстрация ленты на первом экране: пример карточек, не реальные сборы.
export function AppPreview() {
  const cards = landing().preview;
  return (
    <figure
      aria-label={t("landing.previewLabel")}
      className="relative overflow-hidden rounded-[32px] bg-brand p-5 md:p-8"
    >
      <div aria-hidden className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-sand/40" />
      <div aria-hidden className="absolute -bottom-24 -left-16 h-56 w-56 rounded-full bg-brand-700/60" />
      <p className="relative mb-4 font-heading text-lg text-white">{t("landing.previewTitle")}</p>
      <ul className="relative space-y-3">
        {cards.map((c, i) => (
          <li
            key={c.title}
            className="rounded-card bg-surface p-4 shadow-card"
            style={{ transform: `translateX(${i % 2 ? 12 : 0}px)` }}
          >
            <Badge tone="sand">
              <span aria-hidden>{c.emoji}</span> {c.category}
            </Badge>
            <p className="mb-2 mt-2 font-heading text-base">{c.title}</p>
            <p className="mb-3 flex items-center gap-1.5 text-sm text-ink-muted">
              <Icon name="calendar" className="h-4 w-4" />
              {c.when}
              <span aria-hidden>·</span>
              <Icon name="pin" className="h-4 w-4" />
              {c.where}
            </p>
            <SeatsMeter count={c.going} seats={c.seats} />
          </li>
        ))}
      </ul>
    </figure>
  );
}
