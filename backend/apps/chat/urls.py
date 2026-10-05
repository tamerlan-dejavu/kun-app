from django.urls import path

from . import views

urlpatterns = [
    path("gatherings/<int:pk>/messages", views.MessageListCreateView.as_view()),
]
