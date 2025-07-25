from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .paginators import HabitPaginator
from .serializers import HabitSerializer
from users.permissions import IsOwner


class HabitsListAPIView(generics.ListAPIView):
    """Класс для эндпоинта списка привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Метод для изменения запроса  к базе данных (фильтрации по объектам модели привычки)"""

        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(Q(owner=user) | Q(is_public=True)).order_by('id')
        else:
            return Habit.objects.filter(is_public=True).order_by('id')


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для эндпоинта просмотра привычки."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс для эндпоинта создания привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод присваивает привычку владельцу"""

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Класс для эндпоинта изменения привычки."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс для эндпоинта удаления привычки."""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
