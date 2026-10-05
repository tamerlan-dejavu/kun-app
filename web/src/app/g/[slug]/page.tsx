import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { GatheringHeader } from "@/components/gathering/GatheringHeader";
import { JoinButton } from "@/components/gathering/JoinButton";
import { ParticipantsList } from "@/components/gathering/ParticipantsList";
import { ShareButton } from "@/components/gathering/ShareButton";
import { getPublicGathering } from "@/lib/api/server";

type Props = { params: Promise<{ slug: string }> };

// Open Graph для превью в Telegram и WhatsApp.
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const g = await getPublicGathering(slug);
  if (!g) return {};
  // TODO: title, description «<время>, <район>, идут N из M», og:image
  return { title: g.title, openGraph: { title: g.title } };
}

// /g/<slug> — страница сбора: гость видит без имён, фото и точного адреса;
// участник — целиком (данные догружаются на клиенте после входа).
export default async function GatheringPage({ params }: Props) {
  const { slug } = await params;
  const g = await getPublicGathering(slug);
  if (!g) notFound();
  return (
    <main className="mx-auto max-w-app p-4">
      <GatheringHeader />
      <ParticipantsList />
      <JoinButton />
      <ShareButton />
    </main>
  );
}
