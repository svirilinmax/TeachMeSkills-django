from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimeStampedMixin

User = get_user_model()


class TrainingPlan(TimeStampedMixin, models.Model):
    title = models.CharField(max_length=255, verbose_name="Название плана")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")

    class Meta:
        verbose_name = "План тренировки"
        verbose_name_plural = "Планы тренировок"
        ordering = ["-id"]

    def __str__(self):
        return f"Plan by {self.author.username} (#{self.id})"
