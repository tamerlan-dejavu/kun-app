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
              "rounded-chip px-3.5 py-1.5 text-sm font-semibold",
              shared ? "bg-brand text-white" : "bg-sand-100 text-sand-800",
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
