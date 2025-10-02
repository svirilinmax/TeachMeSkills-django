import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status, mixins, viewsets
from .models import Exercise, TrainingPlan, Coach
from django.db.models import Q
from .serializers import (
    CoachSerializer,
    ExerciseSerializer,
    ExerciseOnlyTitleSerializer,
    TrainingPlanSerializer
)
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import ExercisePermission
from .tasks import fill_plan_from_parent
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination


User = get_user_model()


class CoachViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Coach.objects.all().select_related("user")
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TrainingPlanViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TrainingPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = TrainingPlan.objects.all()

        if user.is_authenticated:
            queryset = queryset.filter(
                Q(author=user) | Q(author__coach__isnull=False)
            )
        else:
            queryset = queryset.filter(author__coach__isnull=False)

        return queryset.select_related("author").prefetch_related(
            "exercise", "exercise__exercise"
        )

    @action(detail=True, methods="post", url_name="duplication")
    def duplication(self, request, pk):
        try:
            plan = self.get_object()
            new_plan = TrainingPlan.objects.create(author=request.user if request.user.is_authenticated else plan.author)
            logger = logging.getLogger(__name__)


            logger.info("Starting Celery")
            fill_plan_from_parent.apply_async(
                kwargs={
                    "new_plan_id": new_plan.id,
                    "parent_plan_id": plan.id,
                },
                countdown=5
            )
            logger.info("Finishing Celery")


            serializer = self.get_serializer(new_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": "Failed to duplicate plan"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ExerciseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Exercise.objects.all().prefetch_related("plan")
    serializer_class = ExerciseSerializer
    permission_classes = [ExercisePermission]
    pagination_class = StandardResultsSetPagination

    # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]

        perms = [permissions.IsAuthenticated()]

        if self.action == "destroy":
            perms.append(permissions.IsAdminUser())

        return perms


    @action(detail=True, methods=["post"], url_path="duplicate")
    # exercises/<ID>/duplicate/
    def duplicate_exercise_with_prefix(self, request, pk=None):
        instance = self.get_object()
        data = {"title": instance.title + "DUPLICATE"}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="list-titles")
    @method_decorator(cache_page(60*15))
    # exercises/list_titles
    def list_titles(self, request):
        instances = self.get_queryset()
        serializer = ExerciseOnlyTitleSerializer(instances, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)