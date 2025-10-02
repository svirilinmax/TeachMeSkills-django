from rest_framework import serializers

from cinema.models import Actor, Director, Genre, Movie, Schedule


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "get_name_display"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "dob", "rewards"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "name", "dob"]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    directors = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "name", "year", "genres", "actors", "directors"]


class ScheduleSerializer(serializers.ModelSerializer):
    movie_detail = MovieSerializer(source="movie", read_only=True)
    movie_name = serializers.CharField(source="movie.name", read_only=True)
    movie_genres = serializers.SerializerMethodField()
    movie_year = serializers.IntegerField(source="movie.year", read_only=True)

    class Meta:
        model = Schedule
        fields = [
            "id",
            "movie_start",
            "movie",
            "movie_detail",
            "movie_name",
            "movie_year",
            "movie_genres",
            "price",
        ]

    def get_movie_genres(self, obj):
        return [genre.get_name_display() for genre in obj.movie.genres.all()]
