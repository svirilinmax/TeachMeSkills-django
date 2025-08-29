import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bike.models import Bike, Station


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class BikeView(View):
    def get(self, request: HttpRequest):
        """List of all bikes with pagination via Paginator"""
        try:
            page_number = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 20))
        except ValueError:
            return JsonResponse(
                {"error": "page и per_page должны быть числами"}, status=400
            )

        # We get all the bikes
        qs = (
            Bike.objects.all()
            .values(
                "id",
                "name",
                "brand",
                "category",
                "electricity",
                "colour",
                "available",
                "station__name",
            )
            .order_by("id")
        )

        paginator = Paginator(qs, per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        data = {
            "count": paginator.count,  # total number of objects
            "num_pages": paginator.num_pages,  # total pages
            "page": page_obj.number,  # current page
            "per_page": per_page,  # page size
            "results": list(page_obj.object_list),
        }

        return JsonResponse(data, safe=False)

    def post(self, request: HttpRequest):
        """Making a new bike"""
        try:
            data = json.loads(request.body)
            # Validation of required fields
            if not data.get("brand"):
                return JsonResponse({"error": "Поле 'brand' обязательно"}, status=400)
            if not data.get("colour"):
                return JsonResponse({"error": "Поле 'colour' обязательно"}, status=400)
            if not data.get("station_id"):
                return JsonResponse(
                    {"error": "Поле 'station_id' обязательно"}, status=400
                )

            try:
                station_id = int(data["station_id"])
                station = Station.objects.get(id=station_id)
            except (ValueError, TypeError):
                return JsonResponse(
                    {"error": "station_id должен быть числом"}, status=400
                )
            except Station.DoesNotExist:
                return JsonResponse(
                    {"error": f"Станция с id {station_id} не найдена"}, status=404
                )

            # Create a bicycle
            bike = Bike.objects.create(
                name=data.get("name"),
                brand=data["brand"],
                category=data.get("category"),
                electricity=data.get("electricity", False),
                colour=data["colour"],
                available=data.get("available", True),
                station=station,
                comments=data.get("comments"),
            )

            return JsonResponse(
                {
                    "id": bike.id,
                    "message": f"Bike {bike.name or bike.get_brand_display()} created",
                },
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Невалидный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



def bike_to_dict(obj: Bike) -> dict:
    """Function to convert Bike object to dictionary"""
    return {
        "id": obj.id,
        "category": obj.category,
        "name": obj.name,
        "brand": obj.brand,
        "electricity": obj.electricity,
        "colour": obj.colour,
        "available": obj.available,
        "comments": obj.comments,
        "preview": obj.preview.url if obj.preview else None,
        "station": obj.station_id,
    }

@method_decorator(csrf_exempt, name="dispatch")
class BikeDetailView(View):

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        bike = get_object_or_404(Bike, pk=pk)
        return JsonResponse(bike_to_dict(bike), status=200)

    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        # Getting an object (bicycle by pk (primary key)) for modification
        bike = get_object_or_404(Bike, pk=pk)
        try:
            # Decodes the request body from bytes to a UTF-8 string
            data = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Set the fields that we can change
        updatable_fields = [
            "category",
            "name",
            "brand",
            "electricity",
            "colour",
            "available",
            "comments",
        ]

        # We update only those fields that came in the request
        for field in updatable_fields:
            if field in data:
                setattr(bike, field, data[field])

        # Processing station change
        if "station" in data:
            try:
                station_id = int(data["station"])
                # Finds a station by ID (or 404 if it doesn't exist)
                station = get_object_or_404(Station, pk=station_id)
                # Establishes a connection between the bike and the station
                setattr(bike, "station", station)
            except (ValueError, TypeError):
                return JsonResponse(
                    {"error": "станция должна быть целым числом"}, status=400
                )

        bike.save()
        return JsonResponse(bike_to_dict(bike), status=200)

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        bike = get_object_or_404(Bike, pk=pk)
        bike.delete()
        return JsonResponse({"status": "deleted"}, status=204, safe=False)
