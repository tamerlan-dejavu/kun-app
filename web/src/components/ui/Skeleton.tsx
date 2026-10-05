// Состояние «загрузка».
export function Skeleton({ className = "h-24" }: { className?: string }) {
  return <div aria-hidden className={`animate-pulse rounded-card bg-neutral-100 ${className}`} />;
}
