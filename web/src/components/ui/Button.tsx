import clsx from "clsx";
import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";

const base =
  "inline-flex min-h-tap items-center justify-center gap-2 rounded-button px-5 text-base font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50";

// На абрикосовом — только тёмный текст: белый даёт контраст 1.8:1
const variants: Record<Variant, string> = {
  primary: "bg-brand text-ink hover:bg-brand-500 active:bg-brand-600",
  secondary: "border border-line bg-surface text-ink hover:bg-brand-50",
  ghost: "text-ink-muted hover:bg-brand-50 hover:text-ink",
  danger: "border border-line bg-surface text-danger hover:bg-red-50",
};

export function buttonClass(variant: Variant = "primary", block = false) {
  return clsx(base, variants[variant], block && "w-full");
}

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; block?: boolean };

export function Button({ variant = "primary", block, className, ...props }: Props) {
  return <button className={clsx(buttonClass(variant, block), className)} {...props} />;
}

export function ButtonLink({
  href,
  variant = "primary",
  block,
  children,
}: {
  href: string;
  variant?: Variant;
  block?: boolean;
  children: ReactNode;
}) {
  return (
    <Link href={href} className={buttonClass(variant, block)}>
      {children}
    </Link>
  );
}
