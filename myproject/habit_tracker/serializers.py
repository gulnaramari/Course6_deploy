from rest_framework import serializers

from .models import Habit
from .validators import AwardOrRelated, ExecutionTime, RelatedPleasant, HabitPleasant, \
    FrequencyValidator, PublicValidator, OwnerValidator


class HabitSerializer(serializers.ModelSerializer):
    """ Класс сериализатора с ограниченным доступом к модели "Привычки" (только для чтения). """

    related_habit_id = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        source='related_habit',
        write_only=True,
        allow_null=True,
        default=None
    )

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Привычки"."""

        model = Habit
        fields = [
            'id', 'name', 'place', 'date_completion', 'action', 'is_pleasant',
            'periodicity', 'award', 'execution_time', 'is_public', 'owner',
            'related_habit', 'related_habit_id'
        ]
        validators = [
            AwardOrRelated('is_pleasant', 'related_habit', 'award'),
            ExecutionTime('execution_time'),
            RelatedPleasant('related_habit'),
            HabitPleasant('is_pleasant', 'award', 'related_habit'),
            FrequencyValidator('periodicity'),
            PublicValidator('related_habit', 'is_public'),
            OwnerValidator('related_habit', 'owner')
        ]