from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.FluxView.as_view()), name='home'),
    path('posts/', login_required(views.PostView.as_view()), name='posts'),
    path(
        'create-ticket/',
        login_required(views.CreateTicket.as_view()),
        name='create_ticket',
    ),
    path(
        'create-review/',
        login_required(views.CreateReview.as_view()),
        name='create_review',
    ),
    path(
        'ticket/<int:ticket_id>/update/',
        login_required(views.UpdateTicket.as_view()),
        name='update_ticket',
    ),
    path(
        'ticket/<int:ticket_id>/delete/',
        login_required(views.DeleteTicket.as_view()),
        name='delete_ticket',
    ),
    path(
        'ticket/<int:ticket_id>/create-review/',
        login_required(views.CreateReviewExistingTicket.as_view()),
        name='create_review_selected_ticket',
    ),
    path(
        'review/<int:review_id>/update',
        login_required(views.UpdateReview.as_view()),
        name='update_review',
    ),
    path(
        'review/<int:review_id>/delete/',
        login_required(views.DeleteReview.as_view()),
        name='delete_review',
    ),
]
