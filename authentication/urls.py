from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.decorators import login_required
import authentication.views

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path("logout", LogoutView.as_view(), name='logout'),
    path('signup', authentication.views.signup, name='signup'),
    path(
        'subscriptions',
        login_required(authentication.views.SubscriptionPage.as_view()),
        name='subscriptions',
    ),
    path(
        '<int:sub_id>/unsubscribe',
        login_required(authentication.views.Unsubscribe.as_view()),
        name='unsubscribe',
    ),
]
