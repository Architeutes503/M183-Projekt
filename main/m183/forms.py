from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
)
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "custom-input"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "custom-input"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "custom-input"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        for field in self.fields.values():
            field.widget.attrs.update({"class": "custom-input"})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "custom-input"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "custom-input"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]