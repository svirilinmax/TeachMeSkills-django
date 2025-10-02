from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"author", AuthorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
