from django.db.models import Prefetch, Q
from django.views.generic import ListView

from cinema.models import Actor, Director, Genre, Movie, Schedule


class MovieListView(ListView):
    model = Movie
    template_name = "cinema/movie_list.html"
    context_object_name = "movies"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Movie.objects.only("id", "name", "year")
            .prefetch_related(
                "genres",
                Prefetch("actors", queryset=Actor.objects.only("id", "name")),
                Prefetch("directors", queryset=Director.objects.only("id", "name")),
            )
            .order_by("-year", "name")
        )

        q = self.request.GET.get("q")
        genre = self.request.GET.get("genre")
        year = self.request.GET.get("year")

        if q:
            qs = qs.filter(Q(name__icontains=q))
        if genre:
            qs = qs.filter(genres__name=genre)
        if year:
            qs = qs.filter(year=year)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        from django.core.cache import cache

        genres = cache.get("all_genres")
        if genres is None:
            genres = Genre.objects.only("id", "name").order_by("name")
            cache.set("all_genres", genres, 120)

        ctx["genres"] = Genre.objects.all().order_by("name")
        ctx["active_genre"] = self.request.GET.get("genre", "")
        ctx["active_year"] = self.request.GET.get("year", "")
        ctx["q"] = self.request.GET.get("q", "")
        ctx["is_filtered"] = any([ctx["q"], ctx["active_genre"], ctx["active_year"]])
        return ctx
