from django.urls import path
from .apps import UsersConfig
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserListAPIView


app_name = UsersConfig


urlpatterns = [
    path("", UserListAPIView.as_view(), name="profiles"),

    path(
        "authorization/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="authorization",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
