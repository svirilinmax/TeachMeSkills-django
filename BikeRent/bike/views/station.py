import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bike.models import Station


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class StationView(View):
    def get(self, request: HttpRequest):
        """List of all stations"""
        try:
            page_number = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 20))
        except ValueError:
            return JsonResponse(
                {"error": "page и per_page должны быть числами"}, status=400
            )
        stations = Station.objects.all().values("id", "name", "address", "capacity")

        paginator = Paginator(stations, per_page)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Format the response with pagination
        response_data = {
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "per_page": per_page,
            },
            "stations": list(page_obj.object_list),
        }
        return JsonResponse(response_data)

    def post(self, request: HttpRequest):
        """Creating a new station"""
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
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Невалидный JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)