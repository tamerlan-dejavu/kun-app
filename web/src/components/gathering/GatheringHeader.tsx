import { t } from "@/i18n";
import type { GatheringPublic } from "@/lib/api/types";
import { formatStartsAt } from "@/lib/datetime";
import { Badge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import { SeatsMeter } from "./SeatsMeter";

const STATUS_NOTE = {
  full: "gathering.full",
  cancelled: "gathering.cancelled",
  finished: "gathering.finished",
} as const;

// Шапка сбора — одинаковая для гостя и участника; рендерится на сервере (SSR).
export function GatheringHeader({ g }: { g: GatheringPublic }) {
  const note = STATUS_NOTE[g.status as keyof typeof STATUS_NOTE];
  return (
    <section className="card p-5">
      <Badge tone="brand">
        <span aria-hidden>{g.category.emoji}</span> {g.category.name}
      </Badge>
      <h1 className="mb-5 mt-4 text-3xl uppercase leading-[0.95] md:text-5xl">{g.title}</h1>
      <p className="meta mb-2 flex items-center gap-2 text-sm font-bold">
        <Icon name="calendar" className="h-5 w-5 text-brand" />
        {formatStartsAt(g.starts_at)}
      </p>
      {g.district && (
        <p className="meta mb-5 flex items-center gap-2 text-sm">
          <Icon name="pin" className="h-5 w-5 text-brand" />
          {g.district}
        </p>
      )}
      <SeatsMeter count={g.participants_count} seats={g.seats} />
      {note && (
        <p className="meta mt-5 border-2 border-ink bg-ink px-3 py-2 font-bold text-canvas">{t(note)}</p>
      )}
    </section>
  );
}
