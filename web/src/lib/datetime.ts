// Даты приходят в UTC, показываем в часовом поясе Алматы.
export const ALMATY_TZ = "Asia/Almaty";

export function formatStartsAt(iso: string): string {
  return new Intl.DateTimeFormat("ru-RU", {
    timeZone: ALMATY_TZ,
    weekday: "short",
    day: "numeric",
    month: "long",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(iso));
}
