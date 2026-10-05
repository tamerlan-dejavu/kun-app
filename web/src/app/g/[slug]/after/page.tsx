import { AttendanceButton } from "@/components/after/AttendanceButton";
import { RatingForm } from "@/components/after/RatingForm";

// /g/<slug>/after — «Я пришёл» и оценки участников.
export default function AfterPage() {
  return (
    <main className="mx-auto max-w-app p-4">
      <AttendanceButton />
      <RatingForm />
    </main>
  );
}
