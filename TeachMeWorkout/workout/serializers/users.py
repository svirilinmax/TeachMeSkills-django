from rest_framework import serializers
from django.contrib.auth import get_user_model
from workout.models import Coach

User = get_user_model()


class UserNestedSerializer(serializers.ModelSerializer):
    is_coach = serializers.SerializerMethodField(help_text="Is coach means is coach")

    def get_is_coach(self, user: User) -> bool:
        return hasattr(user, "coach")

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_coach"]


class CoachSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ["id", "user"]