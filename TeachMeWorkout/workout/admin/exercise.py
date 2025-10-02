from django.contrib import admin
from django.db.models import Count

from workout.models import Exercise

from .inlines import ExerciseToPlanInlineForExercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "plans_count")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    ordering = ("title",)
    inlines = (ExerciseToPlanInlineForExercise,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_plans_count=Count("plan"))

    @admin.display(description="В планах", ordering="_plans_count")
    def plans_count(self, obj):
        return getattr(obj, "_plans_count", 0)
