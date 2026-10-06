import clsx from "clsx";

/** Квадратное фото в рамке; без фото — инициал. Ч/б фото — часть языка KUN. */
export function Avatar({
  name,
  photo,
  size = "md",
}: {
  name?: string | null;
  photo?: string | null;
  size?: "sm" | "md" | "lg";
}) {
  const cls = clsx("shrink-0 rounded-card border-2 border-ink", {
    "h-8 w-8 text-sm": size === "sm",
    "h-11 w-11": size === "md",
    "h-28 w-28 text-4xl shadow-card": size === "lg",
  });
  if (photo) {
    // eslint-disable-next-line @next/next/no-img-element -- фото с бэкенда/S3, размер известен
    return <img src={photo} alt="" className={clsx(cls, "object-cover grayscale")} />;
  }
  return (
    <span aria-hidden className={clsx(cls, "flex items-center justify-center bg-brand font-heading font-extrabold text-ink")}>
      {(name ?? "?").trim().charAt(0).toUpperCase() || "?"}
    </span>
  );
}
