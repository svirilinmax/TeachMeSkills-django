import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models.functions import Lower

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField("Email", unique=True)
    first_name = models.CharField("Имя", max_length=255, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, blank=True)

    # Обязательные поля для Django Auth. Для админки
    is_active = models.BooleanField(default=True)       # Может ли пользователь войти
    is_staff = models.BooleanField(default=False)       # Доступ к админке
    is_superuser = models.BooleanField(default=False)   # Все права

    date_joined = models.DateTimeField(default=timezone.now)  # Дата регистрации

    objects = UserManager()

    # использует имя User: логин по email
    USERNAME_FIELD = "email"
    # Определяет, какие поля запрашивать (которые указал в []) при создании суперпользователя
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                Lower("email"), name="uniq_user_email_ci"   # В нижней регистр
            )
        ]
        ordering = ("-date_joined",)    # сортировка по дате убывания регистрации (от старого в новому)

    def __str__(self):
        return self.email