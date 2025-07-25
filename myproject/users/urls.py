from django.urls import path
from rest_framework.permissions import AllowAny
from .apps import UsersConfig
from .views import (
    UserListAPIView,
    UserRetrieveAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name

urlpatterns = [
    path("", UserListAPIView.as_view(), name="list"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="detail"),
    path("registration/", UserCreateAPIView.as_view(), name="registration"),
    path("detail/<int:pk>/update/", UserUpdateAPIView.as_view(), name="update_detail"),
    path("detail/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete_detail"),
    path("authorization/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="authorization"),
    path("refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]
