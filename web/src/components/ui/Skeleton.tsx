import clsx from "clsx";

// Состояние «загрузка».
export function Skeleton({ className = "h-24" }: { className?: string }) {
  return <div aria-hidden className={clsx("animate-pulse rounded-card bg-line/60", className)} />;
}

export function SkeletonList({ count = 3, className = "h-36" }: { count?: number; className?: string }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" role="status" aria-label="Загружаем">
      {Array.from({ length: count }, (_, i) => (
        <Skeleton key={i} className={className} />
      ))}
    </div>
  );
}
