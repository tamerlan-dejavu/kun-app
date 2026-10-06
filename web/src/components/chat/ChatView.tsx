"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useMemo, useRef, useState } from "react";
import { t } from "@/i18n";
import type { Message } from "@/lib/api/types";
import { useMessages, useSendMessage } from "@/lib/queries/chat";
import { keys } from "@/lib/queries/keys";
import { useMe } from "@/lib/queries/me";
import { connectGathering, type WsStatus } from "@/lib/ws";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { SkeletonList } from "@/components/ui/Skeleton";
import { MessageBubble } from "./MessageBubble";
import { MessageInput } from "./MessageInput";
import { SystemMessage } from "./SystemMessage";

type Props = { gatheringId: number; readOnly: boolean };

export function ChatView({ gatheringId, readOnly }: Props) {
  const me = useMe();
  const history = useMessages(gatheringId);
  const send = useSendMessage(gatheringId);
  const qc = useQueryClient();
  const [live, setLive] = useState<Message[]>([]);
  const [status, setStatus] = useState<WsStatus>("connecting");
  const scroller = useRef<HTMLDivElement>(null);

  // Новые сообщения — по WebSocket; изменения сбора — освежаем его карточку
  useEffect(
    () =>
      connectGathering(
        gatheringId,
        (event) => {
          if (event.type === "message.new") setLive((prev) => [...prev, event.data]);
          if (event.type === "gathering.updated" || event.type === "gathering.cancelled") {
            qc.invalidateQueries({ queryKey: keys.gathering(gatheringId) });
          }
        },
        setStatus,
      ),
    [gatheringId, qc],
  );

  // История приходит «новые сверху» — разворачиваем и добавляем живые без дублей
  const messages = useMemo(() => {
    const older = (history.data?.pages ?? []).flatMap((p) => p.results).reverse();
    const seen = new Set(older.map((m) => m.id));
    return [...older, ...live.filter((m) => !seen.has(m.id) && seen.add(m.id))];
  }, [history.data, live]);

  // Новое сообщение — прокручиваем ленту чата вниз (только её, не страницу)
  useEffect(() => {
    const el = scroller.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages.length]);

  if (status === "forbidden" || (history.isError && history.error.status === 403)) {
    return <ErrorState message={t("chat.forbidden")} />;
  }
  if (history.isPending) return <SkeletonList count={4} className="h-14" />;
  if (history.isError) {
    return <ErrorState message={history.error.message} onRetry={() => history.refetch()} />;
  }

  const onSend = async (text: string) => {
    const message = await send.mutateAsync(text);
    // Если сокет сейчас переподключается — показываем своё сразу (дубли отсеются по id)
    setLive((prev) => [...prev, message]);
  };

  return (
    <div className="flex h-[calc(100dvh-180px)] flex-col overflow-hidden rounded-card bg-surface shadow-card md:h-[calc(100dvh-230px)]">
      {status === "closed" && (
        <p role="status" className="bg-sand-100 px-4 py-2 text-center text-sm text-sand-800">
          {t("chat.reconnecting")}
        </p>
      )}
      <div
        ref={scroller}
        className="flex-1 space-y-2 overflow-y-auto bg-canvas px-4 py-4 md:px-6"
        aria-live="polite"
        aria-relevant="additions"
      >
        {history.hasNextPage && (
          <Button
            variant="ghost"
            block
            disabled={history.isFetchingNextPage}
            onClick={() => history.fetchNextPage()}
          >
            {t("chat.older")}
          </Button>
        )}
        {messages.length === 0 && <EmptyState title={t("chat.empty")} />}
        {messages.map((m) =>
          m.kind === "system" ? (
            <SystemMessage key={m.id} message={m} />
          ) : (
            <MessageBubble key={m.id} message={m} mine={m.author?.id === me.data?.id} />
          ),
        )}
      </div>
      {readOnly ? (
        <p className="border-t border-line bg-surface px-4 py-4 text-center text-sm text-ink-muted">
          {t("chat.readOnly")}
        </p>
      ) : (
        <MessageInput onSend={onSend} error={send.error?.message} pending={send.isPending} />
      )}
    </div>
  );
}
