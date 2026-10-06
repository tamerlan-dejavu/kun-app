import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { ProfileView } from "@/components/profile/ProfileView";

export const metadata: Metadata = { title: "Профиль" };

// /profile — свой профиль. Редактирование — вместе с онбордингом (вход по телефону).
export default function MyProfilePage() {
  return (
    <>
      <PageTitle title={t("profile.title")} />
      <ProfileView />
    </>
  );
}
