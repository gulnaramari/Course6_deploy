from datetime import time, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Habit


User = get_user_model()


class HabitTestCase(APITestCase):
    """Тесты для работы с привычками."""
    @classmethod
    def setUpTestData(cls):
        """ Метод класса с начальными данными для тестов."""
        cls.user = User.objects.create(email='test@test.com')
        cls.habit = Habit.objects.create(
            name='Тест',
            place='Дом',
            date_begin='09:00:00',
            action='Уборка квартиры',
            is_pleasant=False,
            periodicity=2,
            award='Мороженое',
            execution_time=timedelta(seconds=90),
            is_public=True,
            owner=cls.user,
            related_habit=None
        )

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.client.force_authenticate(user=self.user)

    def create_habit(self, **kwargs):
        """Создает привычку с заданными аргументами (или по умолчанию)."""
        defaults = {
            'name': 'Тест',
            'place': 'Дом',
            'date_begin': '09:00:00',
            'action': 'Что-нибудь',
            'is_pleasant': False,
            'periodicity': 2,
            'award': 'Мороженое',
            'execution_time': timedelta(seconds=90),
            'is_public': True,
            'owner': self.user,
            'related_habit': None
        }
        defaults.update(kwargs)
        return Habit.objects.create(**defaults)

    def test_habit_create(self):
        """Тест создания новой привычки."""
        url = reverse('habit_tracker:adding_habit')
        response = self.client.post(url, {
            'name': 'Тест2',
            'place': 'Улица',
            'date_begin': '07:20:00',
            'action': 'Гулять с собакой',
            'is_pleasant': False,
            'periodicity': 7,
            'award': 'Игра в компьютер',
            'execution_time': '00:01:30',
            'is_public': True,
            'owner': self.user.id,
            'related_habit': ''
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.last().name, 'Тест2')
        self.assertEqual(Habit.objects.last().place, 'Улица')
        self.assertEqual(Habit.objects.last().date_begin, time(7, 20))
        self.assertEqual(Habit.objects.last().action, 'Гулять с собакой')
        self.assertEqual(Habit.objects.last().is_pleasant, False)
        self.assertEqual(Habit.objects.last().periodicity, 7)
        self.assertEqual(Habit.objects.last().award, 'Игра в компьютер')
        self.assertEqual(Habit.objects.last().execution_time, timedelta(seconds=90))
        self.assertEqual(Habit.objects.last().is_public, True)
        self.assertEqual(Habit.objects.last().owner, self.user)
        self.assertEqual(Habit.objects.last().related_habit, None)


    def test_habit_retrieve(self):
        """Тест получения привычки по pk."""
        url = reverse('habit_tracker:habit', kwargs={'pk': self.habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.habit.id,
            'name': self.habit.name,
            'place': self.habit.place,
            'date_begin': self.habit.date_begin,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'periodicity': self.habit.periodicity,
            'award': self.habit.award,
            'execution_time': '00:01:30',
            'is_public': self.habit.is_public,
            'owner': self.user.id,
            'related_habit': self.habit.related_habit
        }
        self.assertEqual(response.data, expected_data)

    def test_habit_update(self):
        """Тест изменения привычки по pk."""
        url = reverse('habit_tracker:update_habit', kwargs={'pk': self.habit.id})
        updated_data = {
            'name': 'Updated Habit',
            'place': 'Somewhere',
            'date_begin': '05:30:00',
            'action': 'Something',
            'is_pleasant': False,
            'periodicity': 2,
            'award': 'Something',
            'execution_time': '00:02:00',
            'is_public': False,
            'owner': self.user.id,
            'related_habit': None
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, updated_data['name'])
        self.assertEqual(self.habit.place, updated_data['place'])
        self.assertEqual(self.habit.date_begin, time(hour=5, minute=30))
        self.assertEqual(self.habit.action, updated_data['action'])
        self.assertEqual(self.habit.is_pleasant, updated_data['is_pleasant'])
        self.assertEqual(self.habit.periodicity, updated_data['periodicity'])
        self.assertEqual(self.habit.award, updated_data['award'])
        self.assertEqual(self.habit.execution_time, timedelta(seconds=120))
        self.assertEqual(self.habit.is_public, updated_data['is_public'])
        self.assertEqual(self.habit.owner.id, updated_data['owner'])
        self.assertEqual(self.habit.related_habit, updated_data['related_habit'])

    def test_habit_delete(self):
        """Тест удаления привычки по Primary Key."""
        url = reverse('habit_tracker:delete_habit', kwargs={'pk': self.habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())