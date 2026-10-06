import clsx from "clsx";
import { t } from "@/i18n";

type Interest = { slug: string; name: string };

/** Интересы чипами; общие со мной — выделены и подписаны для скринридера. */
export function InterestChips({ interests, common = [] }: { interests: Interest[]; common?: string[] }) {
  if (interests.length === 0) return <p className="text-ink-muted">{t("profile.noInterests")}</p>;
  return (
    <ul className="flex flex-wrap gap-2">
      {interests.map((i) => {
        const shared = common.includes(i.slug);
        return (
          <li
            key={i.slug}
            className={clsx(
              "meta rounded-chip border-2 border-ink px-2.5 py-1 font-bold",
              shared ? "bg-brand text-ink" : "bg-surface text-ink",
            )}
          >
            {i.name}
            {shared && <span className="sr-only"> ({t("profile.common")})</span>}
          </li>
        );
      })}
    </ul>
  );
}
