import { SiteShell } from "@/components/layout/SiteShell";
import { Categories } from "@/components/landing/Categories";
import { FinalCta } from "@/components/landing/FinalCta";
import { Hero } from "@/components/landing/Hero";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Safety } from "@/components/landing/Safety";

// / — лендинг: полосы на всю ширину, общие шапка и подвал сайта
export default function LandingPage() {
  return (
    <SiteShell contained={false}>
      <Hero />
      <HowItWorks />
      <Categories />
      <Safety />
      <FinalCta />
    </SiteShell>
  );
}
