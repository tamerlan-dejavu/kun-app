import { ProfileActions } from "@/components/profile/ProfileActions";
import { ProfileCard } from "@/components/profile/ProfileCard";

// /u/<id> — чужой профиль.
export default async function UserProfilePage({ params }: { params: Promise<{ id: string }> }) {
  const { id: _id } = await params;
  return (
    <>
      <ProfileCard />
      <ProfileActions />
    </>
  );
}
