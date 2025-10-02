from django.contrib import admin

from workout.models import ExerciseToPlan


@admin.register(ExerciseToPlan)
class ExerciseToPlanAdmin(admin.ModelAdmin):
    """
    Админка для быстрого массового редактирования связей.
    """

    list_display = ("id", "plan", "exercise", "amount")
    list_select_related = ("plan", "exercise")
    autocomplete_fields = ("plan", "exercise")
    search_fields = ("plan__author__username", "exercise__title")
    list_filter = ("plan",)
    ordering = ("plan", "exercise__title")
