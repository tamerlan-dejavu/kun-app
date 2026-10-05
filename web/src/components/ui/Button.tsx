import clsx from "clsx";
import type { ButtonHTMLAttributes } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "ghost" };

// Область нажатия не меньше 44x44 (WCAG 2.1 AA).
export function Button({ variant = "primary", className, ...props }: Props) {
  return (
    <button
      className={clsx(
        "min-h-tap rounded-button px-5 font-semibold",
        variant === "primary" && "bg-brand text-neutral-900",
        className,
      )}
      {...props}
    />
  );
}
