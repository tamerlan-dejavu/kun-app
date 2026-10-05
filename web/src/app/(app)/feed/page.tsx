import { FeedFilters } from "@/components/gathering/FeedFilters";

// /feed — лента сборов. Состояния: скелетон, пусто («Создай первый сбор»), ошибка.
export default function FeedPage() {
  return (
    <>
      <FeedFilters />
      {/* TODO: FeedList (useFeed, бесконечная прокрутка) */}
    </>
  );
}
