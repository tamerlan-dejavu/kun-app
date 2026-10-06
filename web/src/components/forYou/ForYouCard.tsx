import clsx from "clsx";
import Link from "next/link";
import type { components } from "@/lib/api/schema";
import { formatStartsAt } from "@/lib/datetime";
import { gatheringHref } from "@/lib/source";
import { SeatsMeter } from "@/components/gathering/SeatsMeter";
import { reasonText } from "./reasonText";

type Item = components["schemas"]["ForYouItem"];

// Карточка подбора: сверху — «почему», это главное отличие от ленты.
export function ForYouCard({ item, index, large }: { item: Item; index: number; large?: boolean }) {
  const g = item.gathering;
  return (
    <Link href={gatheringHref(g.slug, "for_you")} className="card-link flex h-full flex-col">
      <p className="meta flex items-start gap-2 border-b-2 border-ink bg-brand px-4 py-2.5 font-bold">
        <span aria-hidden>→</span>
        <span>{reasonText(item.reason)}</span>
      </p>
      <div className="flex flex-1 flex-col p-4">
        <div className="mb-3 flex items-start justify-between gap-3">
          <span className="meta font-bold">
            <span aria-hidden>{g.category.emoji}</span> {g.category.name}
          </span>
          <span aria-hidden className="font-mono text-sm font-bold text-ink-muted">
            {String(index + 1).padStart(2, "0")}
          </span>
        </div>
        <h2 className={clsx("mb-4 leading-tight tracking-tight", large ? "text-3xl md:text-4xl" : "text-xl")}>
          {g.title}
        </h2>
        <dl className="meta mb-5 space-y-1 text-ink-muted">
          <div>
            <dt className="sr-only">Когда</dt>
            <dd className="font-bold text-ink">{formatStartsAt(g.starts_at)}</dd>
          </div>
          <div>
            <dt className="sr-only">Где</dt>
            <dd>{[g.place_name, g.district].filter(Boolean).join(" · ")}</dd>
          </div>
        </dl>
        <div className="mt-auto">
          <SeatsMeter count={g.participants_count} seats={g.seats} />
        </div>
      </div>
    </Link>
  );
}
