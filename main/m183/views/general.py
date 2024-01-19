from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import logging
import random
import requests


logger = logging.getLogger(__name__)



from..models import (
    User,
    LoginAttempt
)

from ..forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    PasswordUpdateForm,
    ProfileForm,
    SMSCodeForm
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


def send_sms_code(mobile_number):
    code = f"{random.randint(100000, 999999)}"
    url = 'https://m183.gibz-informatik.ch/api/sms/message'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': 'NQA3ADQANQA4ADUANwA1ADMAOQA0ADQANAAxADcAMgA5ADMA',
    }
    payload = {
        'mobileNumber': mobile_number,
        'message': f'Your login code is {code}',
    }
    response = requests.post(url, headers=headers, json=payload)
    return code if response.status_code == 204 else None


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
                    profile = user.profile
                    sms_code = send_sms_code(profile.phone_number)
                    if sms_code:
                        request.session['username'] = username
                        request.session['password'] = request.POST.get('password')
                        LoginAttempt.objects.create(
                            username=username,
                            sms_code=sms_code,
                            code_expires=timezone.now() + timedelta(minutes=5)
                        )
                        return redirect("enter_sms_code")
                    else:
                        messages.error(request, "Failed to send SMS code.")
                        return redirect("login")
                else:
                    LoginAttempt.objects.create(username=username, timestamp=timezone.now())
            else:
                logger.info("User {} does not exist.".format(username))
                messages.warning(request, "No user with that username exists.")
                return redirect("login")
        else:
            form = AuthenticationForm()
        return render(request, "account_management/login.html", {"form": form})
    except Exception as e:
        print(e)
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
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated.")
            logger.info("User {} has successfully updated their account.".format(request.user.username))
            return redirect("account")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Edit Account",
    }

    return render(request, "account_management/account_edit.html", context)


def enter_sms_code_view(request):
    if request.method == "POST":
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            username = request.session.get('username')
            password = request.session.get('password')

            try:

                attempt = LoginAttempt.objects.get(
                    username=username,
                    sms_code=code,
                )

                if attempt.code_expires >= timezone.now():
                    # If the code is correct and not expired, authenticate the user's password
                    user = authenticate(username=attempt.username, password=password)
                    if user is not None:
                        login(request, user)
                        request.session.pop('username', None)
                        request.session.pop('password', None)
                        attempt.sms_code = ""
                        attempt.code_expires = datetime(year=2001, month=1, day=1)
                        attempt.save()
                        messages.success(request, "You have successfully logged in.")
                        return redirect("dashboard")
                    else:
                        messages.error(request, "Invalid password.")
                else:
                    messages.error(request, "Invalid or expired code.")
            except LoginAttempt.DoesNotExist:
                messages.error(request, "Invalid or expired code.")
        else:
            messages.error(request, "Invalid code format.")
    else:
        form = SMSCodeForm()

    return render(request, "account_management/enter_sms_code.html", {"form": form})