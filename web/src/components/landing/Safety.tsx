import Link from "next/link";
import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";

const POINTS = ["landing.safety1", "landing.safety2", "landing.safety3"] as const;

export function Safety() {
  return (
    <section className="px-5 py-8">
      <h2 className="mb-5 text-xl">{t("landing.safetyTitle")}</h2>
      <ul className="mb-8 space-y-3">
        {POINTS.map((p) => (
          <li key={p} className="flex gap-3">
            <Icon name="check" className="mt-0.5 h-5 w-5 shrink-0 text-success" />
            {t(p)}
          </li>
        ))}
      </ul>
      <nav className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-ink-muted">
        <Link className="underline" href="/rules">{t("landing.rules")}</Link>
        <Link className="underline" href="/privacy">{t("landing.privacy")}</Link>
        <Link className="underline" href="/support">{t("landing.support")}</Link>
      </nav>
    </section>
  );
}
