import type { Message } from "@/lib/api/types";

// WebSocket чата: /ws/gatherings/<id>/ (раздел 6 ТЗ). Отправка — через REST.
export type WsEvent =
  | { type: "message.new"; data: Message }
  | { type: "participant.joined" | "participant.left"; data: { user_id: number; name: string } }
  | { type: "gathering.updated" | "gathering.cancelled"; data: Record<string, unknown> }
  | { type: "pong" };

export type WsStatus = "connecting" | "open" | "closed" | "forbidden";

const CLOSE_CODES_FINAL = new Set([4401, 4403]); // не вошёл / не участник

/** Подключение с переподключением (backoff до 15 с). Возвращает функцию отключения. */
export function connectGathering(
  gatheringId: number,
  onEvent: (e: WsEvent) => void,
  onStatus?: (s: WsStatus) => void,
): () => void {
  let ws: WebSocket | null = null;
  let stopped = false;
  let attempt = 0;
  let ping: ReturnType<typeof setInterval> | undefined;

  const open = () => {
    onStatus?.("connecting");
    const proto = location.protocol === "https:" ? "wss" : "ws";
    ws = new WebSocket(`${proto}://${location.host}/ws/gatherings/${gatheringId}/`);
    ws.onopen = () => {
      attempt = 0;
      onStatus?.("open");
      ping = setInterval(() => ws?.send(JSON.stringify({ type: "ping" })), 25_000);
    };
    ws.onmessage = (e) => onEvent(JSON.parse(e.data) as WsEvent);
    ws.onclose = (e) => {
      clearInterval(ping);
      if (stopped) return;
      if (CLOSE_CODES_FINAL.has(e.code)) {
        onStatus?.("forbidden"); // переподключаться бессмысленно
        return;
      }
      onStatus?.("closed");
      setTimeout(open, Math.min(15_000, 1000 * 2 ** attempt++));
    };
  };

  open();
  return () => {
    stopped = true;
    clearInterval(ping);
    ws?.close();
  };
}
