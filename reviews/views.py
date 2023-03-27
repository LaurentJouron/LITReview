from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from PIL import Image

from . import forms, models


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', {'ticket': ticket})


@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request, 'reviews/ticket_upload.html', context={'form': form}
    )


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_form' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect(settings.LOGIN_REDIRECT_URL)
            if 'delete_ticket' in request.POST:
                delete_form = forms.DeleteTicketForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'reviews/edit_ticket.html', context=context)


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(
        request,
        'reviews/home.html',
        context={'reviews': reviews, 'tickets': tickets},
    )
