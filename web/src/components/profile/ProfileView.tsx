"use client";

import Link from "next/link";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { buttonClass } from "@/components/ui/Button";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";
import { InterestChips } from "./InterestChips";
import { StatCards } from "./StatCards";

// Свой профиль: имя, фото, вуз, интересы, состоявшиеся сборы, надёжность (раздел 3.2 ТЗ).
export function ProfileView() {
  const me = useMe();
  if (me.isPending) return <Skeleton className="h-64" />;
  if (me.isError) return <ErrorState message={me.error.message} onRetry={() => me.refetch()} />;
  const u = me.data;

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_340px] lg:items-start">
      <div className="space-y-6">
        <section className="flex flex-col items-start gap-6 rounded-card bg-surface p-6 shadow-card sm:flex-row sm:items-center md:p-8">
          <Avatar name={u.name} photo={u.photo} size="lg" />
          <div className="flex-1 space-y-2">
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
          <Link href="/profile/edit" className={buttonClass("secondary")}>
            {t("profile.edit")}
          </Link>
        </section>
        <section className="rounded-card bg-surface p-6 shadow-card md:p-8">
          <h2 className="mb-4 text-base">{t("profile.interests")}</h2>
          <InterestChips interests={u.interests} />
        </section>
      </div>

      <aside className="space-y-4">
        <StatCards happened={u.happened_gatherings_count} reliability={u.reliability} />
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
