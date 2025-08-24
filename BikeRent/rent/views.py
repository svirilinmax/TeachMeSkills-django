from django.urls import path

from BikeRent.bike.views import BikeDetailView

urlpattern = [
    path('bike/', BikeDetailView.as_view(), name = "bike-detail")
]
