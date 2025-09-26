from django.contrib import admin
from django.contrib.auth import get_user_model

from ..models import Author

User = get_user_model()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Отображение в списке
    list_display = ("name", "user", "is_active", "book_count")
    list_editable = ("is_active",)
    list_filter = ("is_active", "user__is_active")
    search_fields = ("name", "user__username", "user__email")
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("user", "name", "is_active")}),
        ("Статистика", {"fields": ("book_count",), "classes": ("collapse",)}),
    )

    readonly_fields = ("book_count",)

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = "Количество книг"

    actions = ["activate_authors", "deactivate_authors"]

    def activate_authors(self, request, queryset):
        queryset.update(is_active=True)

    activate_authors.short_description = "Активировать выбранных авторов"

    def deactivate_authors(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_authors.short_description = "Деактивировать выбранных авторов"
