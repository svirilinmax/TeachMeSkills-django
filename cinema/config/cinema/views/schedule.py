from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from cinema.models import Actor, Director, Genre, Movie, Schedule
from cinema.serializers import ScheduleSerializer

from .filters import ScheduleFilter
from .forms import ScheduleFilterForm


class ScheduleListView(ListView):
    model = Schedule
    template_name = "cinema/schedule_list.html"
    context_object_name = "sessions"
    paginate_by = 10

    def get_queryset(self):
        # Filters
        self.form = ScheduleFilterForm(self.request.GET)

        if not self.form.is_valid():
            # If the form is not valid, return all records
            return (
                Schedule.objects.select_related("movie")
                .only(
                    "id",
                    "movie_start",
                    "price",
                    "movie_id",
                    "movie__id",
                    "movie__name",
                    "movie__year",
                )
                .order_by("movie_start")
            )

        qs = (
            Schedule.objects.select_related("movie")
            .only(
                "id",
                "movie_start",
                "price",
                "movie_id",
                "movie__id",
                "movie__name",
                "movie__year",
            )
            .order_by("movie_start")
        )

        cleaned_data = self.form.cleaned_data

        # Apply filters
        if cleaned_data.get("q"):
            qs = qs.filter(movie__name__icontains=cleaned_data["q"])

        if cleaned_data.get("genre"):
            qs = qs.filter(movie__genres__name=cleaned_data["genre"])

        # Filter by date
        date_range = self.form.get_date_range()
        qs = qs.filter(**date_range)

        # Filter by price
        if cleaned_data.get("price_min"):
            qs = qs.filter(price__gte=cleaned_data["price_min"])

        if cleaned_data.get("price_max"):
            qs = qs.filter(price__lte=cleaned_data["price_max"])

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["genres"] = Genre.objects.all().order_by("name")

        # Добавляем форму в контекст
        if not hasattr(self, "form"):
            self.form = ScheduleFilterForm(self.request.GET)
        ctx["form"] = self.form

        # Также оставляем старые значения для обратной совместимости
        r = self.request.GET
        ctx.update(
            {
                "q": r.get("q", ""),
                "active_genre": r.get("genre", ""),
                "date_from": r.get("date_from", ""),
                "date_to": r.get("date_to", ""),
                "price_min": r.get("price_min", ""),
                "price_max": r.get("price_max", ""),
            }
        )

        ctx["is_filtered"] = self.form.is_filtered()

        return ctx


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Schedule.objects.all()
        .select_related("movie")
        .prefetch_related("movie__genres", "movie__actors", "movie__directors")
    )
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ScheduleFilter
    ordering_fields = ["movie_start", "price", "movie__name", "movie__year"]
    ordering = ["movie_start"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
