"use client";

import { useRef, useState } from "react";
import { t, type MessageKey } from "@/i18n";
import { useReport } from "@/lib/queries/profile";
import { Button } from "@/components/ui/Button";

const REASONS = ["spam", "harassment", "inappropriate", "danger", "underage", "fake", "no_show", "other"] as const;
type Reason = (typeof REASONS)[number];

// Жалоба на пользователя, сбор или сообщение. Нативный <dialog>: фокус, Esc и затемнение — из браузера.
export function ReportDialog({
  targetType,
  targetId,
  trigger,
}: {
  targetType: "user" | "gathering" | "message";
  targetId: number;
  trigger: (open: () => void) => React.ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const report = useReport();
  const [reason, setReason] = useState<Reason | null>(null);
  const [text, setText] = useState("");

  const close = () => {
    ref.current?.close();
    report.reset();
    setReason(null);
    setText("");
  };

  return (
    <>
      {trigger(() => ref.current?.showModal())}
      <dialog
        ref={ref}
        aria-labelledby="report-title"
        className="card w-[min(92vw,480px)] p-0 text-ink shadow-lg backdrop:bg-ink/50"
        onClose={close}
      >
        <form
          method="dialog"
          className="space-y-4 p-6"
          onSubmit={(e) => {
            e.preventDefault();
            if (reason) report.mutate({ target_type: targetType, target_id: targetId, reason, text });
          }}
        >
          <h2 id="report-title" className="text-2xl uppercase">
            {t("report.title")}
          </h2>
          {report.isSuccess ? (
            <>
              <p role="status" className="font-semibold text-success">
                {t("report.sent")}
              </p>
              <Button type="button" block onClick={close}>
                OK
              </Button>
            </>
          ) : (
            <>
              <p className="text-sm text-ink-muted">{t("report.lead")}</p>
              <fieldset>
                <legend className="mb-2 font-semibold">{t("report.reason")}</legend>
                <div className="space-y-1">
                  {REASONS.map((r) => (
                    <label key={r} className="flex min-h-tap cursor-pointer items-center gap-3 rounded-button px-2 hover:bg-sand-50">
                      <input
                        type="radio"
                        name="reason"
                        value={r}
                        checked={reason === r}
                        onChange={() => setReason(r)}
                        className="h-5 w-5 accent-brand"
                      />
                      {t(`report.reasons.${r}` as MessageKey)}
                    </label>
                  ))}
                </div>
              </fieldset>
              <label className="block">
                <span className="mb-1 block text-sm font-semibold">{t("report.text")}</span>
                <textarea
                  value={text}
                  maxLength={1000}
                  rows={3}
                  onChange={(e) => setText(e.target.value)}
                  className="w-full rounded-button border-2 border-ink bg-canvas px-4 py-2.5"
                />
              </label>
              {report.isError && (
                <p role="alert" className="text-sm text-danger">
                  {report.error.message}
                </p>
              )}
              <div className="flex gap-3">
                <Button type="button" variant="secondary" block onClick={close}>
                  {t("report.cancel")}
                </Button>
                <Button type="submit" block disabled={!reason || report.isPending}>
                  {t("report.send")}
                </Button>
              </div>
            </>
          )}
        </form>
      </dialog>
    </>
  );
}
