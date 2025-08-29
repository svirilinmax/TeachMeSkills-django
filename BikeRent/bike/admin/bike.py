from django.contrib import admin

from bike.models import Bike


# Регистрируем модель в админке
@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "brand",
        "colour",
        "display_station",
        "available",
        "electricity",
    )
    list_filter = (
        "name",
        "station",
        "brand",
        "available",
        "electricity",
    )

    list_editable = ("available", "electricity")
    search_fields = ("name", "brand", "station__name")
    search_help_text = "Search by: bike name, brand or station name"
    ordering = ("-name",)
    fieldsets = (
        (None, {"fields": ("category", "name", "brand", "station")}),
        ("Основная информация", {"fields": ("available", "electricity")}),
        ("Даты", {"fields": ("created_at", "updated_at", "deleted_at")}),
    )

    readonly_fields = ("created_at", "updated_at", "deleted_at", "electricity")

    def display_station(self, obj):
        return f"st. {obj.station.name}, {obj.station.address}"

    display_station.short_description = "Station"
