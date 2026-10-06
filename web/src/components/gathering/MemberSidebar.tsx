"use client";

import Link from "next/link";
import { t } from "@/i18n";
import { useGathering, useParticipation } from "@/lib/queries/gatherings";
import type { Source } from "@/lib/source";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Button, buttonClass } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { Skeleton } from "@/components/ui/Skeleton";
import { ShareButton } from "./ShareButton";

// Правая колонка вошедшему: «Иду» / «Не смогу», чат, участники, «Поделиться».
export function MemberSidebar({ id, source }: { id: number; source?: Source }) {
  const query = useGathering(id);
  const participation = useParticipation(id, source);

  if (query.isPending) return <Skeleton className="h-64" />;
  if (query.isError) return null; // ошибку уже показала левая колонка

  const g = query.data;
  const active = g.status === "open" || g.status === "full";
  const started = new Date(g.starts_at) <= new Date() && g.status !== "cancelled";
  const leave = () => {
    if (window.confirm(t("gathering.leaveConfirm"))) participation.mutate("leave");
  };

  return (
    <div className="space-y-4">
      <section className="card space-y-3 p-6">
        {participation.isError && (
          <p role="alert" className="rounded-button bg-red-50 px-4 py-3 text-sm text-danger">
            {participation.error.message}
          </p>
        )}
        {g.is_participant ? (
          <>
            <p className="flex items-center gap-2 font-semibold text-success">
              <Icon name="check" />
              {t("gathering.joined")}
            </p>
            {started && (
              <Link href={`/g/${g.slug}/after`} className={buttonClass("primary", true)}>
                {t("gathering.howWasIt")}
              </Link>
            )}
            <Link
              href={`/g/${g.slug}/chat`}
              className={buttonClass(started ? "secondary" : "primary", true)}
            >
              <Icon name="chat" />
              {t("gathering.chat")}
            </Link>
            {active && !started && (
              <Button variant="danger" block onClick={leave} disabled={participation.isPending}>
                {t("gathering.leave")}
              </Button>
            )}
          </>
        ) : (
          g.status === "open" && (
            <Button block onClick={() => participation.mutate("join")} disabled={participation.isPending}>
              {t("gathering.join")}
            </Button>
          )
        )}
        <ShareButton slug={g.slug} title={g.title} />
      </section>

      <section className="card p-6">
        <h2 className="mb-4 text-base">{t("gathering.participants")}</h2>
        <ul className="space-y-3">
          {g.participants.map((p) => (
            <li key={p.user.id} className="flex items-center gap-3">
              <Link href={`/u/${p.user.id}`} className="flex min-w-0 items-center gap-3 rounded-button hover:opacity-80">
                <Avatar name={p.user.name} photo={p.user.photo} />
                <div className="min-w-0">
                  <p className="truncate font-semibold">{p.user.name}</p>
                  {p.user.university && <p className="text-sm text-ink-muted">{p.user.university}</p>}
                </div>
              </Link>
              {p.is_creator && (
                <span className="ml-auto">
                  <Badge tone="brand">{t("gathering.creator")}</Badge>
                </span>
              )}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
