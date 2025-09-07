# cinema/tests/test_schedule_list.py
from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cinema.models import Actor, Director, Genre, Movie, Schedule


class ScheduleListViewTest(TestCase):

    def setUp(self):
        """Создание тестовых данных перед каждым тестом"""
        # create Genres
        self.genre_drama = Genre.objects.create(name="drama")
        self.genre_comedy = Genre.objects.create(name="comedy")

        # create Movies
        self.movie_1 = Movie.objects.create(name="Paul Maul", year=1995)
        self.movie_2 = Movie.objects.create(name="Ezy Movie", year=2000)

        # add genres to movies (ManyToMany)
        self.movie_1.genres.add(self.genre_drama)
        self.movie_2.genres.add(self.genre_comedy)

        self.session_1 = Schedule.objects.create(
            movie=self.movie_1,
            movie_start=timezone.make_aware(datetime.today() + timedelta(days=1)),
            price=5.00,
        )
        self.session_2 = Schedule.objects.create(
            movie=self.movie_2,
            movie_start=timezone.make_aware(datetime.today() + timedelta(days=2)),
            price=15.00,
        )

    def test_schedule_filters_by_name(self):
        """Тест фильтрации по названию фильма"""
        url = "/cinema/schedule/"
        response = self.client.get(url, {"q": "Paul"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paul Maul")
        self.assertNotContains(response, "Ezy Movie")

    def test_schedule_filters_by_genre(self):
        """Тест фильтрации по жанру"""
        url = "/cinema/schedule/"
        response = self.client.get(url, {"genre": "comedy"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ezy Movie")
        self.assertNotContains(response, "Paul Maul")

    def test_schedule_filters_by_date(self):
        """Тест фильтрации по дате"""
        url = "/cinema/schedule/"
        today = datetime.now().date()
        tomorrow = (datetime.now() + timedelta(days=1)).date()

        response = self.client.get(
            url,
            {
                "date_from": today.strftime("%Y-%m-%d"),
                "date_to": tomorrow.strftime("%Y-%m-%d"),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paul Maul")
        self.assertNotContains(response, "Ezy Movie")

    def test_schedule_filters_by_price(self):
        """Тест фильтрации по цене"""
        url = "/cinema/schedule/"
        response = self.client.get(url, {"price_min": 10, "price_max": 15})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ezy Movie")
        self.assertNotContains(response, "Paul Maul")

    def test_schedule_pagination(self):
        """Тест пагинации"""
        genre_horror = Genre.objects.create(name="horror")
        movie = Movie.objects.create(name="Test Movie pagination", year=2000)
        movie.genres.add(genre_horror)

        for i in range(15):
            Schedule.objects.create(
                movie=movie,
                movie_start=timezone.make_aware(datetime.today() + timedelta(days=i)),
                price=1.00 + i,
            )

        url = "/cinema/schedule/"
        response = self.client.get(url, {"page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")
