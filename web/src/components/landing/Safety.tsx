import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";
import { Container } from "@/components/layout/Container";

const POINTS = [
  ["landing.safety1Title", "landing.safety1"],
  ["landing.safety2Title", "landing.safety2"],
  ["landing.safety3Title", "landing.safety3"],
] as const;

// Тёмная полоса: vanilla-текст на brand-800 (4.88:1), заголовки — белые.
export function Safety() {
  return (
    <section id="safety" className="scroll-mt-20 bg-brand-800 py-14 text-sand md:py-20">
      <Container>
        <h2 className="mb-10 text-2xl text-white md:text-4xl">{t("landing.safetyTitle")}</h2>
        <ul className="grid gap-8 md:grid-cols-3">
          {POINTS.map(([title, text]) => (
            <li key={title}>
              <Icon name="check" className="mb-4 h-8 w-8 text-white" />
              <h3 className="mb-2 text-lg text-white">{t(title)}</h3>
              <p>{t(text)}</p>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  );
}
