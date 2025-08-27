from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Проверяем, что email указан
        if not email:
            raise ValueError(_("Email must be set"))

        # Приводим к нижнему регистру через normalize_email
        email = self.normalize_email(email)
        # Cоздаем объект пользователя
        user = self.model(email=email, **extra_fields)

        # Проверяем пароль
        if not password:
            user.set_unusable_password()  # Создаём пользователя без пароля
        else:
            user.set_password(password)  # Хэшируем и устанавливаем пароль

        # Только сейчас сохраняем пользователя в базу данных
        user.save(using=self._db)

    # Создаем обычного пользователя
    def create_user(self, email, password=None, **extra_fields):
        # Устанавливаем значения по умолчанию
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # Создаем суперпользователя
    def create_superuser(self, email, password=None, **extra_fields):
        # Устанавливаем значения по умолчанию для админа
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)