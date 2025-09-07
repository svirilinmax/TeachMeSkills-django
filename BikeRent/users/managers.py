from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Проверяем, что email указан
        if not email:
            raise ValueError(_("Email must be set"))

        # Convert to lower case via normalize_email
        email = self.normalize_email(email)
        # Create a user object
        user = self.model(email=email, **extra_fields)

        # Check the password
        if not password:
            user.set_unusable_password()  # Create a user without a password
        else:
            user.set_password(password)  # Hash and set the password

        # Only now we save the user to the database
        user.save(using=self._db)

    # Create a regular user
    def create_user(self, email, password=None, **extra_fields):
        # Set default values
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # Create a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        # Set default values for admin
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)
