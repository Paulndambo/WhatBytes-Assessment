from uuid import uuid4
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy

from users.forms import CustomUserCreationForm
from django.views import generic


from core.email_sender import SendMessage


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid credentials.")
    return render(request, "accounts/login.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


def forgot_password(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request, f"User with email: {email} not found.")
                return redirect("forgot-password")

            """
            Every time a forgot password request is send, a new user token is generated to avoid 
            re-using an already used token.
            """
            user_token = uuid4()
            user.token = user_token
            user.save()

            PASSWORD_RESET_LINK = (
                f"{settings.BASE_URL}/users/reset-password/{user_token}/"
            )

            context_data = {
                "username": user.username,
                "reset_link": PASSWORD_RESET_LINK,
                "subject": "Password Reset Instructions",
            }
            email_message = SendMessage()
            email_message.send_mail(
                context_data=context_data,
                recipient_list=[
                    email,
                ],
                template="forgot_password",
            )
            messages.success(request, "Password reset instructions sent. Check your email")
        except Exception as e:
            print(str(e))
            messages.error(request, "Error sending password reset email.")
            return redirect("forgot-password")
    return render(request, "accounts/forgot_password.html")


def reset_password(request, token):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            user = User.objects.filter(token=token).first()
            if not user:
                messages.error(request, "Invalid token.")
                return redirect("forgot-password")
            user.set_password(password)
            user.token = uuid4()
            user.save()
            context_data = {
                "username": user.username,
                "subject": "Password Reset Successful",
                "login_link": f"{settings.BASE_URL}/users/login/",
            }
            send_message = SendMessage()
            send_message.send_mail(
                context_data=context_data,
                recipient_list=[
                    user.email,
                ],
                template="password_change_success",
            )
            messages.success(request, "Password reset successful.")
            return redirect("password-change-success")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "accounts/reset_password.html", {"token": token})


def password_change_success(request):
    return render(request, "accounts/password_change_success.html")


@login_required
def user_profile(request):
    context = {
        "username": request.user.username,
        "email": request.user.email,
        "date_joined": request.user.date_joined,
        "last_login": request.user.last_login,
        "last_updated": request.user.modified_on,
    }
    return render(request, "accounts/profile.html", context)
