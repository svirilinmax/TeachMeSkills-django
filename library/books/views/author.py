import time

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Author
from ..permissions import AuthorPermission
from ..serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, AuthorPermission]
    serializer_class = AuthorSerializer
    queryset = Author.objects.filter(is_active=True).order_by("id")

    def get_permissions(self):
        """
        Custom permission handling for AuthorViewSet.

        Action-specific permissions:
        - list: IsAuthenticated (view list)
        - retrieve: IsAuthenticated + AuthorPermission (view own detail)
        - create: IsAuthenticated (create new)
        - update/partial_update/destroy: IsAuthenticated + AuthorPermission (modify own)

        Returns:
            List[BasePermission]: Permissions for current action
        """
        if self.action == "list":
            return [IsAuthenticated()]
        elif self.action == "retrieve":
            return [IsAuthenticated(), AuthorPermission()]
        elif self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), AuthorPermission()]  # Change only your own

    def list(self, request, *args, **kwargs):
        """
        Персональный кэш: у каждого пользователя свой ключ.
        Пример ключа в Redis: author_list_user_
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Cache key "per user ID"
        cache_key = f"author_list_user_{user.id}"
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        data = serializer.data

        cache.set(cache_key, data, timeout=120)
        return Response(data)

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, *args, **kwargs):
        time.sleep(1)
        return super().retrieve(request, *args, **kwargs)
