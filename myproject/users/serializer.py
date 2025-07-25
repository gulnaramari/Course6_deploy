from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователя."""

    class Meta:
        model = User
        fields = ["email", "avatar", "tg_chat_id", "tg_nickname",]


class UserBaseSerializer(serializers.ModelSerializer):
    """Класс сериализатора с ограниченным доступом к модели пользователя."""

    class Meta:
        model = User
        fields = ["email", "avatar",]


class CreateUserBaseSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для создания пользователя с ограниченным доступом."""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Класс для изменения поведения полей сериализатора"""

        model = User
        fields = ["email", "avatar", "password"]
