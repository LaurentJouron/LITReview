from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from PIL import Image

from .forms import TicketForm
from .models import Ticket, Review


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', {'ticket': ticket})


@login_required
def ticket_upload(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.uploader = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request, 'reviews/ticket_upload.html', context={'form': form}
    )


# @login_required
# def edit_ticket(request, ticket_id):
#     ticket = get_object_or_404(TicketForm, id=ticket_id)
#     edit_form = TicketForm(instance=ticket)
#     delete_form = forms.DeleteTicketForm()
#     if request.method == 'POST':
#         if 'edit_form' in request.POST:
#             edit_form = TicketForm(request.POST, instance=ticket)
#             if edit_form.is_valid():
#                 edit_form.save()
#                 return redirect(settings.LOGIN_REDIRECT_URL)
#             if 'delete_ticket' in request.POST:
#                 delete_form = forms.DeleteTicketForm(request.POST)
#                 if delete_form.is_valid():
#                     ticket.delete()
#                     return redirect(settings.LOGIN_REDIRECT_URL)
#     context = {
#         'edit_form': edit_form,
#         'delete_form': delete_form,
#     }
#     return render(request, 'reviews/edit_ticket.html', context=context)


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(
        request,
        'reviews/home.html',
        context={'reviews': reviews, 'tickets': tickets},
    )
