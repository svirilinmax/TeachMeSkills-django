from django.contrib import admin

from bike.models import Station, Bike


class BikeInline(admin.StackedInline):
    model = Bike
    extra = 1
    fields = ("name", "brand", "category",)
    readonly_fields = ("name", "brand", "category",)
    max_num = 1

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "capacity", "is_big_capacity")
    list_filter = ("name", "address")
    list_editable = ("capacity",)
    search_fields = ("name",)
    search_help_text = "Search by: station name"
    ordering = ("-name",)
    inlines = [BikeInline]

    def is_big_capacity(self, obj):
        return obj.is_big_capacity

    is_big_capacity.boolean = True
    is_big_capacity.short_description = "Is big capacity?"