import { Hero } from "@/components/landing/Hero";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Safety } from "@/components/landing/Safety";

// / — лендинг (SSR, LCP ≤ 2,5 с на 4G): без клиентского JS, только разметка
export default function LandingPage() {
  return (
    <main className="mx-auto max-w-app">
      <Hero />
      <HowItWorks />
      <Safety />
    </main>
  );
}
