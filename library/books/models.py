from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        "Author", on_delete=models.PROTECT, null=True, blank=True, related_name="books"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="author"
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_owner(self, user):
        return self.user == user
