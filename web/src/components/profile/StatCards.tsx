import { t } from "@/i18n";

// Состоявшиеся сборы и надёжность — в своём и чужом профиле одинаково.
export function StatCards({ happened, reliability }: { happened: number; reliability?: number | null }) {
  const percent = reliability == null ? null : Math.round(reliability * 100);
  return (
    <>
      <dl className="grid grid-cols-2 gap-4">
        <div className="rounded-card bg-surface p-5 shadow-card">
          <dt className="text-sm text-ink-muted">{t("profile.happened")}</dt>
          <dd className="mt-1 font-heading text-3xl">{happened}</dd>
        </div>
        <div className="rounded-card bg-surface p-5 shadow-card">
          <dt className="text-sm text-ink-muted">{t("profile.reliability")}</dt>
          {percent == null ? (
            <dd className="mt-2 font-semibold leading-snug text-ink-muted">{t("profile.reliabilityNone")}</dd>
          ) : (
            <dd className="mt-1 font-heading text-3xl">{percent}%</dd>
          )}
        </div>
      </dl>
      <p className="text-sm text-ink-muted">{t("profile.reliabilityHint")}</p>
    </>
  );
}
