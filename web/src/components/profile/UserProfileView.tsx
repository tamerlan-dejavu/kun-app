"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { useBlock, useUser } from "@/lib/queries/profile";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";
import { ReportDialog } from "@/components/moderation/ReportDialog";
import { InterestChips } from "./InterestChips";
import { StatCards } from "./StatCards";

// «сентября 2026»: без числа Intl отдаёт именительный падеж («сентябрь»), поэтому берём
// полную дату («1 сентября 2026 г.») и убираем число и «г.»
const monthYear = (iso: string) =>
  new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "Asia/Almaty",
  })
    .format(new Date(iso))
    .replace(/^\d+\s/, "")
    .replace(/\s?г\.$/, "");

// Чужой профиль: без телефона; общие интересы, «вместе на сборах», жалоба и блокировка.
export function UserProfileView({ id }: { id: number }) {
  const router = useRouter();
  const me = useMe();
  const query = useUser(id);
  const block = useBlock(id);

  const isMe = me.data?.id === id;
  useEffect(() => {
    if (isMe) router.replace("/profile");
  }, [isMe, router]);

  if (query.isPending || isMe) return <Skeleton className="h-64" />;
  if (query.isError) {
    return query.error.status === 404 ? (
      <EmptyState title={t("profile.notFound")} hint={t("profile.notFoundHint")} />
    ) : (
      <ErrorState message={query.error.message} onRetry={() => query.refetch()} />
    );
  }

  const u = query.data;
  const toggleBlock = () => {
    if (u.is_blocked || window.confirm(t("profile.blockConfirm"))) block.mutate(!u.is_blocked);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_340px] lg:items-start">
      <div className="space-y-6">
        <section className="flex flex-col items-start gap-6 rounded-card bg-surface p-6 shadow-card sm:flex-row sm:items-center md:p-8">
          <Avatar name={u.name} photo={u.photo} size="lg" />
          <div className="space-y-1.5">
            <h2 className="text-2xl">{u.name}</h2>
            {u.university && <p className="text-ink-muted">{u.university}</p>}
            <p className="text-sm text-ink-muted">{t("profile.since", { date: monthYear(u.date_joined) })}</p>
            {u.together_count > 0 && (
              <p className="text-sm font-semibold text-brand">{t("profile.together", { n: u.together_count })}</p>
            )}
          </div>
        </section>
        <section className="rounded-card bg-surface p-6 shadow-card md:p-8">
          <h2 className="mb-4 text-base">{t("profile.interests")}</h2>
          <InterestChips interests={u.interests} common={u.common_interests} />
        </section>
      </div>

      <aside className="space-y-4">
        <StatCards happened={u.happened_gatherings_count} reliability={u.reliability} />
        {u.is_blocked && (
          <p role="status" className="rounded-card bg-sand-100 p-4 text-sm font-semibold text-sand-800">
            {t("profile.blocked")}
          </p>
        )}
        {block.isError && (
          <p role="alert" className="text-sm text-danger">
            {block.error.message}
          </p>
        )}
        <ReportDialog
          targetType="user"
          targetId={u.id}
          trigger={(open) => (
            <Button variant="secondary" block onClick={open}>
              {t("profile.report")}
            </Button>
          )}
        />
        <Button variant={u.is_blocked ? "secondary" : "danger"} block onClick={toggleBlock} disabled={block.isPending}>
          {u.is_blocked ? t("profile.unblock") : t("profile.block")}
        </Button>
      </aside>
    </div>
  );
}
