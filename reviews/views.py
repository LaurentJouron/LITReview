from django.forms import formset_factory
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from PIL import Image

from .models import Ticket, Review
from .forms import DeleteTicketForm, TicketForm, ReviewForm, EditForm
from authentication.models import User, UserFollows


@permission_required('reviews.add_ticket', raise_exception=True)
@login_required
def ticket_upload(request):
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
def create_ticket_and_review(request):
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
def create_multiple_ticket(request):
    TicketFormset = formset_factory(TicketForm, extra=3)
    formset = TicketFormset()
    if request.method == 'POST':
        formset = TicketFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    ticket = form.save(commit=False)
                    ticket.uploader = request.user.id
                    ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        'reviews/create_multiple_tickets.html',
        {'formset': formset},
    )


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', {'ticket': ticket})


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


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(
        request,
        'reviews/home.html',
        context={
            'tickets': tickets,
            'reviews': reviews,
        },
    )

    # @login_required
    # def home(request):
    # tickets = Ticket.objects.filter(
    #     Q(contributors__in=request.UserFollows.all()) | Q(starred=True)
    # )
    # reviews = Review.objects.filter(
    #     uploader__in=request.UserFollows.all()
    # ).exclude(review__in=reviews)
    # context = {
    #     'tickets': tickets,
    #     'reviews': reviews,
    # }
    # return render(request, 'reviews/home.html', context=context)
