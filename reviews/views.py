from django.db.models import Value, CharField
from django.conf import settings
from itertools import chain
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from reviews.models import Ticket, Review
from reviews.forms import DeleteTicketForm, TicketForm, ReviewForm, EditForm
from authentication.models import UserFollows


class FluxView(View):
    template = 'home.html'

    def get(self, request):
        subscribers = []
        for user in UserFollows.objects.all():
            if user.followed_user == request.user:
                subscribers.append(user.user)

        tickets = Ticket.objects.filter(
            user=request.user
        ) | Ticket.objects.filter(user__in=subscribers)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            user=request.user
        ) | Review.objects.filter(user__in=subscribers)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = chain(tickets, reviews)
        posts = sorted(posts, key=lambda post: post.time_created, reverse=True)
        context = {'posts': posts}
        return render(request, self.template, context=context)


class PostView(View):
    template = 'reviews/post.html'

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = chain(tickets, reviews)
        posts = sorted(posts, key=lambda post: post.time_created, reverse=True)
        context = {'posts': posts}
        return render(request, self.template, context=context)


class CreateTicket(View):
    template = ('reviews/ticket_form.html',)
    form = TicketForm

    def get(self, request):
        form = self.form()
        return render(
            request, self.template, {'form': form, 'mode': 'CREATION'}
        )

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {'form': form, 'mode': 'CREATION'}
        return render(request, self.template, context=context)


class UpdateTicket(View):
    form = TicketForm
    template = ('reviews/ticket_form.html',)

    def get(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        form = self.form(instance=ticket)
        context = {'form': form, 'mode': 'EDITING'}
        return render(request, self.template, context=context)

    def post(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        form = self.form(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            ticket.resize_image()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {'form': form, 'mode': 'EDITING'}
        return render(request, self.template, context=context)


class DeleteTicket(View):
    template = 'reviews/delete.html'

    def get(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            context = {'ticket': ticket, 'content_type': 'TICKET'}
            return render(request, self.template, context=context)

    def post(self, request, ticket_id=None):
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
            return redirect(settings.LOGIN_REDIRECT_URL)


class CreateReview(View):
    template = 'reviews/review_form.html'
    ticket_form = TicketForm
    review_form = ReviewForm

    def get(self, request):
        ticket_form = self.ticket_form()
        review_form = self.review_form()
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'existing_ticket': False,
            'mode': 'CREATION',
        }
        return render(request, self.template, context=context)

    def post(self, request, ticket_id=None):
        ticket_form = self.ticket_form(request.POST, request.FILES)
        review_form = self.review_form(request.POST, request.FILES)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            review.ticket.has_review = True
            review.ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'existing_ticket': False,
            'mode': 'CREATION',
        }
        return render(request, self.template, context=context)


class CreateReviewExistingTicket(View):
    template = 'reviews/review_form.html'
    form = ReviewForm

    def get(self, request, ticket_id=None):
        form = self.form()
        ticket = Ticket.objects.get(id=ticket_id)
        context = {
            'review_form': form,
            'ticket': ticket,
            'existing_ticket': True,
            'mode': 'CREATION',
        }
        return render(request, self.template, context=context)

    def post(self, request, ticket_id=None):
        form = self.form(request.POST, request.FILES)
        ticket = Ticket.objects.get(id=ticket_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.ticket.has_review = True
            review.save()
            review.ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'review_form': form,
            'ticket': ticket,
            'existing_ticket': True,
            'mode': 'CREATION',
        }
        return render(request, self.template, context=context)


class UpdateReview(View):
    form = ReviewForm
    template = 'reviews/review_form.html'

    def get(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        form = self.form(instance=review)
        context = {
            'review_form': form,
            'ticket': review.ticket,
            'existing_ticket': True,
            'mode': 'EDITING',
        }
        return render(request, self.template, context=context)

    def post(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        form = self.form_class(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {
            'review_form': form,
            'ticket': review.ticket,
            'existing_ticket': True,
            'mode': 'EDITING',
        }
        return render(request, self.template, context=context)


class DeleteReview(View):
    template = 'reviews/delete_reviews.html'

    def get(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        if review.user == request.user:
            context = {'review': review, 'content_type': 'REVIEW'}
            return render(request, self.template, context=context)

    def post(self, request, review_id=None):
        review = Review.objects.get(id=review_id)
        if review.user == request.user:
            review.delete()
            return redirect(settings.LOGIN_REDIRECT_URL)
