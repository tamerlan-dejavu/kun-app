import { t } from "@/i18n";

const STEPS = [
  ["landing.step1Title", "landing.step1Text"],
  ["landing.step2Title", "landing.step2Text"],
  ["landing.step3Title", "landing.step3Text"],
] as const;

export function HowItWorks() {
  return (
    <section className="px-5 py-8">
      <h2 className="mb-5 text-xl">{t("landing.howTitle")}</h2>
      <ol className="space-y-3">
        {STEPS.map(([title, text], i) => (
          <li key={title} className="flex gap-4 rounded-card bg-surface p-4 shadow-card">
            <span
              aria-hidden
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand font-heading"
            >
              {i + 1}
            </span>
            <div>
              <h3 className="mb-1 text-base">{t(title)}</h3>
              <p className="text-ink-muted">{t(text)}</p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
