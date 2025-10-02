from django.contrib import admin

from cinema.models import Actor, Director, Genre, Movie, Schedule


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ("movie_start", "price")
    ordering = ("movie_start",)
    verbose_name = "Сеанс"
    verbose_name_plural = "Сеансы"


class MovieActorInline(admin.TabularInline):
    """
    Инлайн для связи Movie <-> Actor через скрытую through-модель.
    Используется в MovieAdmin и ActorAdmin.
    """

    model = Movie.actors.through
    extra = 1
    autocomplete_fields = ("actor",)
    verbose_name = "Актёр"
    verbose_name_plural = "Актёры"


class MovieDirectorInline(admin.TabularInline):
    model = Movie.directors.through
    extra = 1
    autocomplete_fields = ("director",)
    verbose_name = "Режиссёр"
    verbose_name_plural = "Режиссёры"


class MovieGenreInline(admin.TabularInline):
    model = Movie.genres.through
    extra = 1
    autocomplete_fields = ("genre",)
    verbose_name = "Жанр"
    verbose_name_plural = "Жанры"
