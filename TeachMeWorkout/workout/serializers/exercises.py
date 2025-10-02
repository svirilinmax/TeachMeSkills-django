from django.contrib.auth import get_user_model
from rest_framework import serializers

from workout.models import Exercise, ExerciseToPlan

User = get_user_model()


class PlansToExerciseSerializer(serializers.ModelSerializer):
    plan_title = serializers.CharField(source="plan.title", read_only=True)
    author = serializers.CharField(source="plan.author.username", read_only=True)

    class Meta:
        model = ExerciseToPlan
        fields = ["id", "plan_title", "author", "amount"]


class ExerciseSerializer(serializers.ModelSerializer):
    plan = PlansToExerciseSerializer(many=True, read_only=True)

    def validate_title(self, value: str) -> str:
        result = Exercise.objects.filter(title__iexact=value).exists()
        if result:
            raise serializers.ValidationError(
                "Exercise with this title already exists (case-insensitive)."
            )
        return value

    class Meta:
        model = Exercise
        fields = ["id", "title", "plan"]


class ExerciseOnlyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["title"]


class ExercisePlanNestedSerializer(serializers.ModelSerializer):
    exercise = serializers.SerializerMethodField()

    def get_exercise(self, exercise: ExerciseToPlan) -> str:
        return exercise.exercise.title

    class Meta:
        model = ExerciseToPlan
        fields = ["id", "exercise", "amount"]
