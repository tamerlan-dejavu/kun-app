"use client";

import { t } from "@/i18n";
import { Button } from "./Button";

// Состояние «ошибка» с кнопкой «Повторить».
export function ErrorState({ message, onRetry }: { message?: string; onRetry?: () => void }) {
  return (
    <div role="alert" className="flex flex-col items-center gap-4 px-6 py-14 text-center">
      <p>{message ?? t("common.error")}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          {t("common.retry")}
        </Button>
      )}
    </div>
  );
}
