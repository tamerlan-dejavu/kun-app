from django.urls import path

from . import views

urlpatterns = [
    path("places/search", views.PlaceSearchView.as_view()),
]
