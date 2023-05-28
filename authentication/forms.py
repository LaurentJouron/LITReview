from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.Form):
    """
    Form class for user login.

    This form is used to capture the username and password input from the user during login.

    Fields:
        username (CharField): Field for entering the username.
        password (CharField): Field for entering the password.

    Usage:
        Instantiate this form class in your view to handle user login.
        Render the form in your template and capture the submitted data.
    """

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
    """
    Form class for user signup.

    This form is used to capture the username and password input from the user during signup.
    It extends the UserCreationForm provided by Django.

    Fields:
        password1 (CharField): Field for entering the password.
        password2 (CharField): Field for confirming the password.

    Meta:
        model (User): The User model to be used for signup.
        fields (tuple): The fields to be included in the form.
        help_texts (dict): Help texts for the form fields.
        labels (dict): Labels for the form fields.
        widgets (dict): Custom widgets for the form fields.

    Usage:
        Instantiate this form class in your signup view to handle user signup.
        Render the form in your template and capture the submitted data.
    """

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
    """
    Form class for user subscription.

    This form is used to capture the username input from the user for subscription tracking.

    Fields:
        username (CharField): Field for entering the username.

    Usage:
        Instantiate this form class in your view to handle user subscription.
        Render the form in your template and capture the submitted data.
    """

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
