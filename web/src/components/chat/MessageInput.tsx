"use client";

import { useState } from "react";
import { t } from "@/i18n";
import { Icon } from "@/components/ui/Icon";

const MAX = 1000;

export function MessageInput({
  onSend,
  error,
  pending,
}: {
  onSend: (text: string) => Promise<void>;
  error?: string;
  pending: boolean;
}) {
  const [text, setText] = useState("");

  const submit = async () => {
    const value = text.trim();
    if (!value || pending) return;
    try {
      await onSend(value);
      setText("");
    } catch {
      // текст ошибки показываем ниже, набранное не теряем
    }
  };

  return (
    <form
      className="border-t-2 border-ink bg-surface px-3 py-3 md:px-4"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
    >
      {error && (
        <p role="alert" className="px-1 pb-1 text-sm text-danger">
          {error}
        </p>
      )}
      <div className="flex items-end gap-2">
        <label htmlFor="chat-input" className="sr-only">
          {t("chat.placeholder")}
        </label>
        <textarea
          id="chat-input"
          rows={1}
          maxLength={MAX}
          value={text}
          placeholder={t("chat.placeholder")}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            // Enter — отправить, Shift+Enter — новая строка
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
          className="max-h-32 min-h-tap flex-1 resize-none rounded-button border-2 border-ink bg-canvas px-4 py-2.5"
        />
        <button
          type="submit"
          aria-label={t("chat.send")}
          disabled={!text.trim() || pending}
          className="flex h-tap w-11 shrink-0 items-center justify-center border-2 border-ink bg-brand text-ink shadow-sm transition-[transform,box-shadow] duration-100 active:translate-x-[3px] active:translate-y-[3px] active:shadow-none disabled:opacity-40"
        >
          <Icon name="send" />
        </button>
      </div>
    </form>
  );
}
