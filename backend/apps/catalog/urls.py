from django.urls import path

from . import views

urlpatterns = [
    path("catalog/categories", views.CategoryListView.as_view()),
    path("catalog/interests", views.InterestListView.as_view()),
]
