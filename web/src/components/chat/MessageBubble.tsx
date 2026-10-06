import clsx from "clsx";
import { t } from "@/i18n";
import type { Message } from "@/lib/api/types";
import { formatTime } from "@/lib/datetime";
import { Avatar } from "@/components/ui/Avatar";

// TODO: жалоба на сообщение долгим нажатием (раздел 3.4) — вместе с POST /reports.
export function MessageBubble({ message, mine }: { message: Message; mine: boolean }) {
  return (
    <div className={clsx("flex items-end gap-2", mine && "flex-row-reverse")}>
      {!mine && <Avatar size="sm" name={message.author?.name} photo={message.author?.photo} />}
      <div
        className={clsx(
          "max-w-[78%] rounded-card px-4 py-2.5",
          mine ? "rounded-br-md bg-brand-100" : "rounded-bl-md bg-surface shadow-card",
        )}
      >
        {!mine && <p className="text-xs font-semibold text-brand-700">{message.author?.name}</p>}
        <p className={clsx("whitespace-pre-wrap break-words", message.is_hidden && "italic text-ink-muted")}>
          {message.is_hidden ? t("chat.hidden") : message.text}
        </p>
        <p className="mt-0.5 text-right text-[11px] text-ink-muted">{formatTime(message.created_at)}</p>
      </div>
    </div>
  );
}
