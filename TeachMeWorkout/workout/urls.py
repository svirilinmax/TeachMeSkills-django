from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CoachViewSet, ExerciseViewSet, TrainingPlanViewSet

router = DefaultRouter()
router.register(r"coaches", CoachViewSet, basename="coach")
router.register(r"plans", TrainingPlanViewSet, basename="trainingplan")
router.register(r"exercises", ExerciseViewSet, basename="exercise")

urlpatterns = [
    path("", include(router.urls)),
]
