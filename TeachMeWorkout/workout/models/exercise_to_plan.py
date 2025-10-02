from django.db import models
from common.models import TimeStampedMixin
from .exercise import Exercise
from .trainingplan import TrainingPlan


class ExerciseToPlan(TimeStampedMixin, models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="plan")
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="exercise")
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Упражнение в плане'
        verbose_name_plural = 'Упражнения в плане'
        unique_together = ("exercise", "plan")

    def __str__(self):
        return f"{self.exercise.title} - {self.amount} reps"