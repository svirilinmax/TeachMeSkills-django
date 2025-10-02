from django.contrib.auth import get_user_model
from django.db import models
from common.models import TimeStampedMixin

User = get_user_model()


class Training(TimeStampedMixin, models.Model):
    workday = models.DateField(
        verbose_name='День тренировки'
    )
    plan = models.ForeignKey(
        "TrainingPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trainings",
        verbose_name='План тренировки'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Длительность (мин)',
        default=60
    )
    completed = models.BooleanField(
        verbose_name='Завершена',
        default=False
    )
    notes = models.TextField(
        verbose_name='Заметки',
        blank=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-workday']

    def __str__(self):
        return f"Тренировка {self.workday}"