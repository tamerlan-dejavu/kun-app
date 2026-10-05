from django.urls import path

from . import views

urlpatterns = [
    path("request", views.StudentRequestView.as_view()),
    path("verify", views.StudentVerifyView.as_view()),
]
