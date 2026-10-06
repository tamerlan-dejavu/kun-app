import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { getPublicGathering } from "@/lib/api/server";
import { PageTitle } from "@/components/layout/PageTitle";
import { SiteShell } from "@/components/layout/SiteShell";
import { AfterView } from "@/components/after/AfterView";

export const metadata: Metadata = { title: "Как прошла встреча?" };

// /g/<slug>/after — сюда ведёт уведомление «Как прошла встреча?» (через 1 ч после начала)
export default async function AfterPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const g = await getPublicGathering(slug);
  if (!g) notFound();
  return (
    <SiteShell>
      <PageTitle title={t("after.title")} backHref={`/g/${slug}`} />
      <p className="-mt-4 mb-8 text-lg text-ink-muted md:-mt-6">{g.title}</p>
      <AfterView id={g.id} />
    </SiteShell>
  );
}
