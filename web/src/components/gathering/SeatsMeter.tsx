import clsx from "clsx";
import { t } from "@/i18n";

/** «Идут N из M» + точки мест. */
export function SeatsMeter({ count, seats }: { count: number; seats: number }) {
  return (
    <div className="flex items-center gap-2">
      <span aria-hidden className="flex gap-1">
        {Array.from({ length: seats }, (_, i) => (
          <span
            key={i}
            className={clsx("h-2.5 w-2.5 rounded-full", i < count ? "bg-brand" : "bg-line")}
          />
        ))}
      </span>
      <span className="text-sm font-semibold">{t("gathering.going", { n: count, m: seats })}</span>
    </div>
  );
}
