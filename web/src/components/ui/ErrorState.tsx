"use client";

import { t } from "@/i18n";
import { Button } from "./Button";

// Состояние «ошибка» с кнопкой «Повторить».
export function ErrorState({ message, onRetry }: { message?: string; onRetry: () => void }) {
  return (
    <div role="alert" className="flex flex-col items-center gap-4 py-12 text-center">
      <p>{message ?? t("common.error")}</p>
      <Button onClick={onRetry}>{t("common.retry")}</Button>
    </div>
  );
}
