import { t } from "@/i18n";
import { Container } from "./Container";

const STEPS = [
  ["landing.step1Title", "landing.step1Text"],
  ["landing.step2Title", "landing.step2Text"],
  ["landing.step3Title", "landing.step3Text"],
] as const;

export function HowItWorks() {
  return (
    <section id="how" className="scroll-mt-20 py-14 md:py-20">
      <Container>
        <h2 className="mb-8 text-2xl md:text-4xl">{t("landing.howTitle")}</h2>
        <ol className="grid gap-4 md:grid-cols-3 md:gap-6">
          {STEPS.map(([title, text], i) => (
            <li key={title} className="rounded-card bg-surface p-6 shadow-card md:p-8">
              <span
                aria-hidden
                className="mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-brand font-heading text-lg text-white"
              >
                {i + 1}
              </span>
              <h3 className="mb-2 text-lg">{t(title)}</h3>
              <p className="text-ink-muted">{t(text)}</p>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  );
}
