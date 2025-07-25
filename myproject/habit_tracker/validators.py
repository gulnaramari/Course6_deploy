from datetime import timedelta
from rest_framework import serializers


class BaseValidator:
    """ Базовый класс для проверок. """
    def __init__(self, *fields):
        """ Инициализатор класса. """
        self.fields = fields

    def __call__(self, attrs):
        """ Вызов django для валидации """
        field_values = {field: attrs.get(field) for field in self.fields}
        self.validate(**field_values)

    def validate(self, **kwargs):
        """ Реализуется в дочерних классах. """
        raise NotImplementedError('Подклассы должны реализовывать этот метод.')


class AwardOrRelated(BaseValidator):
    """ Исключить одновременный выбор связанной привычки и указания вознаграждения. """
    def validate(self, is_pleasant, related_habit, award, **kwargs):
        if award and related_habit:
            raise serializers.ValidationError(
                'не должно быть заполнено одновременно'
                ' и поле вознаграждения, и поле связанной привычки.'
            )


class ExecutionTime(BaseValidator):
    """ Проверяет время выполнения привычки. """
    def validate(self, execution_time, **kwargs):
        if execution_time and execution_time > timedelta(seconds=120):
            raise serializers.ValidationError(
                'Время выполнения должно составлять не более двух минут.'
            )


class RelatedPleasant(BaseValidator):
    """ Проверяет, что в связанные привычки могут
     попадать только привычки с признаком приятной привычки"""
    def validate(self, related_habit, **kwargs):
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                'Выбранная привычка должна обладать характеристиками приятной привычки.'
            )


class HabitPleasant(BaseValidator):
    """ Запрещает указывать вознаграждение или связанную привычку, если текущая привычка приятная. """
    def validate(self, is_pleasant, award, related_habit, **kwargs):
        """Метод для валидации на исходный признак приятности привычки"""
        if is_pleasant and (award or related_habit):
            raise serializers.ValidationError(
                'У исходно приятной привычки не может быть еще награды или связанной с ней привычки.'
            )


class FrequencyValidator(BaseValidator):
    """ Запрещается выполнять данную привычку реже, чем раз в 7 дней. """
    def validate(self, periodicity, **kwargs):
        """Метод для проверки."""
        if periodicity and not (1 <= periodicity <= 7):
            raise serializers.ValidationError(
                'Периодичность выполнения какой-либо привычки не может быть реже, чем раз в 7 дней.'
            )


class PublicValidator(BaseValidator):
    """ Подтверждает, что связанная привычка является общедоступной, если текущая привычка является общедоступной. """
    def validate(self, related_habit, is_public, **kwargs):
        """Метод для проверки."""
        if related_habit and is_public:
            if not related_habit.is_public:
                raise serializers.ValidationError(
                    'Указанная связанная привычка должна быть опубликована.'
                )


class OwnerValidator(BaseValidator):
    """ Подтверждает, что связанная привычка принадлежит тому же владельцу, что и текущая привычка. """
    def validate(self, related_habit, owner):
        """Метод для проверки."""
        if related_habit is not None and related_habit.owner != owner:
            raise serializers.ValidationError(
                'Указанная связанная привычка должна быть создана Вами.'
            )