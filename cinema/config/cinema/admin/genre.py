from django.contrib import admin

from cinema.admin.inline import MovieGenreInline
from cinema.models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    class AttachedMovieInline(MovieGenreInline):
        fk_name = "genre"

    inlines = [AttachedMovieInline]
