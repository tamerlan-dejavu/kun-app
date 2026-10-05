// Service worker: веб-пуши и клик по уведомлению.
// TODO: кэш оболочки приложения (офлайн-страница).

self.addEventListener("push", (event) => {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title ?? "KUN", {
      body: data.body,
      icon: "/icons/icon-192.png",
      data: { url: data.url ?? "/feed" },
    }),
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url));
});
