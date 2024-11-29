from django.urls import path
from users.views import (
    login_user,
    forgot_password,
    reset_password,
    logout_user,
    user_profile,
    SignUpView,
    password_change_success,
)

urlpatterns = [
    path("login/", login_user, name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", user_profile, name="profile"),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path("reset-password/<uuid:token>/", reset_password, name="reset-password"),
    path(
        "password-change-success/",
        password_change_success,
        name="password-change-success",
    ),
    path("logout/", logout_user, name="logout"),
]
