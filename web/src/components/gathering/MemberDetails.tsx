"use client";

import { t } from "@/i18n";
import { useGathering } from "@/lib/queries/gatherings";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";

// Левая колонка вошедшему: адрес и комментарий.
export function MemberDetails({ id }: { id: number }) {
  const query = useGathering(id);
  if (query.isPending) return <Skeleton className="h-32" />;
  if (query.isError) return <ErrorState message={query.error.message} onRetry={() => query.refetch()} />;
  const g = query.data;
  return (
    <>
      {g.moderation_status === "pending" && (
        <p className="rounded-card bg-sand-100 p-4 text-sm text-sand-800">{t("gathering.pending")}</p>
      )}
      <section className="space-y-5 rounded-card bg-surface p-6 shadow-card md:p-8">
        <div>
          <h2 className="mb-1 text-sm text-ink-muted">{t("gathering.address")}</h2>
          <p className="text-lg font-semibold">{g.place_name}</p>
          <p className="text-ink-muted">{g.address}</p>
        </div>
        {g.comment && (
          <div>
            <h2 className="mb-1 text-sm text-ink-muted">{t("gathering.comment")}</h2>
            <p className="whitespace-pre-line">{g.comment}</p>
          </div>
        )}
      </section>
    </>
  );
}
