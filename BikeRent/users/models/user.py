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

    # Required fields for Django Auth. For admin
    is_active = models.BooleanField(default=True)       # Can the user log in
    is_staff = models.BooleanField(default=False)       # Access to admin panel
    is_superuser = models.BooleanField(default=False)   # All rights

    date_joined = models.DateTimeField(default=timezone.now)  # Date of registration

    objects = UserManager()

    # uses name User: login by email
    USERNAME_FIELD = "email"
    # Determines which fields to request (specified in []) when creating a superuser
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                Lower("email"), name="uniq_user_email_ci"   # Lowercase
            )
        ]
        ordering = ("-date_joined",)    # sort by registration date descending (oldest to newest)

    def __str__(self):
        return self.email