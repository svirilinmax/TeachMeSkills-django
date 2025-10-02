from django.contrib import admin
from django.db.models import Sum
from django.contrib.auth import get_user_model
from .inlines import ExerciseToPlanInlineForPlan
from workout.models import TrainingPlan

User = get_user_model()

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "exercises_total")
    list_display_links = ("id", "author")
    autocomplete_fields = ("author",)
    search_fields = (
        "author__username",
        "author__email",
        "author__first_name",
        "author__last_name",
    )
    inlines = (ExerciseToPlanInlineForPlan,)
    ordering = ("-id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_ex_total=Sum("exercise__amount"))

    @admin.display(description="Всего повторений", ordering="_ex_total")
    def exercises_total(self, obj):
        return getattr(obj, "_ex_total", 0) or 0

