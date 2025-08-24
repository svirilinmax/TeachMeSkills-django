import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .models import Bike, Station

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class BikeView(View):
    def get(self, request: HttpRequest):
        """Список всех велосипедов с пагинацией через Paginator"""
        try:
            page_number = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 20))
        except ValueError:
            return JsonResponse(
                {"error": "page и per_page должны быть числами"}, status=400
            )

        # Получаем все велосипеды с связанной станцией
        qs = Bike.objects.all().select_related('station').order_by("id")

        paginator = Paginator(qs, per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        bikes_list = []
        for bike in page_obj.object_list:
            bikes_list.append({
                "id": bike.id,
                "name": bike.name,
                "brand": bike.get_brand_display(),  # Используем метод для отображения
                "category": bike.get_category_display(),  # Используем метод для отображения
                "electricity": bike.electricity,
                "colour": bike.colour,  # Используем метод для отображения
                "available": bike.available,
                "station_name": bike.station.name if bike.station else None,
            })

        # Формируем структурированный ответ
        response_data = {
            "pagination": {
                "current_page": page_obj.number,            # Текущий номер страницы (начинается с 1)
                "total_pages": paginator.num_pages,         # Общее количество страниц
                "total_items": paginator.count,             # Общее количество всех станций в базе
                "per_page": per_page,                       # Количество станций на одной странице
                "has_next": page_obj.has_next(),            # Есть ли следующая страница (true/false)
                "has_previous": page_obj.has_previous(),    # Есть ли предыдущая страница (true/false)
                "next_page_number":
                    page_obj.next_page_number()
                    if page_obj.has_next() else None,       # Номер следующей страницы или None
                "previous_page_number":
                    page_obj.previous_page_number()
                    if page_obj.has_previous() else None,   # Номер предыдущей страницы или None
            },
                "bikes": bikes_list      # Список станций на текущей странице
        }

        return JsonResponse(response_data)

    def post(self, request: HttpRequest):
        """Создание нового велосипеда"""
        try:
            data = json.loads(request.body)
            # Валидация обязательных полей
            if not data.get("brand"):
                return JsonResponse({"error": "Поле 'brand' обязательно"}, status=400)
            if not data.get("colour"):
                return JsonResponse({"error": "Поле 'colour' обязательно"}, status=400)
            if not data.get("station_id"):
                return JsonResponse({"error": "Поле 'station_id' обязательно"}, status=400)

            # Проверка категории
            category = data.get("category")
            if category == "other" and not data.get("custom_category"):
                return JsonResponse(
                    {"error": "При выборе 'Другое' необходимо указать custom_category"},
                    status=400
                )

            # Проверка бренда
            brand = data.get("brand")
            if brand == "other" and not data.get("custom_brand"):
                return JsonResponse(
                    {"error": "При выборе 'Другая' необходимо указать custom_brand"},
                    status=400
                )

            # Проверка цвета
            colour = data.get("colour")
            if colour == "other" and not data.get("custom_colour"):
                return JsonResponse(
                    {"error": "При выборе 'Другой' необходимо указать custom_colour"},
                    status=400
                )

            try:
                station_id = int(data["station_id"])
                station = Station.objects.get(id=station_id)
            except (ValueError, TypeError):
                return JsonResponse({"error": "station_id должен быть числом"}, status=400)
            except Station.DoesNotExist:
                return JsonResponse({"error": f"Станция с id {station_id} не найдена"}, status=404)

            # Создаем велосипед
            bike = Bike.objects.create(
                name=data.get("name"),
                brand=data["brand"],
                custom_brand=data.get("custom_brand"),  # Добавлено
                category=data.get("category"),
                custom_category=data.get("custom_category"),  # Добавлено
                electricity=data.get("electricity", False),
                colour=data["colour"],
                custom_colour=data.get("custom_colour"),  # Добавлено
                available=data.get("available", True),
                station=station,
                comments=data.get("comments"),
            )

            return JsonResponse(
                {"id": bike.id,
                "message": f"Bike {bike.name or bike.get_brand_display()} created"},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Невалидный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class StationView(View):
    def get(self, request: HttpRequest):
        """Список всех станций"""
        try:
            page_number = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 20))
        except ValueError:
            return JsonResponse(
                {"error": "page и per_page должны быть числами"}, status=400
            )
        stations = (Station.objects.all().
                values(
                    "id",
                    "name",
                    "address",
                    "capacity"))

        paginator = Paginator(stations, per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Форматируем ответ с пагинацией
        response_data = {
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "per_page": per_page,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
                "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
            },
            "stations": list(page_obj.object_list)
        }
        return JsonResponse(response_data)

    def post(self, request: HttpRequest):
        """Создание новой станции"""
        try:
            data = json.loads(request.body)
            if not data.get("name"):
                return JsonResponse({"error": "Поле 'name' обязательно"}, status=400)
            if not data.get("address"):
                return JsonResponse({"error": "Поле 'address' обязательно"}, status=400)

            station = Station.objects.create(
                name=data["name"],
                address=data["address"],
                capacity=data.get("capacity", 0),
            )

            return JsonResponse(
                {"id": station.id, "message": f"Station {station.name} created"},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Невалидный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def bike_to_dict(obj: Bike) -> dict:
    """Функция для преобразования объекта Bike в словарь"""
    return {
        "id": obj.id,
        "category": obj.category,
        "custom_category": obj.custom_category,
        "name": obj.name,
        "brand": obj.brand,
        "custom_brand": obj.custom_brand,
        "electricity": obj.electricity,
        "colour": obj.colour,
        "custom_colour": obj.custom_colour,
        "available": obj.available,
        "comments": obj.comments,
        "preview": obj.preview.url if obj.preview else None,
        "station": obj.station_id,
        "display_category": obj.get_category_display(),  # Добавлено для удобства
        "display_brand": obj.get_brand_display(),        # Добавлено для удобства
        "display_colour": obj.get_colour_display(),      # Добавлено для удобства
    }


@method_decorator(csrf_exempt, name='dispatch')
class BikeDetailView(View):

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        bike = get_object_or_404(Bike, pk=pk)
        return JsonResponse(bike_to_dict(bike), status=200)


    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        #  Получение объекта (велосипед по pk (primary key)) для изменения
        bike = get_object_or_404(Bike, pk=pk)
        try:
            # Декодирует тело запроса из bytes в строку UTF-8
            data = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Проверки для полей с выбором "Другое"
        if "category" in data and data["category"] == "other" and not data.get("custom_category"):
            return JsonResponse(
                {"error": "При выборе 'Другое' необходимо указать custom_category"},
                status=400
            )

        if "brand" in data and data["brand"] == "other" and not data.get("custom_brand"):
            return JsonResponse(
                {"error": "При выборе 'Другая' необходимо указать custom_brand"},
                status=400
            )

        if "colour" in data and data["colour"] == "other" and not data.get("custom_colour"):
            return JsonResponse(
                {"error": "При выборе 'Другой' необходимо указать custom_colour"},
                status=400
            )

        # Устанавливаем поля, которые сможем изменить
        updatable_fields = [
            "category", "custom_category",
            "name",
            "brand", "custom_brand",
            "electricity",
            "colour", "custom_colour",
            "comments",
        ]

        #  Обновляем только те поля, которые пришли в запросе
        for field in updatable_fields:
            if field in data:
                setattr(bike, field, data[field])

        # Обрабатываем изменение станции
        if "station" in data:
            try:
                station_id = int(data["station"])
                # Находит станцию по ID (или 404 если не существует)
                station = get_object_or_404(Station, pk=station_id)
                # Устанавливает связь велосипеда со станцией
                setattr(bike, 'station', station)
            except (ValueError, TypeError):
                return JsonResponse({"error": "станция должна быть целым числом"}, status=400)

        bike.save()
        return JsonResponse(bike_to_dict(bike), status=200)


    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        bike = get_object_or_404(Bike, pk=pk)
        bike.delete()
        return JsonResponse({"status": "deleted"}, status=204, safe=False)