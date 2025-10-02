import uuid

from django.db import models


class BaseTimeStampedMixin:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True


class TimeStampedMixin(BaseTimeStampedMixin):
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name='Удалено')

    class Meta:
        abstract = True


class UUIDMixin:
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, auto_created=True
    )

    class Meta:
        abstract = True


class BaseModel(TimeStampedMixin, models.Model):

    class Meta:
        abstract = True


class BaseUUIDModel(UUIDMixin, BaseModel):

    class Meta:
        abstract = True
