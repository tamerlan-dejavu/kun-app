import { landing, t } from "@/i18n";
import { Container } from "@/components/layout/Container";

export function Categories() {
  return (
    <section id="where" className="scroll-mt-20 bg-sand-100 py-14 md:py-20">
      <Container className="grid gap-8 md:grid-cols-[1fr_1.4fr] md:items-center">
        <div>
          <h2 className="mb-4 text-2xl md:text-4xl">{t("landing.whereTitle")}</h2>
          <p className="text-lg text-sand-800">{t("landing.whereLead")}</p>
        </div>
        <ul className="flex flex-wrap gap-3">
          {landing().categories.map((c) => (
            <li
              key={c}
              className="rounded-chip border border-sand-300 bg-surface px-5 py-3 font-semibold"
            >
              {c}
            </li>
          ))}
        </ul>
      </Container>
    </section>
  );
}
