"use client";

import { t } from "@/i18n";
import { Button } from "./Button";

// «Ошибка»: с кнопкой «Повторить».
export function ErrorState({ message, onRetry }: { message?: string; onRetry?: () => void }) {
  return (
    <div role="alert" className="card flex flex-col items-start gap-4 border-danger p-8">
      <p className="meta text-danger">ERROR</p>
      <p className="text-lg font-semibold">{message ?? t("common.error")}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          {t("common.retry")}
        </Button>
      )}
    </div>
  );
}
