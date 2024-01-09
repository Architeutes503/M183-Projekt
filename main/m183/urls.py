from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    #Account management
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
    path("account/", views.account_view, name="account"),
    path("account/edit/", views.account_edit_view, name="account_edit"),
    path(
        "account/change_password/", views.password_change_view, name="password_change"
    ),
]
