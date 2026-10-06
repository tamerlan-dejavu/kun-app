"use client";

import clsx from "clsx";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { t } from "@/i18n";
import { useMe } from "@/lib/queries/me";
import { useInterests, useUniversities, useUpdateMe, useUploadPhoto } from "@/lib/queries/profile";
import { Avatar } from "@/components/ui/Avatar";
import { Button, ButtonLink, buttonClass } from "@/components/ui/Button";
import { Chip } from "@/components/ui/Chip";
import { ErrorState } from "@/components/ui/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";

const MIN = 3;
const MAX = 5;
const field = "w-full min-h-tap rounded-button border-2 border-ink bg-surface px-4 py-2.5";

export function ProfileEditForm() {
  const router = useRouter();
  const me = useMe();
  const universities = useUniversities();
  const interests = useInterests();
  const update = useUpdateMe();
  const photo = useUploadPhoto();

  const [name, setName] = useState("");
  const [university, setUniversity] = useState<string>("");
  const [picked, setPicked] = useState<string[]>([]);

  // Заполняем форму один раз, когда профиль загрузился. Повторно — нельзя: после загрузки фото
  // профиль в кэше обновляется, и это затёрло бы несохранённые правки имени, вуза и интересов.
  const filled = useRef(false);
  useEffect(() => {
    if (!me.data || filled.current) return;
    filled.current = true;
    setName(me.data.name);
    setUniversity(me.data.university_id ? String(me.data.university_id) : "");
    setPicked(me.data.interests.map((i) => i.slug));
  }, [me.data]);

  if (me.isPending || universities.isPending || interests.isPending) return <Skeleton className="h-96" />;
  if (me.isError) return <ErrorState message={me.error.message} onRetry={() => me.refetch()} />;

  const toggle = (slug: string) =>
    setPicked((p) => (p.includes(slug) ? p.filter((s) => s !== slug) : p.length < MAX ? [...p, slug] : p));
  const valid = name.trim().length > 0 && picked.length >= MIN && picked.length <= MAX;

  return (
    <form
      className="grid gap-6 lg:grid-cols-[320px_minmax(0,1fr)] lg:items-start"
      onSubmit={(e) => {
        e.preventDefault();
        update.mutate(
          { name: name.trim(), university: university ? Number(university) : null, interests: picked },
          { onSuccess: () => router.push("/profile") },
        );
      }}
    >
      <section className="card space-y-4 p-6">
        <h2 className="text-base">{t("editProfile.photo")}</h2>
        <Avatar name={me.data.name} photo={me.data.photo} size="lg" />
        {/* Своя кнопка вместо системной «Choose File»: подпись на языке сайта, а не браузера.
            Инпут визуально скрыт, но остаётся доступным с клавиатуры (фокус — на подписи). */}
        <label className={clsx(buttonClass("secondary"), "cursor-pointer focus-within:outline focus-within:outline-2 focus-within:outline-brand-600")}>
          {t("editProfile.photoChange")}
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            className="sr-only"
            disabled={photo.isPending}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) photo.mutate(file);
              e.target.value = "";
            }}
          />
        </label>
        <p className="text-sm text-ink-muted">{t("editProfile.photoHint")}</p>
        <p role="status" aria-live="polite" className="text-sm">
          {photo.isPending && t("editProfile.photoUploading")}
        </p>
        {photo.isError && (
          <p role="alert" className="text-sm text-danger">
            {photo.error.message}
          </p>
        )}
      </section>

      <section className="card space-y-6 p-6 md:p-8">
        <label className="block">
          <span className="mb-1.5 block font-semibold">{t("editProfile.name")}</span>
          <input value={name} maxLength={50} required onChange={(e) => setName(e.target.value)} className={field} />
        </label>

        <label className="block">
          <span className="mb-1.5 block font-semibold">{t("editProfile.university")}</span>
          <select value={university} onChange={(e) => setUniversity(e.target.value)} className={field}>
            <option value="">{t("editProfile.universityNone")}</option>
            {universities.data?.map((u) => (
              <option key={u.id} value={u.id}>
                {u.short_name} — {u.name}
              </option>
            ))}
          </select>
        </label>

        <fieldset>
          <legend className="mb-1.5 font-semibold">{t("editProfile.interests")}</legend>
          <p className="mb-3 text-sm text-ink-muted">{t("editProfile.interestsHint", { n: picked.length })}</p>
          <div className="flex flex-wrap gap-2">
            {interests.data?.map((i) => (
              <Chip key={i.slug} selected={picked.includes(i.slug)} onClick={() => toggle(i.slug)}>
                {i.name}
              </Chip>
            ))}
          </div>
        </fieldset>

        {update.isError && (
          <p role="alert" className="text-sm text-danger">
            {update.error.message}
          </p>
        )}
        <div className="flex flex-col gap-3 sm:flex-row">
          <Button type="submit" disabled={!valid || update.isPending} className="sm:px-10">
            {t("editProfile.save")}
          </Button>
          <ButtonLink href="/profile" variant="ghost">
            {t("editProfile.cancel")}
          </ButtonLink>
        </div>
      </section>
    </form>
  );
}
