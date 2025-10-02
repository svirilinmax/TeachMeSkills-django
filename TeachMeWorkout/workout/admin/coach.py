from django.contrib import admin
from django.contrib.auth import get_user_model
from workout.models import Coach

User = get_user_model()


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")
    autocomplete_fields = ("user",)
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("user__username",)
