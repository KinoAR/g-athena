# Django Review App Url Configuration

from django.urls import path
from django.urls import include
from . import views

app_name = "reviews"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("<str:search>/searchresults/", views.SearchResultsView.as_view(), name="search"),
    path("<int:pk>/review/", views.ReviewView.as_view(), name="review"),
    path("<int:pk>/game/", views.GameView.as_view(), name="game")
]