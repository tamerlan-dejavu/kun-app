import createClient, { type Middleware } from "openapi-fetch";
import type { paths } from "./schema";

/** Ошибка API в едином формате бэкенда: {code, message} + статус. */
export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public fields?: Record<string, string[]>,
  ) {
    super(message);
  }
}

export function getCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  return document.cookie
    .split("; ")
    .find((c) => c.startsWith(`${name}=`))
    ?.split("=")[1];
}

const UNSAFE = new Set(["POST", "PUT", "PATCH", "DELETE"]);

// Django: сессионная кука + CSRF-токен из куки csrftoken в заголовке X-CSRFToken
const csrf: Middleware = {
  onRequest({ request }) {
    if (UNSAFE.has(request.method)) {
      const token = getCookie("csrftoken");
      if (token) request.headers.set("X-CSRFToken", token);
    }
    return request;
  },
};

// Пути в схеме уже начинаются с /api/v1 — baseUrl пустой (тот же домен, nginx)
export const api = createClient<paths>({ baseUrl: "", credentials: "include" });
api.use(csrf);

type FetchResult<T> = { data?: T; error?: unknown; response: Response };

type ErrorBody = { code?: string; message?: string; fields?: Record<string, string[]> };

/** Распаковать ответ openapi-fetch: данные или ApiError. */
export async function unwrap<T>(promise: Promise<FetchResult<T>>): Promise<T> {
  const { data, error, response } = await promise;
  if (response.ok) return data as T;
  const body = (error ?? {}) as ErrorBody;
  throw new ApiError(
    body.code ?? "error",
    body.message ?? "Что-то пошло не так",
    response.status,
    body.fields,
  );
}

/** Курсор следующей страницы из поля next (там полный URL). */
export function nextCursor(next?: string | null): string | undefined {
  if (!next) return undefined;
  return new URL(next).searchParams.get("cursor") ?? undefined;
}

// Ошибки всех запросов TanStack Query — ApiError (с code и status), а не голый Error
declare module "@tanstack/react-query" {
  interface Register {
    defaultError: ApiError;
  }
}
