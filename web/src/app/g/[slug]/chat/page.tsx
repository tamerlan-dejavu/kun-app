import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { getPublicGathering } from "@/lib/api/server";
import { PageTitle } from "@/components/layout/PageTitle";
import { SiteShell } from "@/components/layout/SiteShell";
import { ChatView } from "@/components/chat/ChatView";

const READ_ONLY_AFTER_MS = 24 * 3600_000; // чат только для чтения через сутки после начала

// /g/<slug>/chat — только участники (проверяет и API, и WebSocket).
// Без подвала и нижних вкладок: чату нужна вся высота экрана.
export default async function ChatPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const g = await getPublicGathering(slug);
  if (!g) notFound();
  const readOnly = Date.now() > new Date(g.starts_at).getTime() + READ_ONLY_AFTER_MS;

  return (
    <SiteShell footer={false} bottomNav={false}>
      <div className="mx-auto max-w-3xl">
        <PageTitle title={`${t("chat.title")} · ${g.title}`} backHref={`/g/${slug}`} />
        <ChatView gatheringId={g.id} readOnly={readOnly} />
      </div>
    </SiteShell>
  );
}
