from django.urls import path

from . import views

urlpatterns = [
    path("auth/phone/request", views.PhoneRequestView.as_view()),
    path("auth/phone/verify", views.PhoneVerifyView.as_view()),
    path("auth/logout", views.LogoutView.as_view()),
    path("me", views.MeView.as_view()),
    path("me/photo", views.MePhotoView.as_view()),
    path("users/<int:pk>", views.UserDetailView.as_view()),
]
