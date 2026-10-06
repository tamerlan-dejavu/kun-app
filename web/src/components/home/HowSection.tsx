import { t } from "@/i18n";
import { SectionHead } from "@/components/city/SectionHead";
import { Container } from "@/components/layout/Container";

const STEPS = [
  ["landing.step1Title", "landing.step1Text"],
  ["landing.step2Title", "landing.step2Text"],
  ["landing.step3Title", "landing.step3Text"],
] as const;

// 05 — Как это работает: шаги по горизонтальной линии, номера огромные.
export function HowSection() {
  return (
    <section id="how" className="scroll-mt-20 border-t-2 border-ink py-16 md:py-24">
      <Container>
        <SectionHead no="05" kicker={t("home.howKicker")} title={t("home.howTitle")} />
        <ol className="grid border-t-2 border-ink md:grid-cols-3">
          {STEPS.map(([title, text], i) => (
            <li key={title} className="border-b-2 border-ink py-8 md:border-b-0 md:border-r-2 md:px-6 md:last:border-r-0 md:first:pl-0">
              <span aria-hidden className="block font-mono text-7xl font-bold leading-none text-brand">
                0{i + 1}
              </span>
              <h3 className="mb-2 mt-6 text-2xl uppercase">{t(title)}</h3>
              <p className="text-ink-muted">{t(text)}</p>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  );
}
