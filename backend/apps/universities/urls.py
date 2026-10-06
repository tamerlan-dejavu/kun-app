from django.urls import path

from . import views

urlpatterns = [
    path("catalog/universities", views.UniversityListView.as_view()),
]
