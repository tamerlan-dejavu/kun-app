import "server-only";
import { cookies } from "next/headers";
import type { GatheringPublic } from "./types";

// Серверные компоненты (SSR /g/<slug>, Open Graph) ходят напрямую в контейнер api, мимо nginx
const API = process.env.API_INTERNAL_URL ?? "http://localhost:8000";

export async function getPublicGathering(slug: string): Promise<GatheringPublic | null> {
  const res = await fetch(`${API}/api/v1/public/gatherings/${encodeURIComponent(slug)}`, {
    next: { revalidate: 30 },
  });
  if (!res.ok) return null;
  return res.json();
}

/** Есть ли сессия: решаем, показывать гостевую версию страницы или версию участника. */
export async function hasSession(): Promise<boolean> {
  return (await cookies()).has("sessionid");
}
