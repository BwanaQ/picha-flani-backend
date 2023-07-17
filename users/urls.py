
from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("login/", views.UserLoginAPIView.as_view(), name="login"),
    # path("", views.UserAPIView.as_view(), name="user-info"),
    # path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    # path("profile/avatar/", views.UserAvatarAPIView.as_view(), name="user-avatar"),
]