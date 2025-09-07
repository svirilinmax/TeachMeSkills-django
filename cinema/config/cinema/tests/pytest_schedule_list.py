from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from ..models import Actor, Director, Genre, Movie, Schedule


@pytest.mark.django_db
def test_schedule_filters(client):
    # Create a Genre
    genre_drama = Genre.objects.create(name="Drama")
    genre_comedy = Genre.objects.create(name="Comedy")

    # Create a Movie
    movie_1 = Movie.objects.create(name="Paul Maul", year=1995)
    movie_2 = Movie.objects.create(name="Ezy Movie", year=2000)

    # Add genres to movies (ManyToMany)
    movie_1.genres.add(genre_drama)
    movie_2.genres.add(genre_comedy)

    session_1 = Schedule.objects.create(
        movie=movie_1,
        movie_start=timezone.make_aware(datetime.today() + timedelta(days=1)),
        price=5.00,
    )
    session_2 = Schedule.objects.create(
        movie=movie_2,
        movie_start=timezone.make_aware(datetime.today() + timedelta(days=2)),
        price=15.00,
    )

    url = reverse("schedule-list")

    # 1. filter by q (search by name)
    response = client.get(url, {"q": "Paul"})
    assert response.status_code == 200
    content = response.content.decode()
    assert "Paul Maul" in content  # True
    assert "Ezy Movie" not in content  # False

    # 2. filter by genre (search by name)
    response = client.get(url, {"genre": "Comedy"})
    assert response.status_code == 200
    content = response.content.decode()
    assert "Ezy Movie" not in content
    assert "Paul Maul" in content

    # 3. filter by date
    today = datetime.now().date()
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    response = client.get(
        url,
        {
            "date_from": today.strftime("%Y-%m-%d"),
            "date_to": tomorrow.strftime("%Y-%m-%d"),
        },
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Paul Maul" in content
    assert "Ezy Movie" not in content

    # 4. filter by price
    response = client.get(url, {"price_min": 10, "price_max": 15})
    assert response.status_code == 200
    content = response.content.decode()
    assert "Ezy Movie" not in content
    assert "Paul Maul" in content


@pytest.mark.django_db
def test_schedule_pagination(client):
    genre_horror = Genre.objects.create(name="Horror")
    movie = Movie.objects.create(name="Test Movie pagination", year=2000)
    movie.genres.add(genre_horror)

    for i in range(15):
        Schedule.objects.create(
            movie=movie,
            movie_start=timezone.make_aware(datetime.today() + timedelta(days=i)),
            price=1.00 + i,
        )

    url = reverse("schedule-list")

    response = client.get(url, {"page": 1})
    assert response.status_code == 200

    content = response.content.decode()
    assert "Test Movie" in content
