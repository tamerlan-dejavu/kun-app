"use client";

import { useQuery } from "@tanstack/react-query";
import { api, unwrap } from "@/lib/api/client";

type Point = { lat: number; lng: number } | null;

export function useForYou(point: Point = null) {
  return useQuery({
    queryKey: ["for-you", point],
    queryFn: () =>
      unwrap(api.GET("/api/v1/for-you", { params: { query: point ? { lat: point.lat, lng: point.lng } : {} } })),
  });
}
