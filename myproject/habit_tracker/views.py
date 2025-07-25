from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс для эндпоинта создания привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания "Привычки".
        присваивает привычку владельцу"""

        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()
