from datetime import date, datetime, timedelta

from cinema.models import Actor, Director, Genre, Movie, Schedule
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


class ScheduleViewSetTest(TestCase):

    def setUp(self):
        """Создание тестовых данных для API"""

        self.client = APIClient()
        now = timezone.now()

        # User Creation with Authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        # create Genres, Actors, Directors
        self.genre_drama = Genre.objects.create(name="drama")
        self.genre_comedy = Genre.objects.create(name="comedy")

        self.actor = Actor.objects.create(
            name="John Doe",
            dob=date(1980, 1, 1),
        )

        self.director = Director.objects.create(
            name="Christopher Nolan",
            dob=date(1970, 7, 30),
        )

        # create Movies
        self.movie_1 = Movie.objects.create(name="Paul Maul", year=1995)
        self.movie_2 = Movie.objects.create(name="Ezy Movie", year=2000)

        # add relations
        self.movie_1.genres.add(self.genre_drama)
        self.movie_1.actors.add(self.actor)
        self.movie_1.directors.add(self.director)
        self.movie_2.genres.add(self.genre_comedy)

        self.api_url = reverse("schedule-list")

        # Create schedules
        self.session_1 = Schedule.objects.create(
            movie=self.movie_1,
            movie_start=now + timedelta(days=1),
            price=5.00,
        )
        self.session_2 = Schedule.objects.create(
            movie=self.movie_2,
            movie_start=now + timedelta(days=2),
            price=15.00,
        )

    def test_list_returns_schedules_ordered_by_default(self):
        """Тест возвращает расписания, упорядоченные по умолчанию"""
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        ids = [item["id"] for item in data]
        expected_ids = [self.session_1.id, self.session_2.id]
        self.assertEqual(ids, expected_ids)

    def test_api_returns_all_sessions(self):
        """Тест API без фильтров"""
        print("All schedules in DB:", Schedule.objects.all().count())
        for s in Schedule.objects.all():
            print(f"ID: {s.id}, Movie: {s.movie.name}, Start: {s.movie_start}")

        response = self.client.get(self.api_url)
        print("Response data:", response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), Schedule.objects.all().count())

    def test_api_filters_by_movie_name(self):
        """Тест фильтрации по названию фильма (icontains)"""
        response = self.client.get(self.api_url, {"movie_name": "Paul"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")

    def test_api_filters_by_genre_exact(self):
        """Тест фильтрации по точному названию жанра"""
        response = self.client.get(self.api_url, {"genre": "drama"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")

    def test_api_filters_by_actor_icontains(self):
        """Тест фильтрации по части имени актера"""
        response = self.client.get(self.api_url, {"actor": "John"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")

    def test_api_filters_by_director_icontains(self):
        """Тест фильтрации по части имени режиссера"""
        response = self.client.get(self.api_url, {"director": "Nolan"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")

    def test_api_filters_by_year_exact(self):
        """Тест фильтрации по точному году"""
        response = self.client.get(self.api_url, {"year": 1995})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["year"], 1995)

    def test_api_filters_by_price_range(self):
        """Тест фильтрации по диапазону цен"""
        response = self.client.get(self.api_url, {"min_price": 10, "max_price": 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Ezy Movie")
        self.assertEqual(float(data[0]["price"]), 15.00)

    def test_api_filters_by_start_date(self):
        """Тест фильтрации по начальной дате"""
        today = datetime.now().date()
        response = self.client.get(
            self.api_url, {"start_date": today.strftime("%Y-%m-%d")}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 2)  # Оба сеанса после сегодня

    def test_api_filters_by_exact_date(self):
        """Тест фильтрации по точной дате"""
        exact_date = (datetime.now() + timedelta(days=1)).date()
        response = self.client.get(
            self.api_url, {"exact_date": exact_date.strftime("%Y-%m-%d")}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")

    def test_api_ordering_by_movie_start_desc(self):
        """Тест сортировки по дате сеанса (по убыванию)"""
        response = self.client.get(self.api_url, {"ordering": "-movie_start"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        # Первым должен быть session_2 (более поздняя дата)
        self.assertEqual(data[0]["movie_detail"]["name"], "Ezy Movie")

    def test_api_ordering_by_price_asc(self):
        """Тест сортировки по цене (по возрастанию)"""
        response = self.client.get(self.api_url, {"ordering": "price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        # Первым должен быть session_1 (меньшая цена)
        self.assertEqual(data[0]["movie_detail"]["name"], "Paul Maul")
        self.assertEqual(float(data[0]["price"]), 5.00)

    def test_api_empty_filter_results(self):
        """Тест пустых результатов фильтрации"""
        response = self.client.get(self.api_url, {"movie_name": "NonExistentMovie"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["results"]
        self.assertEqual(len(data), 0)

    def test_create_schedule_not_allowed(self):
        """Тест создания сеанса невозможен"""
        schedule_data = {
            "movie": self.movie_1.id,
            "movie_start": (timezone.now() + timedelta(days=3)).isoformat(),
            "price": 10.00,
        }
        initial_count = Schedule.objects.count()
        self.assertFalse(
            Schedule.objects.filter(movie_start=schedule_data["movie_start"]).exists()
        )
        response = self.client.post(self.api_url, data=schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Schedule.objects.count(), initial_count)

    def test_delete_schedule_not_allowed(self):
        """Тест: удаление сеанса не разрешено (только чтение)"""
        schedule_id = self.session_1.id
        url = reverse("schedule-detail", kwargs={"pk": schedule_id})
        initial_count = Schedule.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Schedule.objects.filter(pk=schedule_id).exists())
        self.assertEqual(Schedule.objects.count(), initial_count)
