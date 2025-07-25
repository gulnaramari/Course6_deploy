from datetime import datetime

import eventlet
from celery import shared_task
from .services import send_message_by_telegram
from habit_tracker.models import Habit

eventlet.monkey_patch()

@shared_task
def send_habit_notification():
    """Отправляет напоминание о привычке"""
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    habits = Habit.objects.filter(
        date_begin__hour=hour_now, date_begin__minute=minute_now
    )
    for habit in habits:
        award_or_related_habit = (
            habit.award
            if habit.award
            else (
                habit.related_habit.name
                if habit.related_habit
                else "Никакого вознаграждения или связанной с ним привычки"
            )
        )
        message = f"""Привычка {habit.name}, действие: {habit.action}, место: {habit.place},
    время: {habit.date_begin}, награда или приятная привычка: {award_or_related_habit} """
        send_message_by_telegram(message, habit.owner.tg_chat_id)
        print(
            f"{habit.owner} - {habit.action} - {habit.place} отправить "
            f"{habit.owner} ({habit.owner.tg_nickname})"
        )
