from rest_framework import serializers

from workout.models import Training, TrainingPlan


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ["workday", "duration", "completed"]
