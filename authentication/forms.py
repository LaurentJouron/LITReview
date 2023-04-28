from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe"}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {"username": None}
        labels = {"username": ""}


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Mot de passe",
            }
        ),
    )

    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Confirmer mot de passe",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        help_texts = {"username": None}
        labels = {"username": ""}

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': "Nom d'utilisateur",
                }
            ),
        }


class SubscriptionForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label=False,
    )
