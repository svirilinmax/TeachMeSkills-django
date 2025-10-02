from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieListView, ScheduleViewSet

router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedule")

urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("api/", include(router.urls)),
]
