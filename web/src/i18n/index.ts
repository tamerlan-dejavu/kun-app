import ru from "./ru.json";

// Все строки — в файлах локализации; казахский (kk.json) добавится на этапе 2.
const dictionaries = { ru } as const;
export type Locale = keyof typeof dictionaries;

// "feed.today" | "gathering.going" | … — опечатка в ключе ловится при проверке типов
type Paths<T, P extends string = ""> = {
  [K in keyof T & string]: T[K] extends string ? `${P}${K}` : Paths<T[K], `${P}${K}.`>;
}[keyof T & string];
export type MessageKey = Paths<typeof ru>;

export function t(
  key: MessageKey,
  params?: Record<string, string | number>,
  locale: Locale = "ru",
): string {
  const value = key
    .split(".")
    .reduce<unknown>((acc, part) => (acc as Record<string, unknown>)?.[part], dictionaries[locale]);
  let text = typeof value === "string" ? value : key;
  for (const [k, v] of Object.entries(params ?? {})) text = text.replaceAll(`{${k}}`, String(v));
  return text;
}
