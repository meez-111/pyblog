from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "register-email"}
        ),
    )

    first_name = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "First Name", "class": "register-first-name"}
        ),
    )
    last_name = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Last Name", "class": "register-last-name"}
        ),
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "register-username"}
        )
    )

    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "placeholder": "Password",
                "class": "register-password1",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "placeholder": "Confirm Password",
                "class": "register-password2",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_user(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "login-username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "placeholder": "Password",
                "class": "login-password",
            }
        )
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "update-email",
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "update-first-name",
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "update-last-name",
            }
        ),
    )

    username = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "update-username",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_user(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Current Password", "class": "current-password"}
        ),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "New Password", "class": "new-password"}
        ),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm New Password",
                "class": "confirm-new-password",
            }
        ),
    )
