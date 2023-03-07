from django.urls import path
from django.contrib.auth.views import LoginView

from authentication import views

urlpatterns = [
    path(
        "",
        LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True,
        ),
        name='index',
    ),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]
