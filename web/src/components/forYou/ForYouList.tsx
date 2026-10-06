"use client";

import clsx from "clsx";
import { useState } from "react";
import { t } from "@/i18n";
import { useForYou } from "@/lib/queries/forYou";
import { useMe } from "@/lib/queries/me";
import { ButtonLink } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { Icon } from "@/components/ui/Icon";
import { SkeletonList } from "@/components/ui/Skeleton";
import { ForYouCard } from "./ForYouCard";

// /for-you: первая рекомендация — крупно, остальные — сеткой.
export function ForYouList() {
  const [point, setPoint] = useState<{ lat: number; lng: number } | null>(null);
  const query = useForYou(point);
  const me = useMe();

  const toggleNear = () => {
    if (point) return setPoint(null);
    navigator.geolocation?.getCurrentPosition(
      (pos) => setPoint({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => setPoint(null),
      { timeout: 8000 },
    );
  };

  return (
    <>
      <div className="mb-6 flex flex-wrap items-center gap-4">
        <p className="max-w-2xl text-lg text-ink-muted">{t("forYou.lead")}</p>
        <div className="ml-auto">
          <Chip selected={Boolean(point)} onClick={toggleNear}>
            <Icon name="near" className="h-4 w-4" />
            {t("forYou.near")}
          </Chip>
        </div>
      </div>

      {query.isPending ? (
        <SkeletonList count={4} className="h-56" />
      ) : query.isError ? (
        <ErrorState message={query.error.message} onRetry={() => query.refetch()} />
      ) : query.data.length === 0 ? (
        <EmptyState
          title={t("forYou.empty")}
          hint={t("forYou.emptyHint")}
          action={
            <div className="flex flex-wrap gap-3">
              {me.data && me.data.interests.length < 3 && (
                <ButtonLink href="/profile/edit">{t("forYou.toProfile")}</ButtonLink>
              )}
              <ButtonLink href="/feed" variant="secondary">
                {t("forYou.toFeed")}
              </ButtonLink>
            </div>
          }
        />
      ) : (
        <ol className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {query.data.map((item, i) => (
            <li key={item.gathering.id} className={clsx(i === 0 && "md:col-span-2")}>
              <ForYouCard item={item} index={i} large={i === 0} />
            </li>
          ))}
        </ol>
      )}
    </>
  );
}
