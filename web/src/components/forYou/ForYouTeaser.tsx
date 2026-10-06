"use client";

import Link from "next/link";
import { t } from "@/i18n";
import { useForYou } from "@/lib/queries/forYou";
import { ForYouCard } from "./ForYouCard";

// Блок вверху ленты: три лучших варианта и ссылка на всю подборку. Пусто — не показываем.
export function ForYouTeaser() {
  const query = useForYou();
  const items = query.data?.slice(0, 3) ?? [];
  if (items.length === 0) return null;
  return (
    <section aria-labelledby="for-you-teaser" className="mb-12 border-b-2 border-ink pb-10">
      <div className="mb-5 flex items-end justify-between gap-4">
        <h2 id="for-you-teaser" className="text-3xl uppercase md:text-4xl">
          {t("forYou.teaser")}
        </h2>
        <Link href="/for-you" className="meta font-bold underline-offset-4 hover:underline">
          {t("forYou.all")}
        </Link>
      </div>
      <ol className="grid gap-6 md:grid-cols-3">
        {items.map((item, i) => (
          <li key={item.gathering.id}>
            <ForYouCard item={item} index={i} />
          </li>
        ))}
      </ol>
    </section>
  );
}
