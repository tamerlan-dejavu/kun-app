import "server-only";

// Запросы из серверных компонентов (SSR /g/<slug>, Open Graph) напрямую в контейнер api.
const API = process.env.API_INTERNAL_URL ?? "http://localhost:8000";

export async function getPublicGathering(slug: string) {
  const res = await fetch(`${API}/api/v1/public/gatherings/${slug}`, { next: { revalidate: 30 } });
  if (!res.ok) return null;
  return res.json();
}
