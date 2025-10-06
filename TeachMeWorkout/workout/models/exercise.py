from common.models import TimeStampedMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

User = get_user_model()


class Exercise(TimeStampedMixin, models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название упражнения",
        help_text="Название упражнения",
    )

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"
        ordering = [Lower("title")]
        constraints = [
            UniqueConstraint(
                Lower("title"),
                name="unique_exercise_title_ci",
            )
        ]

    def __str__(self):

        return self.title
