from django.contrib import admin
from workout.models import ExerciseToPlan


class ExerciseToPlanInlineForPlan(admin.TabularInline):
    """
    Инлайн для редактирования упражнений внутри плана.
    Поле plan скрываем — оно берётся из родителя.
    """
    model = ExerciseToPlan
    fk_name = "plan"
    extra = 1
    autocomplete_fields = ("exercise",)
    fields = ("exercise", "amount")


class ExerciseToPlanInlineForExercise(admin.TabularInline):
    """
    Инлайн для просмотра/редактирования включения упражнения в планы.
    Поле exercise скрываем — оно берётся из родителя.
    """
    model = ExerciseToPlan
    fk_name = "exercise"
    extra = 0
    autocomplete_fields = ("plan",)
    fields = ("plan", "amount")
    readonly_fields = ()