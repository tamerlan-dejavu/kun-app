import clsx from "clsx";

// Состояние «загрузка»: штрихованные блоки в рамке — как незаполненная вёрстка.
export function Skeleton({ className = "h-24" }: { className?: string }) {
  return (
    <div
      aria-hidden
      className={clsx(
        "animate-pulse rounded-card border-2 border-dashed border-ink/30 bg-[repeating-linear-gradient(135deg,transparent_0_10px,rgba(17,17,17,0.05)_10px_11px)]",
        className,
      )}
    />
  );
}

export function SkeletonList({ count = 3, className = "h-44" }: { count?: number; className?: string }) {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3" role="status" aria-label="Загружаем">
      {Array.from({ length: count }, (_, i) => (
        <Skeleton key={i} className={className} />
      ))}
    </div>
  );
}
