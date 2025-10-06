from django.contrib import admin
from django.contrib.auth import get_user_model

from workout.models import Training

User = get_user_model()


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("id", "workday")
    list_display_links = ("id", "workday")
    date_hierarchy = "workday"
    ordering = ("-workday",)
    search_fields = ("workday",)
    list_filter = ("workday",)
