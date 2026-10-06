import clsx from "clsx";
import Link from "next/link";
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger" | "dark";

// Кнопка — физический объект: рамка, жёсткая тень; наведение — сдвиг, нажатие — «вдавливание».
const base =
  "inline-flex min-h-tap items-center justify-center gap-2 rounded-button px-5 text-sm font-bold uppercase tracking-wide transition-[transform,box-shadow,background-color] duration-100 ease-out disabled:cursor-not-allowed disabled:opacity-50";

const physical =
  "border-2 border-ink shadow-sm hover:translate-x-px hover:translate-y-px hover:shadow-[2px_2px_0_#111] active:translate-x-[3px] active:translate-y-[3px] active:shadow-none disabled:translate-x-0 disabled:translate-y-0 disabled:shadow-sm";

// На терракоте — только чёрный текст (белый: 3.86:1, не проходит AA)
const variants: Record<Variant, string> = {
  primary: `${physical} bg-brand text-ink hover:bg-brand-600`,
  secondary: `${physical} bg-surface text-ink hover:bg-sand-50`,
  dark: `${physical} bg-ink text-canvas hover:bg-ink/90 shadow-[3px_3px_0_#E84A2A] hover:shadow-[2px_2px_0_#E84A2A]`,
  danger: `${physical} bg-surface text-danger hover:bg-brand-50`,
  ghost: "text-ink underline-offset-4 hover:underline",
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
  className,
  children,
}: {
  href: string;
  variant?: Variant;
  block?: boolean;
  className?: string;
  children: ReactNode;
}) {
  return (
    <Link href={href} className={clsx(buttonClass(variant, block), className)}>
      {children}
    </Link>
  );
}
