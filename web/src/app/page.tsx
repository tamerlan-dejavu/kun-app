import { getCity } from "@/lib/api/city";
import { SiteShell } from "@/components/layout/SiteShell";
import { CityStrip } from "@/components/home/CityStrip";
import { FinalSection } from "@/components/home/FinalSection";
import { Hero } from "@/components/home/Hero";
import { HowSection } from "@/components/home/HowSection";
import { MapSection } from "@/components/home/MapSection";
import { PeopleSection } from "@/components/home/PeopleSection";
import { PlacesSection } from "@/components/home/PlacesSection";
import { SafetySection } from "@/components/home/SafetySection";
import { TodaySection } from "@/components/home/TodaySection";

// / — главная: город как интерфейс. Данные — живые, из /public/city (без личных данных).
export default async function HomePage() {
  const city = await getCity();
  return (
    <SiteShell contained={false}>
      <Hero />
      <CityStrip city={city} />
      <PlacesSection places={city?.places ?? []} />
      <TodaySection city={city} />
      <PeopleSection people={city?.people ?? []} />
      <MapSection points={city?.points ?? []} />
      <HowSection />
      <SafetySection />
      <FinalSection />
    </SiteShell>
  );
}
