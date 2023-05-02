from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from reviews.views import DeleteTicket, PostTicket
import reviews.views

urlpatterns = [
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
]
