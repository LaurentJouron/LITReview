from django.urls import include, path
from django.contrib.auth.views import LoginView

from authentication import views

# app_name = 'authentication'
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('signup/', views.signup, name='signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]
