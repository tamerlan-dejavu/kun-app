"use client";

import Link from "next/link";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { buttonClass } from "@/components/ui/Button";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";

// Свой профиль: имя, фото, вуз, состоявшиеся сборы, надёжность (раздел 3.2 ТЗ).
export function ProfileView() {
  const me = useMe();
  if (me.isPending) return <Skeleton className="h-64" />;
  if (me.isError) return <ErrorState message={me.error.message} onRetry={() => me.refetch()} />;
  const u = me.data;
  const reliability = u.reliability == null ? null : Math.round(u.reliability * 100);

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_340px] lg:items-start">
      <section className="flex flex-col items-start gap-6 rounded-card bg-surface p-6 shadow-card sm:flex-row sm:items-center md:p-8">
        <Avatar name={u.name} photo={u.photo} size="lg" />
        <div className="space-y-2">
          <h2 className="text-2xl">{u.name || "—"}</h2>
          <p className="text-ink-muted">
            {t("profile.university")}: {u.university ?? t("profile.noUniversity")}
          </p>
          {u.role !== "user" && (
            <Badge tone="brand">{t(u.role === "admin" ? "profile.admin" : "profile.moderator")}</Badge>
          )}
          <p className="text-sm text-ink-muted">
            {u.phone} · {t("profile.phoneHidden")}
          </p>
        </div>
      </section>

      <aside className="space-y-4">
        <dl className="grid grid-cols-2 gap-4">
          <div className="rounded-card bg-surface p-5 shadow-card">
            <dt className="text-sm text-ink-muted">{t("profile.happened")}</dt>
            <dd className="mt-1 font-heading text-3xl">{u.happened_gatherings_count}</dd>
          </div>
          <div className="rounded-card bg-surface p-5 shadow-card">
            <dt className="text-sm text-ink-muted">{t("profile.reliability")}</dt>
            {reliability == null ? (
              <dd className="mt-2 font-semibold leading-snug text-ink-muted">{t("profile.reliabilityNone")}</dd>
            ) : (
              <dd className="mt-1 font-heading text-3xl">{reliability}%</dd>
            )}
          </div>
        </dl>
        <p className="text-sm text-ink-muted">{t("profile.reliabilityHint")}</p>
        <Link href="/my" className={buttonClass("secondary", true)}>
          {t("profile.myGatherings")}
        </Link>
        <Link href="/settings" className={buttonClass("ghost", true)}>
          {t("profile.settings")}
        </Link>
      </aside>
    </div>
  );
}
