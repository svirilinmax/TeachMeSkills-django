from django.contrib import admin

from cinema.admin.inline import (
    MovieActorInline,
    MovieDirectorInline,
    MovieGenreInline,
    ScheduleInline,
)
from cinema.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    list_filter = ("year", "genres")
    search_fields = ("name",)
    ordering = ("-year", "name")
    exclude = ("genres", "actors", "directors")

    inlines = [
        ScheduleInline,
        MovieActorInline,
        MovieDirectorInline,
        MovieGenreInline,
    ]
