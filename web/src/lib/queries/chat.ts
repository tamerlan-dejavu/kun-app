"use client";

import { useInfiniteQuery, useMutation } from "@tanstack/react-query";
import { api, nextCursor, unwrap } from "@/lib/api/client";
import { keys } from "./keys";

/** История: новые сверху; следующая страница — более старые сообщения. */
export function useMessages(gatheringId: number) {
  return useInfiniteQuery({
    queryKey: keys.messages(gatheringId),
    queryFn: ({ pageParam }) =>
      unwrap(
        api.GET("/api/v1/gatherings/{id}/messages", {
          params: { path: { id: gatheringId }, query: { cursor: pageParam } },
        }),
      ),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (page) => nextCursor(page.next),
  });
}

/** Отправка. Само сообщение приходит обратно по WebSocket (message.new). */
export function useSendMessage(gatheringId: number) {
  return useMutation({
    mutationFn: (text: string) =>
      unwrap(
        api.POST("/api/v1/gatherings/{id}/messages", {
          params: { path: { id: gatheringId } },
          body: { text },
        }),
      ),
  });
}
