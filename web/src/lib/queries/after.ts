"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api, unwrap } from "@/lib/api/client";
import { keys } from "./keys";

export type RatingValue = "ok" | "no_show";

/** «Я пришёл» и оценки; после — освежаем сбор (attended, my_ratings). */
export function useAfterMeeting(id: number) {
  const qc = useQueryClient();
  const refresh = () => qc.invalidateQueries({ queryKey: keys.gathering(id) });

  const attend = useMutation({
    mutationFn: () =>
      unwrap(api.POST("/api/v1/gatherings/{id}/attendance", { params: { path: { id } } })),
    onSuccess: refresh,
  });
  const rate = useMutation({
    mutationFn: (ratings: Record<number, RatingValue>) =>
      unwrap(
        api.POST("/api/v1/gatherings/{id}/ratings", {
          params: { path: { id } },
          body: {
            ratings: Object.entries(ratings).map(([user_id, value]) => ({
              user_id: Number(user_id),
              value,
            })),
          },
        }),
      ),
    onSuccess: refresh,
  });
  return { attend, rate };
}
