from multiprocessing.dummy import Value
from itertools import chain
from PIL import Image
from django.forms import CharField
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from reviews.models import Ticket, Review
from reviews.forms import DeleteTicketForm, TicketForm, ReviewForm, EditForm

# from authentication.models import User, UserFollows


@login_required
def ticket_upload(request):
    """
    This function gives the possibility to create a ticket, provided
    that it is authenticated and entitled to do so. It records the ID
    of the ticket creator. The function uses the creation of the TicketForm
    form of the forms.py file and ticket_update.html of templates/reviews.
    Once the ticket is created, the user is returning the home page.
    """
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user_id = request.user.id
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'ticket_form': ticket_form,
    }
    return render(
        request,
        'reviews/ticket_upload.html',
        context=context,
    )


@login_required
def home(request):
    """
    This function displays all tickets and comments, provided
    they are authenticated. home.html of templates/reviews.
    """
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    context = {
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(
        request,
        'reviews/home.html',
        context=context,
    )


@login_required
def create_ticket_and_review(request):
    """
    This function gives the possibility to create a ticket,
    a comment while evaluating the book.
    """
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
            review.ticket = ticket
            review.user_id = request.user.id
            review.ticket.has_review = True
            review.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(
        request,
        'reviews/create_ticket_and_review.html',
        context=context,
    )


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {'ticket': ticket}
    return render(request, 'reviews/view_ticket.html', context=context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_ticket = EditForm(instance=ticket)
    delete_ticket = DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_ticket = EditForm(request.POST, instance=ticket)
            if edit_ticket.is_valid():
                edit_ticket.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
            if 'delete_ticket' in request.POST:
                delete_ticket = DeleteTicketForm(request.POST)
                if delete_ticket.is_valid():
                    ticket.delete()
                    return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'reviews/edit_ticket.html', context=context)


class DeleteTicket(View):
    template_name: str = 'reviews/delete.html'

    def get(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            context = {'ticket': ticket, 'content_type': 'TICKET'}
            return render(
                request,
                self.template_name,
                context=context,
            )

    def post(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
            return redirect('posts')


class PostTicket(View):
    template_name = 'reviews/post_ticket.html'

    def get(self, request):
        ticket = Ticket.objects.filter(user=request.user)
        review = Review.objects.filter(user=request.user)
        posts = chain(ticket, review)
        posts = sorted(posts, key=lambda post: post.time_created, reverse=True)
        context = {'posts': posts}
        return render(request, self.template_name, context=context)
