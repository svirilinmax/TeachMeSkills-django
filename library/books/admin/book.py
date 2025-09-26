from django.contrib import admin
from django.contrib.auth import get_user_model
from ..models import Book

User = get_user_model()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'author_status', 'quantity')
    list_editable = ('quantity',)
    list_filter = ('author__is_active', 'quantity')
    search_fields = ('title', 'author__name')
    list_select_related = ('author',)


    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'quantity')
        }),
        ('Дополнительно', {
            'fields': (),
            'classes': ('collapse',)
        }),
    )

    def author_status(self, obj):
        if obj.author:
            return "Активен" if obj.author.is_active else "Неактивен"
        return "Нет автора"
    author_status.short_description = 'Статус автора'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
