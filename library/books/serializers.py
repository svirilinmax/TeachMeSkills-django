from rest_framework import serializers
from .models import Book, Author

class AuthorShortSerializer(serializers.ModelSerializer):
    """Ускороченный сериализатор для автора (только основные поля)"""
    class Meta:
        model = Author
        fields = ["id", "name", "is_active"]

class BookSerializer(serializers.ModelSerializer):
    author = AuthorShortSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "quantity", "author"]


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_book_count(self, obj):
        return obj.books.count()

    def get_is_owner(self, obj):
        """Добавляем поле, показывающее, является ли текущий пользователь владельцем"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False

    class Meta:
        model = Author
        fields = ["id", "name", "is_active", "books", "book_count", "is_owner"]
        read_only_fields = ["is_owner"]