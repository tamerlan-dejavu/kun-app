// Даты приходят в UTC, показываем в часовом поясе Алматы (раздел 4 ТЗ).
export const ALMATY_TZ = "Asia/Almaty";

const dayKey = (d: Date) =>
  new Intl.DateTimeFormat("en-CA", { timeZone: ALMATY_TZ, dateStyle: "short" }).format(d);

const time = (d: Date) =>
  new Intl.DateTimeFormat("ru-RU", {
    timeZone: ALMATY_TZ,
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);

/** «Сегодня, 19:00» / «Завтра, 19:00» / «пт, 10 октября, 19:00» */
export function formatStartsAt(iso: string, now: Date = new Date()): string {
  const d = new Date(iso);
  const tomorrow = new Date(now.getTime() + 24 * 3600_000);
  if (dayKey(d) === dayKey(now)) return `Сегодня, ${time(d)}`;
  if (dayKey(d) === dayKey(tomorrow)) return `Завтра, ${time(d)}`;
  const day = new Intl.DateTimeFormat("ru-RU", {
    timeZone: ALMATY_TZ,
    weekday: "short",
    day: "numeric",
    month: "long",
  }).format(d);
  return `${day}, ${time(d)}`;
}

/** Время сообщения в чате: «19:05» */
export const formatTime = (iso: string) => time(new Date(iso));

export function formatDistance(meters?: number | null): string | null {
  if (meters == null) return null;
  return meters < 1000 ? `${Math.round(meters / 10) * 10} м` : `${(meters / 1000).toFixed(1)} км`;
}
