import { Categories } from "@/components/landing/Categories";
import { FinalCta } from "@/components/landing/FinalCta";
import { Hero } from "@/components/landing/Hero";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Safety } from "@/components/landing/Safety";
import { SiteFooter } from "@/components/landing/SiteFooter";
import { SiteHeader } from "@/components/landing/SiteHeader";

// / — лендинг: адаптивный, на десктопе на всю ширину (SSR, без клиентского JS)
export default function LandingPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <HowItWorks />
        <Categories />
        <Safety />
        <FinalCta />
      </main>
      <SiteFooter />
    </>
  );
}
