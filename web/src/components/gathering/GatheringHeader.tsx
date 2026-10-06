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
    <section className="rounded-card bg-surface p-5 shadow-card">
      <Badge tone="brand">
        <span aria-hidden>{g.category.emoji}</span> {g.category.name}
      </Badge>
      <h1 className="mb-4 mt-3 text-2xl leading-tight">{g.title}</h1>
      <p className="mb-1.5 flex items-center gap-2">
        <Icon name="calendar" className="h-5 w-5 text-brand" />
        {formatStartsAt(g.starts_at)}
      </p>
      {g.district && (
        <p className="mb-4 flex items-center gap-2">
          <Icon name="pin" className="h-5 w-5 text-brand" />
          {g.district}
        </p>
      )}
      <SeatsMeter count={g.participants_count} seats={g.seats} />
      {note && (
        <p className="mt-4 rounded-button bg-line/60 px-3 py-2 text-sm font-semibold">{t(note)}</p>
      )}
    </section>
  );
}
