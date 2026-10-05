import { AdultConsentStep } from "@/components/onboarding/AdultConsentStep";
import { InterestsPicker } from "@/components/onboarding/InterestsPicker";
import { NamePhotoStep } from "@/components/onboarding/NamePhotoStep";

// /onboarding — 18+, согласия, имя, фото, интересы.
export default function OnboardingPage() {
  return (
    <main className="mx-auto max-w-app p-4">
      <AdultConsentStep />
      <NamePhotoStep />
      <InterestsPicker />
    </main>
  );
}
