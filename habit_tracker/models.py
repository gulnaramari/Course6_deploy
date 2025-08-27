from datetime import timedelta
from django.db import models
from users.models import User


class Habit(models.Model):
    """Модель Привычка"""

    name = models.CharField(
        max_length=140, verbose_name="Название привычки", blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец привычки",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Место выполнения привычки",
        help_text="Введите место для выполнения привычки",
    )
    date_begin = models.TimeField(
        verbose_name="Дата начала выполнения", blank=True, null=True
    )
    action = models.CharField(
        max_length=140,
        verbose_name="Действие для привычки",
        help_text="Введите действие, чтобы обозначить привычку",
        blank=True,
        null=True,
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Выберите, будет ли привычка приятной."
        "Только приятная привычка будет наградой"
        " после выполнения полезной привычки.",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        related_name="related_habits",
        help_text="Выберите привычку, связанную с данной привычкой."
        " Условие: Привычка должна быть полезной.",
        blank=True,
        null=True,
    )
    periodicity = models.PositiveSmallIntegerField(
        default=7,
        verbose_name="Периодичность выполнения привычки",
        help_text="Выберите, какая будет периодичность выполнения привычки."
        " По умолчанию ежедневная",
    )
    award = models.CharField(
        max_length=100,
        verbose_name="Вознаграждение",
        help_text="Введите, чем пользователь должен себя вознаградить после выполнения привычки.",
        blank=True,
        null=True,
    )
    execution_time = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name="Время, которое потребуется для выполнения привычки",
        help_text="Введите время, которое потребуется для выполнения привычки."
        " По умолчанию дается 2 минуты",
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Привычка находится в публичном доступе"
    )

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        if self.owner:
            return (
                f"{self.owner.email} - {self.action} - {self.place} - {self.date_begin}"
            )
        return f"не найдено владельца привычки - {self.action} - {self.place} - {self.date_begin}"
