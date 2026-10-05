import { DeleteAccount } from "@/components/settings/DeleteAccount";
import { NotificationToggles } from "@/components/settings/NotificationToggles";
import { PushConnect } from "@/components/settings/PushConnect";
import { StudentBadgeForm } from "@/components/settings/StudentBadgeForm";
import { TelegramConnect } from "@/components/settings/TelegramConnect";

// /settings — уведомления, Telegram, значок студента, удаление аккаунта.
export default function SettingsPage() {
  return (
    <div className="space-y-6 p-4">
      <NotificationToggles />
      <PushConnect />
      <TelegramConnect />
      <StudentBadgeForm />
      <DeleteAccount />
    </div>
  );
}
