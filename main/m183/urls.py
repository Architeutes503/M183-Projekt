from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            authentication_form=CustomAuthenticationForm,
            template_name="account_management/login.html",
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
