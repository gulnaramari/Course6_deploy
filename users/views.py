from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .permissions import IsUserOwner
from .serializer import (
    UserSerializer,
    CreateUserBaseSerializer,
    UserBaseSerializer,
)


class UserListAPIView(generics.ListAPIView):
    """Класс для эндпоинта списка пользователей."""

    serializer_class = UserBaseSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для эндпоинта просмотра деталей о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Метод получения сериализатора в соответствии с запросом."""

        if (
            self.request.method == "GET"
            and self.get_object() != self.request.user
            or self.request.user.is_superuser is False
        ):
            return UserBaseSerializer
        if self.request.user.is_superuser:
            return UserSerializer
        return UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Класс для эндпоинта создания пользователя."""

    serializer_class = CreateUserBaseSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Пользователя"."""

        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Класс для эндпоинта редактирования деталей пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Класс для эндпоинта удаления пользователя."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]
