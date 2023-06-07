from django.db.models import Value, CharField, Q
from django.conf import settings
from itertools import chain
from django.views.generic import View
from django.shortcuts import render, redirect
from itertools import chain

from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from authentication.models import UserFollows


class FluxView(View):
    """
    View class for handling the flux page.

    This class retrieves and displays a list of posts (tickets and reviews) based on the user's subscriptions.
    The posts are sorted by the time of creation, with the most recent ones appearing first.

    Attributes:
        template_name (str): The path to the template used for rendering the flux page.
    """

    template_name = "reviews/home.html"

    def get(self, request):
        """
        Handles GET requests to the flux view.

        Retrieves the user's subscribers, tickets, and reviews.
        Combines the tickets and reviews into a single list and sorts them by time of creation.
        Renders the flux template with the list of posts.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered flux template with the list of posts.
        """
        subscribers = [
            user.followed_user
            for user in UserFollows.objects.filter(user=request.user)
        ]

        tickets = Ticket.objects.filter(
            Q(user=request.user) | Q(user__in=subscribers)
        )
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(
            Q(user=request.user) | Q(user__in=subscribers)
        )
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = chain(tickets, reviews)
        posts = sorted(posts, key=lambda post: post.time_created, reverse=True)

        context = {'posts': posts}
        return render(request, self.template_name, context=context)


class PostView(View):
    """
    View class for handling the user's posts.

    This class retrieves and displays a list of posts (tickets and reviews) created by the user.
    The posts are sorted by the time of creation, with the most recent ones appearing first.

    Attributes:
        template_name (str): The path to the template used for rendering the posts page.
    """

    template_name = "reviews/posts_ticket.html"

    def get(self, request):
        """
        Handles GET requests to the post view.

        Retrieves the user's tickets and reviews.
        Combines the tickets and reviews into a single list and sorts them by time of creation.
        Renders the posts template with the list of posts.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered posts template with the list of posts.
        """
        tickets = Ticket.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        reviews = Review.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )
        context = {'posts': posts}
        return render(request, self.template_name, context=context)


class CreateTicket(View):
    """
    View class for creating a new ticket.

    This class handles the creation of a new ticket by the user.
    It provides a form for entering ticket details and saves the ticket upon successful validation.

    Attributes:
        template_name (str): The path to the template used for rendering the ticket creation form.
        form_class (class): The form class used for ticket creation input.
    """

    template_name = "reviews/ticket_form.html"
    form_class = TicketForm

    def get(self, request):
        """
        Handles GET requests to the ticket creation view.

        Creates an instance of the ticket creation form.
        Renders the ticket creation template with the form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered ticket creation template with the form.
        """
        form = self.form_class()
        context = {'form': form, 'mode': 'CREATION'}
        return render(request, self.template_name, context=context)

    def post(self, request):
        """
        Handles POST requests to the ticket creation view.

        Validates the ticket creation form data.
        If the form is valid, saves the ticket with the user as the creator.
        If the form is invalid, renders the ticket creation template with the form and validation errors.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse:
                - If the form is valid, redirects the user to the login redirect URL.
                - If the form is invalid, returns the response containing the rendered ticket creation template with the form.
        """
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user_id = request.user.id
            ticket.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {'form': form, 'mode': 'CREATION'}
        return render(request, self.template_name, context=context)


class UpdateTicket(View):
    """
    View class for updating a ticket.

    This class handles the updating of an existing ticket by the user.
    It retrieves the ticket to be updated, pre-fills the form with its current data,
    and saves the updated ticket upon successful validation.

    Attributes:
        template_name (str): The path to the template used for rendering the ticket update form.
        form_class (class): The form class used for ticket update input.
    """

    template_name = "reviews/ticket_form.html"
    form_class = TicketForm

    def get(self, request, ticket_id=None):
        """
        Handles GET requests to the ticket update view.

        Retrieves the ticket to be updated.
        Creates an instance of the ticket update form pre-filled with the ticket's current data.
        Renders the ticket update template with the form.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the ticket to be updated.

        Returns:
            HttpResponse: The response containing the rendered ticket update template with the form.
        """
        ticket = Ticket.objects.get(id=ticket_id)
        form = self.form_class(instance=ticket)
        context = {'form': form, 'mode': 'EDITING'}
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id=None):
        """
        Handles POST requests to the ticket update view.

        Retrieves the ticket to be updated.
        Validates the ticket update form data.
        If the form is valid, saves the updated ticket and performs additional actions.
        If the form is invalid, renders the ticket update template with the form and validation errors.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the ticket to be updated.

        Returns:
            HttpResponse:
                - If the form is valid, redirects the user to the login redirect URL.
                - If the form is invalid, returns the response containing the rendered ticket update template with the form.
        """
        ticket = Ticket.objects.get(id=ticket_id)
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            ticket.resize_image()
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {'form': form, 'mode': 'EDITING'}
        return render(request, self.template_name, context=context)


class Delete(View):
    """
    View class for deleting a ticket.

    This class handles the deletion of a ticket by the user.
    It confirms the deletion action and performs the deletion upon user confirmation.

    Attributes:
        template_name (str): The path to the template used for rendering the delete confirmation page.
    """

    template_name = 'reviews/delete.html'

    def get(self, request, ticket_id=None):
        """
        Handles GET requests to the delete view.

        Retrieves the ticket to be deleted.
        Checks if the current user is the owner of the ticket.
        Renders the delete confirmation template if the user is the owner.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the ticket to be deleted.

        Returns:
            HttpResponse: The response containing the rendered delete confirmation template.
        """
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            context = {'ticket': ticket, 'content_type': 'TICKET'}
            return render(request, self.template_name, context=context)

    def post(self, request, ticket_id=None):
        """
        Handles POST requests to the delete view.

        Retrieves the ticket to be deleted.
        Checks if the current user is the owner of the ticket.
        Deletes the ticket if the user is the owner.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the ticket to be deleted.

        Returns:
            HttpResponse: The response redirecting the user to the login redirect URL.
        """
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user == request.user:
            ticket.delete()
            return redirect(settings.LOGIN_REDIRECT_URL)


class CreateReview(View):
    """
    View class for creating a review.

    This class handles the creation of a new review by the user.
    It allows the user to submit a review along with an optional associated ticket.

    Attributes:
        template_name (str): The path to the template used for rendering the review creation form.
        ticket_form (class): The form class used for ticket input.
        review_form (class): The form class used for review input.
    """

    template_name = "reviews/review_form.html"
    ticket_form = TicketForm
    review_form = ReviewForm

    def get(self, request):
        """
        Handles GET requests to the review creation view.

        Creates instances of the ticket form and the review form.
        Renders the review creation template with the forms.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered review creation template with the forms.
        """
        ticket_form = self.ticket_form()
        review_form = self.review_form()
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'existing_ticket': False,
            'mode': 'CREATION',
        }
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id=None):
        """
        Handles POST requests to the review creation view.

        Validates the ticket form and the review form data.
        If both forms are valid, creates a new ticket and a new review associated with it.
        Updates the ticket's review status.
        Redirects the user to the login redirect URL.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the associated ticket (optional).

        Returns:
            HttpResponse:
                - If both forms are valid, redirects the user to the login redirect URL.
                - If either form is invalid, returns the response containing the rendered review creation template with the forms.
        """
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
        return render(request, self.template_name, context=context)


class CreateReviewExistingTicket(View):
    """
    View class for creating a review for an existing ticket.

    This class handles the creation of a new review associated with an existing ticket.
    It allows the user to submit a review for the specified ticket.

    Attributes:
        template_name (str): The path to the template used for rendering the review creation form.
        form_class (class): The form class used for review input.
    """

    template_name = "reviews/review_form.html"
    form_class = ReviewForm

    def get(self, request, ticket_id=None):
        """
        Handles GET requests to the review creation view for an existing ticket.

        Creates an instance of the review form.
        Retrieves the specified ticket.
        Renders the review creation template with the form and ticket details.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the existing ticket.

        Returns:
            HttpResponse: The response containing the rendered review creation template with the form and ticket details.
        """
        form = self.form_class()
        ticket = Ticket.objects.get(id=ticket_id)
        context = {
            'review_form': form,
            'ticket': ticket,
            'existing_ticket': True,
            'mode': 'CREATION',
        }
        return render(request, self.template_name, context=context)

    def post(self, request, ticket_id=None):
        """
        Handles POST requests to the review creation view for an existing ticket.

        Validates the review form data.
        If the form is valid, creates a new review associated with the specified ticket.
        Updates the review status of the ticket.
        Redirects the user to the login redirect URL.

        Args:
            request (HttpRequest): The HTTP request object.
            ticket_id (int): The ID of the existing ticket.

        Returns:
            HttpResponse:
                - If the form is valid, redirects the user to the login redirect URL.
                - If the form is invalid, returns the response containing the rendered review creation template with the form and ticket details.
        """
        form = self.form_class(request.POST, request.FILES)
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
        return render(request, self.template_name, context=context)


class UpdateReview(View):
    """
    View class for updating a review.

    This class handles the update of an existing review.
    It allows the user to edit and save changes to the review.

    Attributes:
        template_name (str): The path to the template used for rendering the review form.
        form_class (class): The form class used for review input.
    """

    template_name = "reviews/review_form.html"
    form_class = ReviewForm

    def get(self, request, review_id=None):
        """
        Handles GET requests to the review update view.

        Retrieves the specified review.
        Creates an instance of the review form with the review data.
        Renders the review form template with the form and review details.

        Args:
            request (HttpRequest): The HTTP request object.
            review_id (int): The ID of the review to be updated.

        Returns:
            HttpResponse: The response containing the rendered review form template with the form and review details.
        """
        review = Review.objects.get(id=review_id)
        form = self.form_class(instance=review)
        context = {
            'review_form': form,
            'ticket': review.ticket,
            'existing_ticket': True,
            'mode': 'EDITING',
        }
        return render(request, self.template_name, context=context)

    def post(self, request, review_id=None):
        """
        Handles POST requests to the review update view.

        Retrieves the specified review.
        Validates the updated review form data.
        If the form is valid, saves the updated review and redirects the user to the login redirect URL.
        If the form is invalid, returns the response containing the rendered review form template with the form and review details.

        Args:
            request (HttpRequest): The HTTP request object.
            review_id (int): The ID of the review to be updated.

        Returns:
            HttpResponse:
                - If the form is valid, redirects the user to the login redirect URL.
                - If the form is invalid, returns the response containing the rendered review form template with the form and review details.
        """
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
        return render(request, self.template_name, context=context)


class DeleteReview(View):
    """
    View class for deleting a review.

    This class handles the deletion of an existing review.
    It verifies if the review belongs to the authenticated user before deleting it.

    Attributes:
        template_name (str): The path to the template used for rendering the delete confirmation page.
    """

    template_name = "reviews/delete.html"

    def get(self, request, review_id=None):
        """
        Handles GET requests to the review deletion view.

        Retrieves the specified review.
        Checks if the review belongs to the authenticated user.
        Renders the delete confirmation page with the review details.

        Args:
            request (HttpRequest): The HTTP request object.
            review_id (int): The ID of the review to be deleted.

        Returns:
            HttpResponse: The response containing the rendered delete confirmation page with the review details,
                          or None if the review doesn't belong to the authenticated user.
        """
        review = Review.objects.get(id=review_id)
        if review.user == request.user:
            context = {'review': review, 'content_type': 'REVIEW'}
            return render(request, self.template_name, context=context)

    def post(self, request, review_id=None):
        """
        Handles POST requests to the review deletion view.

        Retrieves the specified review.
        Checks if the review belongs to the authenticated user.
        Deletes the review and redirects the user to the login redirect URL.

        Args:
            request (HttpRequest): The HTTP request object.
            review_id (int): The ID of the review to be deleted.

        Returns:
            HttpResponse: The response redirecting the user to the login redirect URL,
                          or None if the review doesn't belong to the authenticated user.
        """
        review = Review.objects.get(id=review_id)
        if review.user == request.user:
            review.delete()
            return redirect(settings.LOGIN_REDIRECT_URL)
