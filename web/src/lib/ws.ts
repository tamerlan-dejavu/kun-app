// WebSocket чата: /ws/gatherings/<id>/
// События: message.new, participant.joined, participant.left, gathering.updated, gathering.cancelled
export type WsEvent =
  | { type: "message.new"; data: unknown }
  | { type: "participant.joined"; data: unknown }
  | { type: "participant.left"; data: unknown }
  | { type: "gathering.updated"; data: unknown }
  | { type: "gathering.cancelled"; data: unknown };

export function connectGathering(_gatheringId: number, _onEvent: (e: WsEvent) => void): () => void {
  // TODO: переподключение с backoff, инвалидация кэша TanStack Query по событиям
  throw new Error("not implemented");
}
