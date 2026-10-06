import { SoonPage } from "@/components/layout/SoonPage";

// /u/<id> — чужой профиль. Ждёт GET /users/{id} (публичный профиль без телефона).
export default function UserProfilePage() {
  return <SoonPage title="Профиль" />;
}
