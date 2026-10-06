import Link from "next/link";
import { t } from "@/i18n";

// Логотип: KUN жирным гротеском + терракотовый квадрат — «точка на карте».
export function Logo({ href }: { href: string }) {
  return (
    <Link href={href} className="flex items-center gap-1.5 font-heading text-2xl font-black tracking-tighter">
      KUN
      <span aria-hidden className="inline-block h-2.5 w-2.5 bg-brand" />
    </Link>
  );
}

// Координаты центра Алматы — техническая метка в шапке (только на широких экранах).
export function Coords() {
  return (
    <p aria-label={t("nav.coordsLabel")} className="meta hidden flex-col text-right leading-tight text-ink-muted xl:flex">
      <span className="font-bold text-ink">Almaty</span>
      <span>43.2389° N</span>
      <span>76.8897° E</span>
    </p>
  );
}
