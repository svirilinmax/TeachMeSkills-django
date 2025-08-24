from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bikes/', include('bike.urls')),  # Подключение URLs из приложения bike
    path('rents/', include('rent.urls')),
]
