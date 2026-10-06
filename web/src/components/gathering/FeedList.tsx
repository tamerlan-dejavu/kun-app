"use client";

import { useState } from "react";
import { t } from "@/i18n";
import { useCategories } from "@/lib/queries/catalog";
import { type FeedFilters, useFeed } from "@/lib/queries/gatherings";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { Icon } from "@/components/ui/Icon";
import { SkeletonList } from "@/components/ui/Skeleton";
import { GatheringCard } from "./GatheringCard";

const DATES = [
  { value: undefined, label: "feed.all" },
  { value: "today", label: "feed.today" },
  { value: "tomorrow", label: "feed.tomorrow" },
  { value: "week", label: "feed.week" },
] as const;

export function FeedList() {
  const [filters, setFilters] = useState<FeedFilters>({});
  const [geoDenied, setGeoDenied] = useState(false);
  const feed = useFeed(filters);
  const categories = useCategories();
  const items = feed.data?.pages.flatMap((p) => p.results) ?? [];
  const near = filters.lat !== undefined;
  const filtered = Boolean(filters.date || filters.category || near);

  const toggleNear = () => {
    if (near) return setFilters(({ lat: _lat, lng: _lng, ...rest }) => rest);
    navigator.geolocation?.getCurrentPosition(
      (pos) => {
        setGeoDenied(false);
        setFilters((f) => ({ ...f, lat: pos.coords.latitude, lng: pos.coords.longitude }));
      },
      () => setGeoDenied(true),
      { timeout: 8000 },
    );
  };

  return (
    <>
      <div
        role="group"
        aria-label={t("feed.dateFilter")}
        className="-mx-5 flex gap-2 overflow-x-auto px-5 pb-5 md:mx-0 md:flex-wrap md:overflow-visible md:px-0"
      >
        {DATES.map((d) => (
          <Chip
            key={d.label}
            selected={filters.date === d.value}
            onClick={() => setFilters((f) => ({ ...f, date: d.value }))}
          >
            {t(d.label)}
          </Chip>
        ))}
        <Chip selected={near} onClick={toggleNear}>
          <Icon name="near" className="h-4 w-4" />
          {t("feed.near")}
        </Chip>
      </div>
      {categories.data && (
        <div
          role="group"
          aria-label={t("feed.categoryFilter")}
          className="-mx-5 flex gap-2 overflow-x-auto px-5 pb-5 md:mx-0 md:flex-wrap md:overflow-visible md:px-0"
        >
          <Chip
            selected={!filters.category}
            onClick={() => setFilters((f) => ({ ...f, category: undefined }))}
          >
            {t("feed.allCategories")}
          </Chip>
          {categories.data.map((c) => (
            <Chip
              key={c.slug}
              selected={filters.category === c.slug}
              onClick={() => setFilters((f) => ({ ...f, category: c.slug }))}
            >
              <span aria-hidden>{c.emoji}</span>
              {c.name}
            </Chip>
          ))}
        </div>
      )}
      {geoDenied && (
        <p role="status" className="pb-3 text-sm text-ink-muted">
          {t("feed.nearDenied")}
        </p>
      )}

      {feed.isPending ? (
        <SkeletonList />
      ) : feed.isError ? (
        <ErrorState message={feed.error.message} onRetry={() => feed.refetch()} />
      ) : items.length === 0 ? (
        <EmptyState
          title={filtered ? t("feed.emptyFiltered") : t("feed.empty")}
          hint={filtered ? undefined : t("feed.emptyHint")}
          action={
            filtered && (
              <Button variant="secondary" onClick={() => setFilters({})}>
                {t("feed.resetFilters")}
              </Button>
            )
          }
        />
      ) : (
        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((g) => (
            <li key={g.id}>
              <GatheringCard g={g} />
            </li>
          ))}
        </ul>
      )}

      {feed.hasNextPage && (
        <Button
          variant="secondary"
          block
          className="mx-auto mt-6 max-w-sm"
          disabled={feed.isFetchingNextPage}
          onClick={() => feed.fetchNextPage()}
        >
          {feed.isFetchingNextPage ? t("common.loading") : t("common.more")}
        </Button>
      )}
    </>
  );
}
