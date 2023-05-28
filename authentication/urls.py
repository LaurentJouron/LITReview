from django.urls import path
from authentication import views
from django.contrib.auth.decorators import login_required

"""
URL configuration for authentication-related views.

This file defines the URL patterns for the authentication views, such as login, logout, signup, subscriptions,
and unsubscribe.

Path patterns:
    - "" : The root URL pattern that maps to the LoginView class.
    - "logout" : URL pattern for logging out the user.
    - "signup" : URL pattern for signing up a new user.
    - "subscriptions" : URL pattern for tracking subscriptions, with login required.
    - "<int:sub_id>/unsubscribe" : URL pattern for unsubscribing from a specific user, with login required.

Note:
    The login_required decorator is used to ensure that only authenticated users can access certain views.

Usage:
    Include this URL configuration in your main project URLs to enable authentication-related functionality.
"""

urlpatterns = [
    path("", views.LoginView.as_view(), name='login'),
    path("logout", views.logout_user, name='logout'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path(
        'subscriptions',
        login_required(views.SubscriptionView.as_view()),
        name='subscriptions',
    ),
    path(
        '<int:sub_id>/unsubscribe',
        login_required(views.Unsubscribe.as_view()),
        name='unsubscribe',
    ),
]
