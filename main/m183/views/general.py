from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)



from..models import (
    User,
    LoginAttempt
)

from ..forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    PasswordUpdateForm
)





def register(request):  # sourcery skip: extract-method
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered.")
            logger.info("User {} has successfully registered.".format(username))
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "account_management/register.html", {"form": form})




def login_view(request):
    try:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            username = request.POST.get('username')
            if User.objects.filter(username=username).exists():
                if LoginAttempt.has_exceeded_limit(username):
                    messages.warning(request, "You have exceeded the limit of login attempts. Please try again later.")
                    logger.warning("User {} has exceeded the limit of login attempts.".format(username))
                    return redirect("home")
                if form.is_valid():
                    user = form.get_user()
                    login(request, user)
                    messages.success(request, "You have successfully logged in.")
                    logger.info("User {} has successfully logged in.".format(username))
                    return redirect("dashboard")
                else:
                    LoginAttempt.objects.create(username=username, timestamp=timezone.now())
            else:
                logger.info("User {} does not exist.".format(username))
                messages.warning(request, "No user with that username exists.")
                return redirect("login")
        else:
            form = AuthenticationForm()
        return render(request, "account_management/login.html", {"form": form})
    except Exception:
        messages.error(request, "An error occurred, please try again.")
        logger.error("An error occurred while logging in.")
        return redirect("home")


@login_required
def account_view(request):
    if request.method == "POST":
        if "edit_account" in request.POST:
            return redirect("account_edit")
        elif "change_password" in request.POST:
            return redirect("password_change")
    return render(request, "account_management/account_dashboard.html")


@login_required
def password_change_view(request):
    if request.method == "POST":
        password_form = PasswordUpdateForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Your password has been updated.")
            logger.info("User {} has successfully changed their password.".format(request.user.username))
            return redirect("account")
    else:
        password_form = PasswordUpdateForm(request.user)

    context = {
        "password_form": password_form,
        "title": "Change Password",
    }

    return render(request, "account_management/password_change.html", context)


@login_required
def account_edit_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your account has been updated.")
            logger.info("User {} has successfully updated their account.".format(request.user.username))
            return redirect("account")
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        "user_form": user_form,
        "title": "Edit Account",
    }

    return render(request, "account_management/account_edit.html", context)