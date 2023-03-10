from django.urls import path
from django.contrib.auth.views import LoginView

from reviews import views

# app_name = 'reviews'
urlpatterns = [
    path('', views.reviews, name='reviews'),
]
