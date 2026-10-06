from django.urls import path

from . import views

urlpatterns = [
    path("gatherings", views.GatheringListCreateView.as_view()),
    path("gatherings/<int:pk>", views.GatheringDetailView.as_view()),
    path("gatherings/<int:pk>/cancel", views.GatheringCancelView.as_view()),
    path("gatherings/<int:pk>/join", views.GatheringJoinView.as_view()),
    path("gatherings/<int:pk>/leave", views.GatheringLeaveView.as_view()),
    path("gatherings/<int:pk>/attendance", views.AttendanceView.as_view()),
    path("gatherings/<int:pk>/ratings", views.RatingsView.as_view()),
    path("me/gatherings", views.MyGatheringsView.as_view()),
    path("public/gatherings/<slug:slug>", views.PublicGatheringView.as_view()),
    path("public/city", views.PublicCityView.as_view()),
]
