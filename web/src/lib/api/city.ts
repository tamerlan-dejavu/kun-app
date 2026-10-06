import "server-only";
import type { components } from "./schema";

export type CitySnapshot = components["schemas"]["CitySnapshot"];

const API = process.env.API_INTERNAL_URL ?? "http://localhost:8000";

/** Витрина города для главной: сервер Next ходит прямо в api, кэш 60 с. */
export async function getCity(): Promise<CitySnapshot | null> {
  try {
    const res = await fetch(`${API}/api/v1/public/city`, { next: { revalidate: 60 } });
    return res.ok ? res.json() : null;
  } catch {
    return null; // главная должна открываться, даже если api недоступен
  }
}
