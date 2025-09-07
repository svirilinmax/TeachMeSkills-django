from django.contrib import admin

from cinema.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("movie", "movie_start", "price")
    list_filter = ("movie",)
    date_hierarchy = "movie_start"
    search_fields = ("movie__name",)
    ordering = ("-movie_start",)
    autocomplete_fields = ("movie",)
