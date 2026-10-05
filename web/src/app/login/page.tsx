import { CodeForm } from "@/components/auth/CodeForm";
import { PhoneForm } from "@/components/auth/PhoneForm";

// /login — номер телефона -> код. TODO: шаги в одном клиентском компоненте, редирект на ?next.
export default function LoginPage() {
  return (
    <main className="mx-auto max-w-app p-4">
      <PhoneForm />
      <CodeForm />
    </main>
  );
}
