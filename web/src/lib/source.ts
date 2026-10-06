// Откуда человек пришёл в сбор — для метрики «Для тебя» против ленты (ТЗ).
export const SOURCES = ["feed", "for_you", "map", "link"] as const;
export type Source = (typeof SOURCES)[number];

export function parseSource(value?: string | null): Source {
  return SOURCES.includes(value as Source) ? (value as Source) : "link";
}

export const gatheringHref = (slug: string, src?: Source) => (src ? `/g/${slug}?src=${src}` : `/g/${slug}`);
