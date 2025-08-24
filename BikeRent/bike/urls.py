from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .views import BikeView, StationView, BikeDetailView

urlpatterns = [
    path("bikes/<int:pk>/", BikeDetailView.as_view(), name="bike-view"),
    path("bikes/", BikeView.as_view(), name="bike-list"),
    path("stations/", StationView.as_view(), name="station-list"),
]