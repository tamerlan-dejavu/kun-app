import { t, type MessageKey } from "@/i18n";
import type { components } from "@/lib/api/schema";
import { pluralKey } from "@/lib/plural";

type Reason = components["schemas"]["Reason"];

/** Строка-объяснение рекомендации из code и params (тексты — в i18n). */
export function reasonText(reason: Reason): string {
  const p = reason.params as Record<string, string | number>;
  switch (reason.code) {
    case "together":
      return Number(p.n) > 1
        ? t("forYou.reasons.togetherMany", { name: p.name, more: Number(p.n) - 1 })
        : t("forYou.reasons.together", { name: p.name });
    case "attended":
      return t("forYou.reasons.attended", {
        category: p.category,
        n: p.n,
        times: t(`forYou.times.${pluralKey(Number(p.n))}` as MessageKey),
      });
    case "time_habit":
      return t("forYou.reasons.time_habit", { bucket: t(`forYou.buckets.${p.bucket}` as MessageKey) });
    case "near":
      return t("forYou.reasons.near", { km: String(p.km).replace(".", ",") });
    default:
      return t(`forYou.reasons.${reason.code}` as MessageKey, p);
  }
}
