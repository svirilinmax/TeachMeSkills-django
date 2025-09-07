import os
import sys

import django
import pytest
from django.apps import apps
from django.test import Client

# Add the path to the project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_model_instance(db):
    """
    Возвращает функцию, которая создаёт экземпляр любой модели с тестовыми данными.
    Usage:
        genre = create_model_instance('cinema.Genre', name="Drama")
    """
    from django.db import models

    def _create(model_name: str, **kwargs):
        app_label, model_class_name = model_name.split(".")
        model_class = apps.get_model(app_label, model_class_name)

        # Create test values for required fields if not passed
        for field in model_class._meta.fields:
            if field.name not in kwargs and not field.blank and not field.auto_created:
                if isinstance(field, models.CharField) or isinstance(
                    field, models.TextField
                ):
                    kwargs[field.name] = f"Test {field.name}"
                elif isinstance(field, models.IntegerField):
                    kwargs[field.name] = 1
                elif isinstance(field, models.FloatField):
                    kwargs[field.name] = 1.0
                elif isinstance(field, models.BooleanField):
                    kwargs[field.name] = True
                elif isinstance(field, models.ForeignKey):
                    kwargs[field.name] = _create(
                        f"{field.related_model._meta.app_label}.{field.related_model.__name__}"
                    )

        instance = model_class.objects.create(**kwargs)
        return instance

    return _create


@pytest.fixture
def test_data(create_model_instance):
    genre = create_model_instance("cinema.Genre", name="drama")
    director = create_model_instance("cinema.Director", name="Test Director")
    actor = create_model_instance("cinema.Actor", name="Test Actor")

    movie = create_model_instance(
        "cinema.Movie",
        name="Test Movie",
        year=2024,
    )
    movie.genres.add(genre)
    movie.actors.add(actor)
    movie.directors.add(director)

    from datetime import datetime

    from django.utils import timezone

    schedule = create_model_instance(
        "cinema.Schedule",
        movie=movie,
        movie_start=timezone.make_aware(datetime(2024, 1, 1, 18, 0)),
        price=10.00,
    )

    return {
        "genre": genre,
        "director": director,
        "actor": actor,
        "movie": movie,
        "schedule": schedule,
    }
