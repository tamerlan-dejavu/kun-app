"use client";

import { useQuery } from "@tanstack/react-query";
import { api, unwrap } from "@/lib/api/client";

// Справочник меняется редко — держим в кэше час
export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: () => unwrap(api.GET("/api/v1/catalog/categories")),
    staleTime: 60 * 60_000,
  });
}
