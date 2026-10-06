import { SiteShell } from "@/components/layout/SiteShell";
import { AdultConsentStep } from "@/components/onboarding/AdultConsentStep";
import { InterestsPicker } from "@/components/onboarding/InterestsPicker";
import { NamePhotoStep } from "@/components/onboarding/NamePhotoStep";

// /onboarding — 18+, согласия, имя, фото, интересы. TODO: экран.
export default function OnboardingPage() {
  return (
    <SiteShell>
      <AdultConsentStep />
      <NamePhotoStep />
      <InterestsPicker />
    </SiteShell>
  );
}
