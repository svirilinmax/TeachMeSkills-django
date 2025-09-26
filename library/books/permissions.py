from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermission(BasePermission):
    """
    Permission для проверки, является ли user владельцем автора.
    - Чтение: разрешено всем аутентифицированным пользователям
    - Запись: разрешено только владельцу автора
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False
