// Web Share API, иначе — копирование ссылки (раздел 3.3 ТЗ).
export async function shareLink(
  url: string,
  title: string,
): Promise<"shared" | "copied" | "cancelled"> {
  if (typeof navigator.share === "function") {
    try {
      await navigator.share({ url, title });
      return "shared";
    } catch {
      return "cancelled"; // пользователь закрыл меню
    }
  }
  await navigator.clipboard.writeText(url);
  return "copied";
}
