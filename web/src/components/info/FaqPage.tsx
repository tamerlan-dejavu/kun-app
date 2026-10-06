import type { FaqDoc } from "@/content/types";
import { PageTitle } from "@/components/layout/PageTitle";

// FAQ: нативные <details> — работают без JS, с клавиатуры и скринридером.
export function FaqPage({ doc }: { doc: FaqDoc }) {
  return (
    <article>
      <PageTitle title={doc.title} />
      {doc.lead && <p className="mb-8 text-lg text-ink-muted">{doc.lead}</p>}
      <div className="space-y-10">
        {doc.groups.map((g) => (
          <section key={g.title}>
            <h2 className="mb-4 text-xl">{g.title}</h2>
            <div className="space-y-3">
              {g.items.map((item) => (
                <details key={item.q} className="card group">
                  <summary className="flex min-h-tap cursor-pointer list-none items-center justify-between gap-4 px-6 py-4 font-semibold">
                    {item.q}
                    <span aria-hidden className="text-xl text-brand transition-transform group-open:rotate-45">
                      +
                    </span>
                  </summary>
                  <p className="px-6 pb-5 leading-relaxed text-ink-muted">{item.a}</p>
                </details>
              ))}
            </div>
          </section>
        ))}
      </div>
    </article>
  );
}
