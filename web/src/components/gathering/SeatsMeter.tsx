import clsx from "clsx";
import { t } from "@/i18n";

/** «Идут N из M» + квадраты мест: занятые — терракотовые. */
export function SeatsMeter({ count, seats }: { count: number; seats: number }) {
  return (
    <div className="flex items-center gap-3">
      <span aria-hidden className="flex gap-1">
        {Array.from({ length: seats }, (_, i) => (
          <span key={i} className={clsx("h-3.5 w-3.5 border-2 border-ink", i < count ? "bg-brand" : "bg-surface")} />
        ))}
      </span>
      <span className="meta font-bold">{t("gathering.going", { n: count, m: seats })}</span>
    </div>
  );
}
