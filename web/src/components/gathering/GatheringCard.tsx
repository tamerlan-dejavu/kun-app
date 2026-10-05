import Link from "next/link";
import { t } from "@/i18n";
import type { GatheringCard as Card } from "@/lib/api/types";
import { formatDistance, formatStartsAt } from "@/lib/datetime";
import { Badge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import { SeatsMeter } from "./SeatsMeter";

// Карточка в ленте: категория, название, время, район, «идут N из M» (раздел 3.3 ТЗ).
export function GatheringCard({ g }: { g: Card }) {
  const distance = formatDistance(g.distance_m);
  return (
    <Link
      href={`/g/${g.slug}`}
      className="block rounded-card bg-surface p-4 shadow-card transition-transform active:scale-[0.99]"
    >
      <div className="mb-2 flex items-center justify-between gap-2">
        <Badge tone="brand">
          <span aria-hidden>{g.category.emoji}</span> {g.category.name}
        </Badge>
        {g.is_participant && (
          <Badge tone="success">
            <Icon name="check" className="h-3.5 w-3.5" />
            {t("gathering.joined")}
          </Badge>
        )}
      </div>
      <h2 className="mb-2 text-base leading-snug">{g.title}</h2>
      <p className="flex items-center gap-1.5 text-sm text-ink-muted">
        <Icon name="calendar" className="h-4 w-4" />
        {formatStartsAt(g.starts_at)}
      </p>
      <p className="mb-3 flex items-center gap-1.5 text-sm text-ink-muted">
        <Icon name="pin" className="h-4 w-4" />
        {[g.place_name, g.district].filter(Boolean).join(" · ")}
        {distance && <span className="ml-auto shrink-0">{distance}</span>}
      </p>
      <SeatsMeter count={g.participants_count} seats={g.seats} />
    </Link>
  );
}
