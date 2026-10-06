import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { UserProfileView } from "@/components/profile/UserProfileView";

export const metadata: Metadata = { title: "Профиль" };

// /u/<id> — чужой профиль (только для вошедших; телефон не показывается)
export default async function UserProfilePage({ params }: { params: Promise<{ id: string }> }) {
  const id = Number((await params).id);
  if (!Number.isInteger(id) || id <= 0) notFound();
  return (
    <>
      <PageTitle title={t("profile.title")} />
      <UserProfileView id={id} />
    </>
  );
}
