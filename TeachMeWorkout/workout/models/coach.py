from django.contrib.auth import get_user_model
from django.db import models
from common.models import TimeStampedMixin


User = get_user_model()


class Coach(TimeStampedMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="coach")

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f"Тренер: {self.user.get_full_name() or self.user.username}"