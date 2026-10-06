import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { getPublicGathering, hasSession } from "@/lib/api/server";
import { formatStartsAt } from "@/lib/datetime";
import { parseSource } from "@/lib/source";
import { PageTitle } from "@/components/layout/PageTitle";
import { SiteShell } from "@/components/layout/SiteShell";
import { GatheringHeader } from "@/components/gathering/GatheringHeader";
import { GuestPanel } from "@/components/gathering/GuestPanel";
import { MemberDetails } from "@/components/gathering/MemberDetails";
import { MemberSidebar } from "@/components/gathering/MemberSidebar";

type Props = { params: Promise<{ slug: string }>; searchParams: Promise<{ src?: string }> };

// Open Graph: карточка-превью в Telegram и WhatsApp (раздел 3.1 ТЗ)
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const g = await getPublicGathering((await params).slug);
  if (!g) return { title: t("gathering.notFound") };
  const description = [
    formatStartsAt(g.starts_at),
    g.district,
    t("gathering.going", { n: g.participants_count, m: g.seats }),
  ]
    .filter(Boolean)
    .join(" · ");
  return {
    title: g.title,
    description,
    openGraph: { title: `${g.category.emoji} ${g.title}`, description, type: "website" },
  };
}

// /g/<slug>: шапка сбора — на сервере для всех; на десктопе две колонки
export default async function GatheringPage({ params, searchParams }: Props) {
  const { slug } = await params;
  const source = parseSource((await searchParams).src);
  const [g, loggedIn] = await Promise.all([getPublicGathering(slug), hasSession()]);
  if (!g) notFound();

  return (
    <SiteShell>
      <PageTitle title={g.category.name} backHref={loggedIn ? "/feed" : "/"} />
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_380px] lg:items-start">
        <div className="space-y-6">
          <GatheringHeader g={g} />
          {loggedIn && <MemberDetails id={g.id} />}
        </div>
        <aside className="lg:sticky lg:top-24">
          {loggedIn ? <MemberSidebar id={g.id} source={source} /> : <GuestPanel slug={g.slug} title={g.title} />}
        </aside>
      </div>
    </SiteShell>
  );
}
