import Link from "next/link";
import { t } from "@/i18n";
import type { GatheringCard as Card } from "@/lib/api/types";
import { formatDistance, formatStartsAt } from "@/lib/datetime";
import { gatheringHref, type Source } from "@/lib/source";
import { Badge } from "@/components/ui/Badge";
import { SeatsMeter } from "./SeatsMeter";

// Карточка в ленте: категория, название, время, район, «идут N из M» (раздел 3.3 ТЗ).
export function GatheringCard({ g, src }: { g: Card; src?: Source }) {
  const distance = formatDistance(g.distance_m);
  return (
    <Link href={gatheringHref(g.slug, src)} className="card-link flex h-full flex-col">
      <div className="flex items-center justify-between gap-2 border-b-2 border-ink px-4 py-2.5">
        <span className="meta font-bold">
          <span aria-hidden>{g.category.emoji}</span> {g.category.name}
        </span>
        {g.is_participant && <Badge tone="dark">{t("gathering.joined")}</Badge>}
      </div>
      <div className="flex flex-1 flex-col p-4">
        <h2 className="mb-4 text-xl leading-tight tracking-tight">{g.title}</h2>
        <dl className="meta mb-5 space-y-1 text-ink-muted">
          <div className="flex gap-2">
            <dt className="sr-only">Когда</dt>
            <dd className="font-bold text-ink">{formatStartsAt(g.starts_at)}</dd>
          </div>
          <div className="flex gap-2">
            <dt className="sr-only">Где</dt>
            <dd>{[g.place_name, g.district].filter(Boolean).join(" · ")}</dd>
            {distance && <dd className="ml-auto shrink-0">{distance}</dd>}
          </div>
        </dl>
        <div className="mt-auto">
          <SeatsMeter count={g.participants_count} seats={g.seats} />
        </div>
      </div>
    </Link>
  );
}
