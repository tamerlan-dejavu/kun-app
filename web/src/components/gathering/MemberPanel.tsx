"use client";

import Link from "next/link";
import { t } from "@/i18n";
import { useGathering, useParticipation } from "@/lib/queries/gatherings";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Button, buttonClass } from "@/components/ui/Button";
import { ErrorState } from "@/components/ui/ErrorState";
import { Icon } from "@/components/ui/Icon";
import { Skeleton } from "@/components/ui/Skeleton";
import { ShareButton } from "./ShareButton";

// Вошедшему: адрес, участники, «Иду» / «Не смогу», чат.
export function MemberPanel({ id }: { id: number }) {
  const query = useGathering(id);
  const participation = useParticipation(id);

  if (query.isPending) {
    return (
      <div className="mt-4 space-y-3" role="status" aria-label={t("common.loading")}>
        <Skeleton className="h-20" />
        <Skeleton className="h-40" />
      </div>
    );
  }
  if (query.isError) {
    return <ErrorState message={query.error.message} onRetry={() => query.refetch()} />;
  }

  const g = query.data;
  const open = g.status === "open";

  const leave = () => {
    if (window.confirm(t("gathering.leaveConfirm"))) participation.mutate("leave");
  };

  return (
    <div className="mt-4 space-y-4">
      {g.moderation_status === "pending" && (
        <p className="rounded-card bg-brand-100 p-4 text-sm text-brand-800">{t("gathering.pending")}</p>
      )}

      <section className="space-y-3 rounded-card bg-surface p-5 shadow-card">
        <div>
          <h2 className="mb-1 text-sm text-ink-muted">{t("gathering.address")}</h2>
          <p className="font-semibold">{g.place_name}</p>
          <p className="text-ink-muted">{g.address}</p>
        </div>
        {g.comment && (
          <div>
            <h2 className="mb-1 text-sm text-ink-muted">{t("gathering.comment")}</h2>
            <p className="whitespace-pre-line">{g.comment}</p>
          </div>
        )}
      </section>

      <section className="rounded-card bg-surface p-5 shadow-card">
        <h2 className="mb-3 text-base">{t("gathering.participants")}</h2>
        <ul className="space-y-3">
          {g.participants.map((p) => (
            <li key={p.user.id} className="flex items-center gap-3">
              <Avatar name={p.user.name} photo={p.user.photo} />
              <span className="font-semibold">{p.user.name}</span>
              {p.user.university && <span className="text-sm text-ink-muted">{p.user.university}</span>}
              {p.is_creator && (
                <span className="ml-auto">
                  <Badge tone="brand">{t("gathering.creator")}</Badge>
                </span>
              )}
            </li>
          ))}
        </ul>
      </section>

      <div className="space-y-3">
        {participation.isError && (
          <p role="alert" className="rounded-button bg-red-50 px-4 py-3 text-sm text-danger">
            {participation.error.message}
          </p>
        )}
        {g.is_participant ? (
          <>
            <Link href={`/g/${g.slug}/chat`} className={buttonClass("primary", true)}>
              <Icon name="chat" />
              {t("gathering.chat")}
            </Link>
            {open || g.status === "full" ? (
              <Button variant="danger" block onClick={leave} disabled={participation.isPending}>
                {t("gathering.leave")}
              </Button>
            ) : null}
          </>
        ) : (
          open && (
            <Button block onClick={() => participation.mutate("join")} disabled={participation.isPending}>
              {t("gathering.join")}
            </Button>
          )
        )}
        <ShareButton slug={g.slug} title={g.title} />
      </div>
    </div>
  );
}
