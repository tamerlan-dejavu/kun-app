import createClient from "openapi-fetch";
import type { paths } from "./schema";

// Клиент для браузера: сессионная кука + CSRF-токен из куки csrftoken.
export const api = createClient<paths>({ baseUrl: "/api/v1", credentials: "include" });

// TODO: middleware, добавляющий X-CSRFToken для небезопасных методов
// TODO: приведение ошибок к формату {code, message}
