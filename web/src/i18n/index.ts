import ru from "./ru.json";

// Все строки — в файлах локализации; казахский (kk.json) добавится на этапе 2.
const dictionaries = { ru } as const;
export type Locale = keyof typeof dictionaries;

export function t(key: string, params?: Record<string, string | number>, locale: Locale = "ru"): string {
  const value = key.split(".").reduce<unknown>((acc, part) => (acc as Record<string, unknown>)?.[part], dictionaries[locale]);
  let text = typeof value === "string" ? value : key;
  for (const [k, v] of Object.entries(params ?? {})) text = text.replace(`{${k}}`, String(v));
  return text;
}
