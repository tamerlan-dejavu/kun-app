import { t } from "@/i18n";
import { SoonPage } from "@/components/layout/SoonPage";

// /profile — свой профиль. Вместе с входом и онбордингом.
export default function MyProfilePage() {
  return <SoonPage title={t("nav.profile")} />;
}
