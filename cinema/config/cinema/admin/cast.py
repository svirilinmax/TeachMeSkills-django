from django.contrib import admin

from cinema.admin.inline import MovieActorInline, MovieDirectorInline
from cinema.models import Actor, Director


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "dob")
    search_fields = ("name",)
    date_hierarchy = "dob"
    ordering = ("name",)

    class AttachedMovieInline(MovieActorInline):
        fk_name = "actor"

    inlines = [AttachedMovieInline]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "dob")
    search_fields = ("name",)
    date_hierarchy = "dob"
    ordering = ("name",)

    class AttachedMovieInline(MovieDirectorInline):
        fk_name = "director"

    inlines = [AttachedMovieInline]
