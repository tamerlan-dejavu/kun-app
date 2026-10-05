import { t, type MessageKey } from "@/i18n";
import type { Message } from "@/lib/api/types";

// Присоединился / вышел / сбор изменён / отменён / сменился создатель.
export function SystemMessage({ message }: { message: Message }) {
  const name = String((message.payload as { name?: string })?.name ?? "");
  const text = t(`chat.${message.system_event}` as MessageKey, { name });
  return <p className="py-1 text-center text-xs text-ink-muted">{text}</p>;
}
