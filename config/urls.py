from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path

import authentication.views

import reviews.views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Authentication
    path(
        "",
        LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path("logout", LogoutView.as_view(), name='logout'),
    path('signup', authentication.views.signup_page, name='signup'),
    path(
        'change-password/',
        PasswordChangeView.as_view(
            template_name='authentication/password_change_form.html'
        ),
        name='password_change',
    ),
    path(
        'change-password-done/',
        PasswordChangeDoneView.as_view(
            template_name='authentication/password_change_done.html'
        ),
        name='password_change_done',
    ),
    # Blog
    path("home/", reviews.views.home, name='home'),
    path('ticket/upload/', reviews.views.ticket_upload, name='ticket_upload'),
    path(
        'ticket/<int:ticket_id>', reviews.views.view_ticket, name='view_ticket'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
