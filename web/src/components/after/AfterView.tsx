"use client";

import { useState } from "react";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { useGathering } from "@/lib/queries/gatherings";
import { type RatingValue, useAfterMeeting } from "@/lib/queries/after";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ErrorState } from "@/components/ui/ErrorState";
import { Icon } from "@/components/ui/Icon";
import { Skeleton } from "@/components/ui/Skeleton";

// /g/<slug>/after: «Я пришёл» (до +12 ч) и оценки участников (до +48 ч), раздел 3.6 ТЗ.
export function AfterView({ id }: { id: number }) {
  const me = useMe();
  const query = useGathering(id);
  const { attend, rate } = useAfterMeeting(id);
  const [draft, setDraft] = useState<Record<number, RatingValue>>({});

  if (query.isPending || me.isPending) return <Skeleton className="h-64" />;
  if (query.isError) return <ErrorState message={query.error.message} onRetry={() => query.refetch()} />;

  const g = query.data;
  const note = (text: string) => <p className="card p-6">{text}</p>;
  if (!g.is_participant) return note(t("after.notParticipant"));
  if (g.status === "cancelled") return note(t("after.cancelled"));
  if (new Date(g.starts_at) > new Date()) return note(t("after.notStarted"));

  const others = g.participants.filter((p) => p.user.id !== me.data?.id);
  const saved = (g.my_ratings ?? {}) as Record<string, RatingValue>;
  const value = (userId: number) => draft[userId] ?? saved[String(userId)];
  const changed = Object.keys(draft).length > 0;

  return (
    <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
      <section className="card space-y-4 p-6 md:p-8">
        <h2 className="text-xl">{t("after.attendTitle")}</h2>
        <p className="text-ink-muted">{t("after.attendHint")}</p>
        {g.attended ? (
          <p className="flex items-center gap-2 font-semibold text-success">
            <Icon name="check" />
            {t("after.attended")}
          </p>
        ) : (
          <Button block onClick={() => attend.mutate()} disabled={attend.isPending}>
            {t("after.iCame")}
          </Button>
        )}
        {attend.isError && (
          <p role="alert" className="text-sm text-danger">
            {attend.error.message}
          </p>
        )}
      </section>

      <section className="card space-y-4 p-6 md:p-8">
        <h2 className="text-xl">{t("after.rateTitle")}</h2>
        <p className="text-ink-muted">{t("after.rateHint")}</p>
        {others.length === 0 ? (
          <p>{t("after.nobody")}</p>
        ) : (
          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              rate.mutate(draft, { onSuccess: () => setDraft({}) });
            }}
          >
            <ul className="space-y-4">
              {others.map((p) => (
                <li key={p.user.id} className="space-y-2">
                  <p id={`rate-${p.user.id}`} className="flex items-center gap-3 font-semibold">
                    <Avatar name={p.user.name} photo={p.user.photo} size="sm" />
                    {p.user.name}
                  </p>
                  <div role="group" aria-labelledby={`rate-${p.user.id}`} className="flex flex-wrap gap-2">
                    {(["ok", "no_show"] as const).map((v) => (
                      <Chip
                        key={v}
                        selected={value(p.user.id) === v}
                        onClick={() => setDraft((d) => ({ ...d, [p.user.id]: v }))}
                      >
                        {t(v === "ok" ? "after.ok" : "after.noShow")}
                      </Chip>
                    ))}
                  </div>
                </li>
              ))}
            </ul>
            {rate.isError && (
              <p role="alert" className="text-sm text-danger">
                {rate.error.message}
              </p>
            )}
            <p role="status" className="text-sm font-semibold text-success">
              {rate.isSuccess && !changed ? t("after.saved") : ""}
            </p>
            <Button type="submit" block disabled={!changed || rate.isPending}>
              {t("after.save")}
            </Button>
          </form>
        )}
      </section>
    </div>
  );
}
