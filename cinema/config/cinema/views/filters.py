import django_filters
from django_filters import CharFilter, DateFilter, NumberFilter

from cinema.models import Schedule


class ScheduleFilter(django_filters.FilterSet):
    movie_name = CharFilter(
        field_name="movie__name", lookup_expr="icontains", label="Название фильма"
    )

    min_price = NumberFilter(
        field_name="price", lookup_expr="gte", label="Минимальная цена"
    )

    max_price = NumberFilter(
        field_name="price", lookup_expr="lte", label="Максимальная цена"
    )

    start_date = DateFilter(
        field_name="movie_start", lookup_expr="date__gte", label="Начальная дата"
    )

    end_date = DateFilter(
        field_name="movie_start", lookup_expr="date__lte", label="Конечная дата"
    )

    exact_date = DateFilter(
        field_name="movie_start", lookup_expr="date", label="Точная дата"
    )

    genre = CharFilter(
        field_name="movie__genres__name", lookup_expr="exact", label="Жанр"
    )

    actor = CharFilter(
        field_name="movie__actors__name", lookup_expr="icontains", label="Актер"
    )

    director = CharFilter(
        field_name="movie__directors__name", lookup_expr="icontains", label="Режиссер"
    )

    year = NumberFilter(
        field_name="movie__year", lookup_expr="exact", label="Год фильма"
    )

    class Meta:
        model = Schedule
        fields = [
            "movie_name",
            "min_price",
            "max_price",
            "start_date",
            "end_date",
            "exact_date",
            "genre",
            "actor",
            "director",
            "year",
        ]
