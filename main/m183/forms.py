from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UserChangeForm,
)
from .models import Profile, Comment, User
from .models import Comment





class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={"class": "custom-input"}))

    class Meta:
        model = Profile
        fields = ['phone_number']


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
        self.profile_form = ProfileForm(*args, **(kwargs.get('instance') or {}))

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = self.profile_form.save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user


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
        
        
class SMSCodeForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)

    def clean_code(self):
        code = self.cleaned_data['code']
        return code