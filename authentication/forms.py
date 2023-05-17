from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label=False,
        widget=forms.TextInput(
            attrs={
                "class": "textbox textbox_login_username",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "textbox textbox_login_password",
                "placeholder": "Mot de passe",
            }
        ),
    )


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "textbox textbox_signup_username",
                "placeholder": "Mot de passe",
            }
        ),
    )

    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "textbox textbox_signup_password",
                "placeholder": "Confirmer mot de passe",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")
        help_texts = {"username": None}
        labels = {"username": ""}

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "textbox textbox_signup_username",
                    "placeholder": "Nom d'utilisateur",
                }
            ),
        }


class SubscriptionForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label=False,
        widget=forms.TextInput(
            attrs={
                "class": "textbox subscription_textbox_username",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
