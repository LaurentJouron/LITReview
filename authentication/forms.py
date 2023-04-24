from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(
        max_length=128, widget=forms.PasswordInput(), required=True
    )


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


class SubscriptionForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label=False,
    )
