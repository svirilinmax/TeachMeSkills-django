from rest_framework import serializers

from workout.models import TrainingPlan

from .exercises import ExercisePlanNestedSerializer
from .trainings import TrainingSerializer
from .users import UserNestedSerializer


class TrainingPlanSerializer(serializers.ModelSerializer):
    author = UserNestedSerializer(read_only=True)
    exercise = ExercisePlanNestedSerializer(read_only=True, many=True)
    trainings = TrainingSerializer(read_only=True, many=True)

    class Meta:
        model = TrainingPlan
        fields = ["id", "title", "author", "exercise", "trainings"]
