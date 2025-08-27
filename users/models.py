from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле 'email' обязательно для заполнения.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        verbose_name="username",
        help_text="Введите ваш логин(юзернейм)",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Введите ваш емейл"
    )
    avatar = models.ImageField(
        upload_to="users/images",
        null=True,
        blank=True,
        verbose_name="Аватар профиля",
        validators=[
            FileExtensionValidator(
                ["jpg", "png"],
                "Расширение файла « %(extension)s » не допускается. "
                "Разрешенные расширения: %(allowed_extensions)s ."
                "Недопустимое расширение!",
            )
        ],
    )
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="telegram chat id",
        help_text="Введите ваш id для телеграм чата",
        null=True,
        blank=True,
    )
    tg_nickname = models.CharField(
        max_length=32,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^@[A-Za-z0-9_]{4,31}$",
                message="Имя пользователя в Telegram должен начинаться с @"
                " и содержать только буквы, цифры и символы подчеркивания",
                code="invalid_telegram_nickname",
            )
        ],
        verbose_name="Имя пользователя в Telegram",
        blank=True,
        null=True,
    )
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username if self.username else self.email

    class Meta:
        """Класс для изменения поведения полей модели "Пользователь"."""

        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["email"]
