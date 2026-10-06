import { t } from "@/i18n";
import type { TextDoc } from "@/content/types";
import { PageTitle } from "@/components/layout/PageTitle";

// Шаблон текстовой страницы: правила, соглашение, конфиденциальность, поддержка.
export function TextPage({ doc }: { doc: TextDoc }) {
  return (
    <article>
      <PageTitle title={doc.title} />
      {doc.draft && (
        <p role="note" className="mb-6 rounded-card bg-sand-100 p-4 text-sm font-semibold text-sand-800">
          {t("info.draft")}
        </p>
      )}
      {doc.lead && <p className="mb-8 text-lg text-ink-muted">{doc.lead}</p>}
      {doc.sections.length > 3 && (
        <nav aria-label={t("info.toc")} className="mb-10 rounded-card bg-surface p-6 shadow-card">
          <p className="mb-3 font-heading text-sm">{t("info.toc")}</p>
          <ol className="space-y-1.5">
            {doc.sections.map((s) => (
              <li key={s.id}>
                <a href={`#${s.id}`} className="text-brand underline-offset-4 hover:underline">
                  {s.title}
                </a>
              </li>
            ))}
          </ol>
        </nav>
      )}
      <div className="space-y-10">
        {doc.sections.map((s) => (
          <section key={s.id} id={s.id} className="scroll-mt-24">
            <h2 className="mb-3 text-xl">{s.title}</h2>
            <div className="space-y-3 leading-relaxed">
              {s.blocks.map((b, i) =>
                typeof b === "string" ? (
                  <p key={i}>{b}</p>
                ) : (
                  <ul key={i} className="list-disc space-y-1.5 pl-5 marker:text-brand">
                    {b.list.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                ),
              )}
            </div>
          </section>
        ))}
      </div>
    </article>
  );
}
