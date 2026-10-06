import { existsSync } from "node:fs";
import { join } from "node:path";
import clsx from "clsx";
import type { PhotoSlot } from "@/content/photos";

// Серверный компонент: если файл лежит в public/photos — показываем фото (ч/б, контраст),
// иначе — рамку-плейсхолдер с подписью, что сюда снять.
export function CityPhoto({ slot, className, priority }: { slot: PhotoSlot; className?: string; priority?: boolean }) {
  const exists = existsSync(join(process.cwd(), "public", "photos", slot.file));
  return (
    <figure className={clsx("relative border-2 border-ink bg-sand-100 shadow-card", slot.aspect, className)}>
      {exists ? (
        // eslint-disable-next-line @next/next/no-img-element -- локальный файл из public/photos
        <img
          src={`/photos/${slot.file}`}
          alt={slot.caption}
          loading={priority ? "eager" : "lazy"}
          className="h-full w-full object-cover contrast-125 grayscale"
        />
      ) : (
        <div className="flex h-full w-full flex-col justify-between bg-[repeating-linear-gradient(135deg,transparent_0_14px,rgba(17,17,17,0.07)_14px_15px)] p-4">
          <span className="meta">ФОТО · {slot.file}</span>
          <span className="meta max-w-[24ch] normal-case text-ink-muted">{slot.hint}</span>
        </div>
      )}
      <figcaption className="meta absolute -bottom-3 left-3 border-2 border-ink bg-canvas px-2 py-0.5">
        {slot.caption}
      </figcaption>
    </figure>
  );
}
