import { t } from "@/i18n";
import { Container } from "@/components/layout/Container";

const POINTS = [
  ["landing.safety1Title", "landing.safety1"],
  ["landing.safety2Title", "landing.safety2"],
  ["landing.safety3Title", "landing.safety3"],
] as const;

// 06 — Безопасность: чёрная полоса, бумажный текст (16.6:1), терракотовые номера (4.9:1 на чёрном).
export function SafetySection() {
  return (
    <section id="safety" className="scroll-mt-20 bg-ink py-16 text-canvas md:py-24">
      <Container>
        <p className="section-no mb-4 text-brand">06 — {t("home.safetyKicker")}</p>
        <h2 className="mb-12 max-w-[16ch] text-5xl uppercase leading-[0.92] md:text-7xl">{t("home.safetyTitle")}</h2>
        <ul className="grid gap-px border-2 border-canvas bg-canvas md:grid-cols-3">
          {POINTS.map(([title, text], i) => (
            <li key={title} className="bg-ink p-6 md:p-8">
              <span className="meta text-brand">0{i + 1}</span>
              <h3 className="mb-2 mt-4 text-2xl uppercase">{t(title)}</h3>
              <p className="text-canvas/80">{t(text)}</p>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  );
}
