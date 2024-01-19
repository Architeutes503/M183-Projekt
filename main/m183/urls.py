from django.urls import path, re_path
from . import views
from .forms import CustomAuthenticationForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("post/<uuid:post_id>/", views.post_detail, name="post_detail"),    #Account management
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("account/", views.account_view, name="account"),
    path("account/edit/", views.account_edit_view, name="account_edit"),
    path(
        "account/change_password/", views.password_change_view, name="password_change"
    ),
    path("api/posts/", views.api_view, name="api"),
    path("enter_sms_code/", views.enter_sms_code_view, name="enter_sms_code"),
]
