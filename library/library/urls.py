from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)  # POST /api/token/        -> access + refresh
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)  # POST /api/token/refresh -> новый access (и refresh если ROTATE)
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)  # POST /api/token/verify  -> проверить access/refresh

jwt_urlpatterns = (
    [
        path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    ],
    "jwt",
)

api_patterns = [
    path("", include("books.urls")),
    path("auth/jwt/", include(jwt_urlpatterns, namespace="jwt")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((api_patterns, "api"), namespace="api")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
