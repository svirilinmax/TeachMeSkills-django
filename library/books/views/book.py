from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Book
from ..serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Полный CRUD для Book:
    - GET /books/         список (с поиском и сортировкой)
    - POST /books/        создать
    - GET /books/{id}/    получить
    - PUT/PATCH /books/{id}/ обновить
    - DELETE /books/{id}/ удалить
    """

    queryset = Book.objects.order_by("id")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["id", "title"]
