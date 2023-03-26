from django.urls import path
from authentication.views import LoginPage, SignupPage, logout_user


urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', SignupPage.as_view(), name='signup'),
]
