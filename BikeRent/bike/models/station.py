from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=250, unique=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    capacity = models.PositiveSmallIntegerField (default=0)

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"

    def __str__(self):
        return f"Station {self.name} - ({self.address})"

    @property
    def is_big_capacity(self):
        return self.capacity > 20