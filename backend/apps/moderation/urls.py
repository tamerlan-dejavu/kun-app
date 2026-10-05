from django.urls import path

from . import views

urlpatterns = [
    path("reports", views.ReportCreateView.as_view()),
    path("blocks", views.BlockCreateView.as_view()),
    path("blocks/<int:user_id>", views.BlockDeleteView.as_view()),
]
