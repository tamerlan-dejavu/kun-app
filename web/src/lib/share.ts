// Web Share API, иначе — копирование ссылки.
export async function shareLink(url: string, title: string): Promise<"shared" | "copied"> {
  if (navigator.share) {
    await navigator.share({ url, title });
    return "shared";
  }
  await navigator.clipboard.writeText(url);
  return "copied";
}
