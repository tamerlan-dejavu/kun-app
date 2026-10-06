import clsx from "clsx";
import type { ReactNode } from "react";

// Заголовок раздела главной: номер «01 —» вынесен за колонку, заголовок — огромный.
export function SectionHead({
  no,
  kicker,
  title,
  className,
  size = "xl",
  children,
}: {
  size?: "xl" | "lg";
  no: string;
  kicker: string;
  title: ReactNode;
  className?: string;
  children?: ReactNode;
}) {
  return (
    <div className={clsx("relative mb-10 md:mb-14", className)}>
      <p className="section-no mb-4 flex items-center gap-3 md:absolute md:-left-24 md:top-2 md:mb-0 md:w-20 md:flex-col md:items-start md:gap-1">
        <span>{no}</span>
        <span className="text-ink-muted">— {kicker}</span>
      </p>
      <h2
        className={clsx(
          "max-w-[14ch] uppercase leading-[0.92]",
          size === "xl" ? "text-5xl md:text-7xl lg:text-8xl" : "text-4xl md:text-5xl lg:text-6xl",
        )}
      >
        {title}
      </h2>
      {children && <div className="mt-6 max-w-xl text-lg text-ink-muted">{children}</div>}
    </div>
  );
}
