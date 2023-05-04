from django.urls import path
from authentication import views
from django.contrib.auth.decorators import login_required

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
