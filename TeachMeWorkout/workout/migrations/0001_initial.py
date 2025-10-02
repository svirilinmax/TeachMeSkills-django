import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models

import common.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Coach",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coach",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Тренер",
                "verbose_name_plural": "Тренеры",
            },
            bases=(common.models.TimeStampedMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Название упражнения",
                        max_length=255,
                        verbose_name="Название упражнения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение",
                "verbose_name_plural": "Упражнения",
                "ordering": [django.db.models.functions.text.Lower("title")],
                "constraints": [
                    models.UniqueConstraint(
                        django.db.models.functions.text.Lower("title"),
                        name="unique_exercise_title_ci",
                    )
                ],
            },
            bases=(common.models.TimeStampedMixin, models.Model),
        ),
        migrations.CreateModel(
            name="TrainingPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название плана"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "План тренировки",
                "verbose_name_plural": "Планы тренировок",
                "ordering": ["-id"],
            },
            bases=(common.models.TimeStampedMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Training",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("workday", models.DateField(verbose_name="День тренировки")),
                (
                    "duration",
                    models.PositiveIntegerField(
                        default=60, verbose_name="Длительность (мин)"
                    ),
                ),
                (
                    "completed",
                    models.BooleanField(default=False, verbose_name="Завершена"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Заметки")),
                (
                    "plan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trainings",
                        to="workout.trainingplan",
                        verbose_name="План тренировки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тренировка",
                "verbose_name_plural": "Тренировки",
                "ordering": ["-workday"],
            },
            bases=(common.models.TimeStampedMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ExerciseToPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.PositiveSmallIntegerField()),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plan",
                        to="workout.exercise",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercise",
                        to="workout.trainingplan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Упражнение в плане",
                "verbose_name_plural": "Упражнения в плане",
                "unique_together": {("exercise", "plan")},
            },
            bases=(common.models.TimeStampedMixin, models.Model),
        ),
    ]
