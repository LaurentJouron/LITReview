from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.decorators import login_required

from reviews.views import DeleteTicket, PostTicket
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
    path('signup', authentication.views.signup, name='signup'),
    # Blog
    path("home/", reviews.views.home, name='home'),
    path(
        'ticket/upload/',
        reviews.views.ticket_upload,
        name='ticket_upload',
    ),
    path(
        'ticket/<int:ticket_id>', reviews.views.view_ticket, name='view_ticket'
    ),
    path(
        'ticket/create_ticket_and_review',
        reviews.views.create_ticket_and_review,
        name='create_ticket_and_review',
    ),
    path(
        'ticket/<int:ticket_id>/edit',
        reviews.views.edit_ticket,
        name='edit_ticket',
    ),
    path(
        'ticket/<int:ticket_id>/delete/',
        login_required(DeleteTicket.as_view()),
        name='delete_ticket',
    ),
    path('posts/', login_required(PostTicket.as_view()), name='posts'),
    # Follower
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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
