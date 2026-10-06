"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api, unwrap } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";
import { keys } from "./keys";

type MeUpdate = components["schemas"]["PatchedMeUpdateRequest"];
type ReportBody = components["schemas"]["ReportCreateRequest"];

export function useUser(id: number) {
  return useQuery({
    queryKey: ["user", id],
    queryFn: () => unwrap(api.GET("/api/v1/users/{id}", { params: { path: { id } } })),
  });
}

export function useUniversities() {
  return useQuery({
    queryKey: ["universities"],
    queryFn: () => unwrap(api.GET("/api/v1/catalog/universities")),
    staleTime: 60 * 60_000,
  });
}

export function useInterests() {
  return useQuery({
    queryKey: ["interests"],
    queryFn: () => unwrap(api.GET("/api/v1/catalog/interests")),
    staleTime: 60 * 60_000,
  });
}

export function useUpdateMe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: MeUpdate) => unwrap(api.PATCH("/api/v1/me", { body })),
    onSuccess: (me) => qc.setQueryData(keys.me, me),
  });
}

export function useUploadPhoto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (file: File) =>
      unwrap(
        api.POST("/api/v1/me/photo", {
          // В схеме поле — строка (binary); реальное тело — multipart с файлом.
          // Заголовок Content-Type с boundary браузер проставит сам.
          body: { photo: file.name },
          bodySerializer: () => {
            const form = new FormData();
            form.append("photo", file);
            return form;
          },
        }),
      ),
    onSuccess: (me) => qc.setQueryData(keys.me, me),
  });
}

/** Блокировка / снятие; после — освежаем профиль и ленту (сборы заблокированных скрываются). */
export function useBlock(userId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (block: boolean) =>
      unwrap(
        block
          ? api.POST("/api/v1/blocks", { body: { user_id: userId } })
          : api.DELETE("/api/v1/blocks/{user_id}", { params: { path: { user_id: userId } } }),
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["user", userId] });
      qc.invalidateQueries({ queryKey: ["feed"] });
    },
  });
}

export function useReport() {
  return useMutation({
    mutationFn: (body: ReportBody) => unwrap(api.POST("/api/v1/reports", { body })),
  });
}
