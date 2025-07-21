from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User

from .serializer import UserSerializer


class UserListAPIView(generics.ListAPIView):
    """Контроллер-дженерик для списка пользователей."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
