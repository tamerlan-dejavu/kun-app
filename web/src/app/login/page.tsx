import type { Metadata } from "next";
import { t } from "@/i18n";
import { ButtonLink } from "@/components/ui/Button";
import { SiteShell } from "@/components/layout/SiteShell";

export const metadata: Metadata = { title: "Вход" };

type Props = { searchParams: Promise<{ next?: string }> };

// Только относительные пути внутри сайта — не даём увести на чужой домен
const safeNext = (next?: string) => (next?.startsWith("/") && !next.startsWith("//") ? next : "/feed");

// /login — номер телефона -> код (раздел 3.2 ТЗ). Пока вход по телефону в работе,
// в dev — вход демо-пользователем через браузерный API Django.
export default async function LoginPage({ searchParams }: Props) {
  const next = safeNext((await searchParams).next);
  const dev = process.env.NODE_ENV === "development";
  return (
    <SiteShell>
      <section className="card mx-auto max-w-md space-y-4 p-8 md:my-10">
        <h1 className="text-2xl">{t("login.title")}</h1>
        <p className="text-ink-muted">{t("login.soon")}</p>
        {dev && (
          <>
            <ButtonLink href={`/api/v1/auth/dev/login/?next=${encodeURIComponent(next)}`} block>
              {t("login.dev")}
            </ButtonLink>
            <p className="text-center text-sm text-ink-muted">{t("login.devHint")}</p>
          </>
        )}
      </section>
    </SiteShell>
  );
}
