from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CurrentUserView, LoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", CurrentUserView.as_view(), name="user_me"),
]
