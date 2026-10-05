from django.urls import path

from . import views

urlpatterns = [
    path("me/notifications/settings", views.NotificationSettingsView.as_view()),
    path("me/push-subscriptions", views.PushSubscriptionView.as_view()),
    path("telegram/link", views.TelegramLinkView.as_view()),
    path("telegram/webhook", views.TelegramWebhookView.as_view()),
]
