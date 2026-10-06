import type { Metadata } from "next";
import { t } from "@/i18n";
import { PageTitle } from "@/components/layout/PageTitle";
import { ProfileEditForm } from "@/components/profile/ProfileEditForm";

export const metadata: Metadata = { title: "Редактировать профиль" };

export default function EditProfilePage() {
  return (
    <>
      <PageTitle title={t("editProfile.title")} backHref="/profile" />
      <ProfileEditForm />
    </>
  );
}
