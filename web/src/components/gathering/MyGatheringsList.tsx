"use client";

import { useState } from "react";
import { t } from "@/i18n";
import { useMyGatherings } from "@/lib/queries/gatherings";
import { Button, ButtonLink } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { SkeletonList } from "@/components/ui/Skeleton";
import { GatheringCard } from "./GatheringCard";

export function MyGatheringsList() {
  const [when, setWhen] = useState<"upcoming" | "past">("upcoming");
  const query = useMyGatherings(when);
  const items = query.data?.pages.flatMap((p) => p.results) ?? [];

  return (
    <>
      <div role="group" aria-label={t("my.title")} className="flex gap-2 pb-3">
        <Chip selected={when === "upcoming"} onClick={() => setWhen("upcoming")}>
          {t("my.upcoming")}
        </Chip>
        <Chip selected={when === "past"} onClick={() => setWhen("past")}>
          {t("my.past")}
        </Chip>
      </div>
      {query.isPending ? (
        <SkeletonList />
      ) : query.isError ? (
        <ErrorState message={query.error.message} onRetry={() => query.refetch()} />
      ) : items.length === 0 ? (
        <EmptyState
          title={when === "upcoming" ? t("my.emptyUpcoming") : t("my.emptyPast")}
          action={when === "upcoming" && <ButtonLink href="/feed">{t("my.toFeed")}</ButtonLink>}
        />
      ) : (
        <ul className="space-y-3">
          {items.map((g) => (
            <li key={g.id}>
              <GatheringCard g={g} />
            </li>
          ))}
        </ul>
      )}
      {query.hasNextPage && (
        <Button variant="secondary" block className="mt-4" onClick={() => query.fetchNextPage()}>
          {t("common.more")}
        </Button>
      )}
    </>
  );
}
