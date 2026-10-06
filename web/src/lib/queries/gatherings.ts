"use client";

import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, nextCursor, unwrap } from "@/lib/api/client";
import type { Source } from "@/lib/source";
import { keys } from "./keys";

export type FeedFilters = {
  date?: "today" | "tomorrow" | "week";
  category?: string;
  lat?: number;
  lng?: number;
};

export function useFeed(filters: FeedFilters) {
  return useInfiniteQuery({
    queryKey: keys.feed(filters),
    queryFn: ({ pageParam }) =>
      unwrap(
        api.GET("/api/v1/gatherings", { params: { query: { ...filters, cursor: pageParam } } }),
      ),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (page) => nextCursor(page.next),
  });
}

export function useMyGatherings(when: "upcoming" | "past") {
  return useInfiniteQuery({
    queryKey: keys.my(when),
    queryFn: ({ pageParam }) =>
      unwrap(api.GET("/api/v1/me/gatherings", { params: { query: { when, cursor: pageParam } } })),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (page) => nextCursor(page.next),
  });
}

export function useGathering(id: number) {
  return useQuery({
    queryKey: keys.gathering(id),
    queryFn: () => unwrap(api.GET("/api/v1/gatherings/{id}", { params: { path: { id } } })),
  });
}

type Action = "join" | "leave";

/** Присоединиться / выйти: ответ — сбор целиком, кладём его в кэш и обновляем списки. */
export function useParticipation(id: number, source: Source = "link") {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (action: Action) =>
      unwrap(
        action === "join"
          ? api.POST("/api/v1/gatherings/{id}/join", { params: { path: { id } }, body: { source } })
          : api.POST("/api/v1/gatherings/{id}/leave", { params: { path: { id } } }),
      ),
    onSuccess: (gathering) => {
      qc.setQueryData(keys.gathering(id), gathering);
      qc.invalidateQueries({ queryKey: ["feed"] });
      qc.invalidateQueries({ queryKey: ["my"] });
    },
  });
}
