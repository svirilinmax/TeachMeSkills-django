from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieListView, ScheduleListView, ScheduleViewSet

router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedule")

urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("schedule/", ScheduleListView.as_view(), name="schedule-list"),
    path("api/", include(router.urls)),
]
