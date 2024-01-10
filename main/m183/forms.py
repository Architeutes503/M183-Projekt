from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
)
from django.contrib.auth.models import User
from .models import Comment



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "custom-input"}), max_length=150
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
        
        
class UserUpdateForm(UserChangeForm):
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "custom-input"}), max_length=150
    )
    
    class Meta:
        model = User
        fields = ["username"]


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Current Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"
        for field_name in ["old_password", "new_password1", "new_password2"]:
            self.fields[field_name].widget.attrs.update({"class": "custom-input"})
            
            
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50, 'class': 'resizable-textarea'}),
        max_length=200
    )

    class Meta:
        model = Comment
        fields = ["content"]