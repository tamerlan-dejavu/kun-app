import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { getPublicGathering } from "@/lib/api/server";
import { PageHeader } from "@/components/layout/PageHeader";
import { ChatView } from "@/components/chat/ChatView";

const READ_ONLY_AFTER_MS = 24 * 3600_000; // чат только для чтения через сутки после начала

// /g/<slug>/chat — только участники (проверяет и API, и WebSocket)
export default async function ChatPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const g = await getPublicGathering(slug);
  if (!g) notFound();
  const readOnly = Date.now() > new Date(g.starts_at).getTime() + READ_ONLY_AFTER_MS;

  return (
    <>
      <PageHeader title={`${t("chat.title")} · ${g.title}`} backHref={`/g/${slug}`} />
      <ChatView gatheringId={g.id} readOnly={readOnly} />
    </>
  );
}
