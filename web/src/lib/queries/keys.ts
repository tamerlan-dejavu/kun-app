import type { FeedFilters } from "./gatherings";

// Ключи кэша TanStack Query — в одном месте, чтобы точно инвалидировать после действий
export const keys = {
  me: ["me"] as const,
  feed: (f: FeedFilters) => ["feed", f] as const,
  gathering: (id: number) => ["gathering", id] as const,
  my: (when: "upcoming" | "past") => ["my", when] as const,
  messages: (id: number) => ["messages", id] as const,
};
