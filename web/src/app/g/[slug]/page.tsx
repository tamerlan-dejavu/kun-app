import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { getPublicGathering, hasSession } from "@/lib/api/server";
import { formatStartsAt } from "@/lib/datetime";
import { PageHeader } from "@/components/layout/PageHeader";
import { GatheringHeader } from "@/components/gathering/GatheringHeader";
import { GuestPanel } from "@/components/gathering/GuestPanel";
import { MemberPanel } from "@/components/gathering/MemberPanel";

type Props = { params: Promise<{ slug: string }> };

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

// /g/<slug>: шапка рендерится на сервере для всех; дальше — гостю или участнику
export default async function GatheringPage({ params }: Props) {
  const { slug } = await params;
  const [g, loggedIn] = await Promise.all([getPublicGathering(slug), hasSession()]);
  if (!g) notFound();

  return (
    <>
      <PageHeader title={g.category.name} backHref={loggedIn ? "/feed" : "/"} />
      <div className="px-4 pb-10">
        <GatheringHeader g={g} />
        {loggedIn ? <MemberPanel id={g.id} /> : <GuestPanel slug={g.slug} title={g.title} />}
      </div>
    </>
  );
}
