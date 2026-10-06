import clsx from "clsx";

/** Фото пользователя; без фото — инициал на абрикосовом фоне. */
export function Avatar({
  name,
  photo,
  size = "md",
}: {
  name?: string | null;
  photo?: string | null;
  size?: "sm" | "md" | "lg";
}) {
  const cls = clsx("shrink-0 rounded-full", {
    "h-8 w-8 text-sm": size === "sm",
    "h-11 w-11": size === "md",
    "h-24 w-24 text-3xl": size === "lg",
  });
  if (photo) {
    // eslint-disable-next-line @next/next/no-img-element -- фото с бэкенда/S3, размер известен
    return <img src={photo} alt="" className={clsx(cls, "object-cover")} />;
  }
  return (
    <span aria-hidden className={clsx(cls, "flex items-center justify-center bg-sand-100 font-semibold text-sand-800")}>
      {(name ?? "?").trim().charAt(0).toUpperCase() || "?"}
    </span>
  );
}
