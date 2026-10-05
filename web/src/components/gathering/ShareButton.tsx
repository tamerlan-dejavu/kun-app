"use client";

import { useState } from "react";
import { t } from "@/i18n";
import { shareLink } from "@/lib/share";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";

export function ShareButton({ slug, title }: { slug: string; title: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <>
      <Button
        variant="secondary"
        block
        onClick={async () => {
          const result = await shareLink(`${location.origin}/g/${slug}`, title);
          setCopied(result === "copied");
        }}
      >
        <Icon name="share" />
        {t("gathering.share")}
      </Button>
      <p role="status" aria-live="polite" className="text-center text-sm text-ink-muted">
        {copied ? t("gathering.copied") : ""}
      </p>
    </>
  );
}
