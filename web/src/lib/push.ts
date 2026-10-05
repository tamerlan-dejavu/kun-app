// Подписка на веб-пуши: регистрация sw.js, PushManager.subscribe, POST /me/push-subscriptions.
// На iPhone пуши работают только в PWA, добавленной на главный экран (iOS 16.4+).
export async function subscribeToPush(): Promise<void> {
  throw new Error("not implemented");
}

export function isIosNotStandalone(): boolean {
  // TODO: подсказка «Добавь на главный экран» + предложение Telegram-бота
  return false;
}
