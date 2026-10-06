import { SiteShell } from "@/components/layout/SiteShell";
import { AttendanceButton } from "@/components/after/AttendanceButton";
import { RatingForm } from "@/components/after/RatingForm";

// /g/<slug>/after — «Я пришёл» и оценки участников. TODO: экран.
export default function AfterPage() {
  return (
    <SiteShell>
      <AttendanceButton />
      <RatingForm />
    </SiteShell>
  );
}
