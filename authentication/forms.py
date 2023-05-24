from django.forms import Form, TextInput, CharField, PasswordInput
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(Form):
    username = CharField(
        max_length=50,
        label=False,
        widget=TextInput(
            attrs={
                "class": "textbox textbox_login_username",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
    password = CharField(
        max_length=50,
        label=False,
        widget=PasswordInput(
            attrs={
                "class": "textbox textbox_login_password",
                "placeholder": "Mot de passe",
            }
        ),
    )


class SignupForm(UserCreationForm):
    password1 = CharField(
        label=False,
        widget=PasswordInput(
            attrs={
                "class": "textbox textbox_signup_username",
                "placeholder": "Mot de passe",
            }
        ),
    )

    password2 = CharField(
        label=False,
        widget=PasswordInput(
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
            "username": TextInput(
                attrs={
                    "class": "textbox textbox_signup_username",
                    "placeholder": "Nom d'utilisateur",
                }
            ),
        }


class SubscriptionForm(Form):
    username = CharField(
        max_length=50,
        label=False,
        widget=TextInput(
            attrs={
                "class": "textbox subscription_textbox_username",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
