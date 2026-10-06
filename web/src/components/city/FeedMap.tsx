"use client";

import { t } from "@/i18n";
import { useFeed } from "@/lib/queries/gatherings";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";
import { GatheringCard } from "@/components/gathering/GatheringCard";
import { CityMap } from "./CityMap";

// /map для вошедших: точные координаты открытых сборов + список рядом.
export function FeedMap() {
  const feed = useFeed({});
  if (feed.isPending) return <Skeleton className="h-[480px]" />;
  if (feed.isError) return <ErrorState message={feed.error.message} onRetry={() => feed.refetch()} />;
  const items = feed.data.pages.flatMap((p) => p.results);
  const points = items.map((g) => ({ slug: g.slug, title: g.title, lat: g.lat, lng: g.lng }));

  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:items-start">
      <figure className="card overflow-hidden p-0">
        <CityMap points={points} label={t("home.mapLabel")} />
        <figcaption className="meta border-t-2 border-ink px-4 py-3">{t("home.mapCaption")}</figcaption>
      </figure>
      <ul className="space-y-5">
        {items.map((g) => (
          <li key={g.id}>
            <GatheringCard g={g} />
          </li>
        ))}
      </ul>
    </div>
  );
}
