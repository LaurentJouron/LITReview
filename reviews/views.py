from django.db.models import Value, CharField, Q
from django.conf import settings
from itertools import chain
from django.views.generic import View
from django.shortcuts import render, redirect
from itertools import chain

from reviews.models import Ticket, Review
from reviews.forms import TicketForm, ReviewForm
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
        # Get the list of users subscribed to the current user
        subscribers = [
            user.user
            for user in UserFollows.objects.filter(followed_user=request.user)
        ]

        # Get the tickets associated with the current user or the subscribers
        tickets = Ticket.objects.filter(
            Q(user=request.user) | Q(user__in=subscribers)
        )
        # Annotate the tickets with a content_type field set to 'TICKET'
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Get the reviews associated with the current user or the subscribers
        reviews = Review.objects.filter(
            Q(user=request.user) | Q(user__in=subscribers)
        )
        # Annotate the reviews with a content_type field set to 'REVIEW'
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # Combine the tickets and reviews into a single list
        posts = chain(tickets, reviews)
        # Sort the posts by time of creation in descending order
        posts = sorted(posts, key=lambda post: post.time_created, reverse=True)

        # Prepare the context for rendering the template
        context = {'posts': posts}

        # Render the template with the provided context
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
        # Get the tickets created by the user
        tickets = Ticket.objects.filter(user=request.user)
        # Annotate the tickets with a content_type field set to 'TICKET'
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Get the reviews created by the user
        reviews = Review.objects.filter(user=request.user)
        # Annotate the reviews with a content_type field set to 'REVIEW'
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # Combine the tickets and reviews into a single list
        posts = sorted(
            chain(tickets, reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )

        # Prepare the context for rendering the template
        context = {'posts': posts}

        # Render the template with the provided context
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
        # Create an instance of the ticket creation form
        form = self.form_class()
        # Prepare the context for rendering the template
        context = {'form': form, 'mode': 'CREATION'}
        # Render the template with the provided context
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
        # Create an instance of the ticket creation form with the POST data
        form = self.form_class(request.POST, request.FILES)
        # Check if the form is valid
        if form.is_valid():
            # Save the ticket with the user as the creator
            ticket = form.save(commit=False)
            ticket.user_id = request.user.id
            ticket.save()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If the form is invalid, render the ticket creation template with the form and validation errors
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
        # Retrieve the ticket to be updated
        ticket = Ticket.objects.get(id=ticket_id)
        # Create an instance of the ticket update form pre-filled with the ticket's current data
        form = self.form_class(instance=ticket)
        # Prepare the context for rendering the template
        context = {'form': form, 'mode': 'EDITING'}
        # Render the template with the provided context
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
        # Retrieve the ticket to be updated
        ticket = Ticket.objects.get(id=ticket_id)
        # Create an instance of the ticket update form with the POST data and the ticket instance
        form = self.form_class(request.POST, request.FILES, instance=ticket)
        # Check if the form is valid
        if form.is_valid():
            # Save the updated ticket
            form.save()
            # Perform additional actions, such as resizing the image
            ticket.resize_image()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If the form is invalid, render the ticket update template with the form and validation errors
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
        # Retrieve the ticket to be deleted
        ticket = Ticket.objects.get(id=ticket_id)
        # Check if the current user is the owner of the ticket
        if ticket.user == request.user:
            # Prepare the context for rendering the template
            context = {'ticket': ticket, 'content_type': 'TICKET'}
            # Render the template with the provided context
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
        # Retrieve the ticket to be deleted
        ticket = Ticket.objects.get(id=ticket_id)
        # Check if the current user is the owner of the ticket
        if ticket.user == request.user:
            # Delete the ticket
            ticket.delete()
            # Redirect the user to the login redirect URL
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
        # Create instances of the ticket form and the review form
        ticket_form = self.ticket_form()
        review_form = self.review_form()
        # Prepare the context for rendering the template
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
            'existing_ticket': False,
            'mode': 'CREATION',
        }
        # Render the template with the provided context
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
        # Create instances of the ticket form and the review form with the POST data
        ticket_form = self.ticket_form(request.POST, request.FILES)
        review_form = self.review_form(request.POST, request.FILES)
        # Check if both forms are valid
        if ticket_form.is_valid() and review_form.is_valid():
            # Save the ticket form data and associate it with the current user
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # Save the review form data and associate it with the ticket and the current user
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            # Update the review status of the associated ticket
            review.ticket.has_review = True
            review.ticket.save()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If either form is invalid, render the review creation template with the forms
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
        # Create an instance of the review form
        form = self.form_class()
        # Retrieve the specified ticket
        ticket = Ticket.objects.get(id=ticket_id)
        # Prepare the context for rendering the template
        context = {
            'review_form': form,
            'ticket': ticket,
            'existing_ticket': True,
            'mode': 'CREATION',
        }
        # Render the template with the provided context
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
        # Create an instance of the review form with the POST data
        form = self.form_class(request.POST, request.FILES)
        # Retrieve the specified ticket
        ticket = Ticket.objects.get(id=ticket_id)
        # Check if the form is valid
        if form.is_valid():
            # Save the review form data and associate it with the ticket and the current user
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            # Update the review status of the ticket
            review.ticket.has_review = True
            review.save()
            review.ticket.save()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If the form is invalid, render the review creation template with the form and ticket details
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
        # Retrieve the specified review
        review = Review.objects.get(id=review_id)
        # Create an instance of the review form with the review data
        form = self.form_class(instance=review)
        # Prepare the context for rendering the template
        context = {
            'review_form': form,
            'ticket': review.ticket,
            'existing_ticket': True,
            'mode': 'EDITING',
        }
        # Render the template with the provided context
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
        # Retrieve the specified review
        review = Review.objects.get(id=review_id)
        # Create an instance of the review form with the updated POST data and the existing review instance
        form = self.form_class(request.POST, instance=review)
        # Check if the form is valid
        if form.is_valid():
            # Save the updated review
            form.save()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If the form is invalid, render the review form template with the form and review details
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
        # Retrieve the specified review
        review = Review.objects.get(id=review_id)
        # Check if the review belongs to the authenticated user
        if review.user == request.user:
            # Prepare the context for rendering the template
            context = {'review': review, 'content_type': 'REVIEW'}
            # Render the delete confirmation page with the provided context
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
        # Retrieve the specified review
        review = Review.objects.get(id=review_id)
        # Check if the review belongs to the authenticated user
        if review.user == request.user:
            # Delete the review
            review.delete()
            # Redirect the user to the login redirect URL
            return redirect(settings.LOGIN_REDIRECT_URL)
