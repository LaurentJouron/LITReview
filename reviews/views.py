from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from PIL import Image

from .forms import TicketForm, ReviewForm
from .models import Ticket, Review


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', {'ticket': ticket})


@login_required
def ticket_and_reviews_upload(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user_id = request.user.id
            ticket.save()
            review = review_form.save(commit=False)
            review.user_id = request.user.id
            review.rating = ticket
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(
        request,
        'reviews/ticket_and_reviews_upload.html',
        context=context,
    )


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(
        request,
        'reviews/home.html',
        context={'tickets': tickets, 'reviews': reviews},
    )
