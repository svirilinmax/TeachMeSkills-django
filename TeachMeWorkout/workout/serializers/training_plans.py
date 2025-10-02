from rest_framework import serializers
from .users import UserNestedSerializer
from .exercises import ExercisePlanNestedSerializer
from .trainings import TrainingSerializer
from workout.models import TrainingPlan


class TrainingPlanSerializer(serializers.ModelSerializer):
    author = UserNestedSerializer(read_only=True)
    exercise = ExercisePlanNestedSerializer(read_only=True, many=True)
    trainings = TrainingSerializer(read_only=True, many=True)

    class Meta:
        model = TrainingPlan
        fields = ["id", "title", "author", "exercise", "trainings"]
