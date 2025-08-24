from django.contrib import admin
# Импортируем вашу модель
from .models import Bike, Station


# Регистрируем модель в админке
@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ("category", "name", 'brand')
    # list_display_links = ()
    list_filter = ('available', 'electricity')
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Stations)
# admin.site.register(Bike)
# Register your models here.
