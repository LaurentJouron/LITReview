from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import SignupForm, LoginForm, SubscriptionForm
from .models import User, UserFollows


class SignupView(View):
    """
    View class for user signup functionality.

    This class handles the creation of a user account on the first login.
    Upon successful validation of the signup form, the user is redirected to the home page.

    Attributes:
        template_name (str): The path to the template used for rendering the signup page.
        form_class (class): The form class used for user signup input.
    """

    template_name = 'authentication/signup.html'
    form_class = SignupForm

    def get(self, request):
        """
        Handles GET requests to the signup view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered signup template with the signup form.
        """
        # Create an instance of the signup form
        form = self.form_class()
        # Render the signup template with the form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handles POST requests to the signup view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse:
                - If the signup form is valid, the response redirects the user to the home page after creating the account and logging in.
                - If the signup form is invalid, the response contains the rendered signup template with the form and validation errors.
        """
        # Create an instance of the signup form with the POST data
        form = self.form_class(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the user account
            user = form.save()
            # Log in the user
            login(request, user)
            # Redirect the user to the home page
            return redirect(settings.LOGIN_REDIRECT_URL)
        # If the form is invalid, render the signup template with the form and validation errors
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """
    View class for user login functionality.

    This class handles the user login process after the user has created an account.

    Attributes:
        template (str): The path to the template used for rendering the login page.
        form (class): The form class used for user login input.
    """

    template = 'authentication/login.html'
    form = LoginForm

    def get(self, request):
        """
        Handles GET requests to the login view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered login template with the login form.
        """
        # Create an instance of the login form
        form = self.form()
        # Render the login template with the form
        return render(request, self.template, {'form': form})

    def post(self, request):
        """
        Handles POST requests to the login view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered login template with the login form
                          and an error message if the login credentials are incorrect.
        """
        # Instantiates the login form with the POST data received
        form = self.form(request.POST)
        # Checks if the form is valid.
        if form.is_valid():
            # Authenticates the user using the credentials provided.
            user = authenticate(
                username=form.cleaned_data['username'].lower(),
                password=form.cleaned_data['password'],
            )
            # If authentication is successful:
            if user is not None:
                # Connects the user.
                login(request, user)
                # Redirects to the redirect URL after login.
                return redirect(settings.LOGIN_REDIRECT_URL)
        # Error message to display in case of failed authentication.
        error_message = 'Identifiants incorrects'
        # Context for rendering the template.
        context = {'form': form, 'error_message': error_message}
        # Renders the login template with the form and the error message.
        return render(
            request,
            self.template,
            context=context,
        )


def logout_user(request):
    """
    Logs out the user and redirects them to the authentication page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response that redirects the user to the logout redirect URL.
    """
    # Logs out the user
    logout(request)
    # Redirects the user to the logout redirect URL
    return redirect(settings.LOGOUT_REDIRECT_URL)


class SubscriptionView(View):
    """
    View class for managing user subscriptions to track other users' written tickets.

    This class allows users to subscribe to other users and view the tickets they have written.

    Attributes:
        template_name (str): The path to the template used for rendering the subscription page.
        form_class (class): The form class used for subscription input.
    """

    template_name = 'authentication/subscription.html'
    form_class = SubscriptionForm

    def get(self, request):
        """
        Handles GET requests to the subscription view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
        HttpResponse: The response containing the rendered subscription template with the subscription form,
                      the current user, the subscriptions, and the list of subscribers.
        """
        # Create an instance of the subscription form
        form = self.form_class()
        # Get the current user
        current_user = request.user
        # Get the subscriptions for the current user
        subscriptions = UserFollows.objects.filter(user=current_user)
        # Get the list of subscribers for the current user
        subscribers = UserFollows.objects.filter(
            followed_user=current_user
        ).values_list('user__username', flat=True)
        subscribers = [subscriber.capitalize() for subscriber in subscribers]
        # Create the context data to be passed to the template
        context = {
            'form': form,
            'current_user': current_user,
            'subscriptions': subscriptions,
            'subscribers': subscribers,
        }
        # Render the subscription template with the context data
        return render(
            request,
            self.template_name,
            context=context,
        )

    def post(self, request):
        """
        Handles POST requests to the subscription view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
        HttpResponse:
            - If the subscription form is valid, the response redirects the user to the 'subscriptions' URL after
            creating a new UserFollows object to establish the subscription.
            - If the subscription form is invalid or the username does not exist, the response contains the rendered
            subscription template with the form and an error message.
        """
        # Create an instance of the subscription form with the posted data
        form = self.form_class(request.POST)
        # Get all users
        users = User.objects.all()

        if form.is_valid():
            # Get the username from the form data
            entry = request.POST['username'].lower()
            # Check if the username exists in the User model
            followed_user = (
                User.objects.get(username=entry)
                if User.objects.filter(username=entry).exists()
                else None
            )
            if followed_user is None:
                # If the username does not exist, display an error message
                error_message = "Le nom d'utilisateur n'existe pas."
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'error_message': error_message},
                )
            # Iterate over all users
            for user in users:
                # Check if the username matches the entry
                if user.username == entry:
                    # Create a UserFollows object to establish the subscription
                    if followed_user != request.user:
                        UserFollows.objects.create(
                            user=request.user, followed_user=followed_user
                        )
            # Redirect the user to the 'subscriptions' URL
            return redirect('subscriptions')
        # If the form is invalid, render the subscription template with the form
        return render(request, self.template_name, {'form': form})


class Unsubscribe(View):
    """
    View class for unsubscribing from selected users.

    This class allows users to stop tracking selected users.

    Attributes:
        template (str): The path to the template used for rendering the unsubscribe page.
    """

    template = 'authentication/unsubscribe.html'

    def get(self, request, sub_id=None):
        """
        Handles GET requests to the unsubscribe view.

        Args:
            request (HttpRequest): The HTTP request object.
            sub_id (int, optional): The ID of the subscription to unsubscribe from.

        Returns:
        HttpResponse:
            - If the subscription belongs to the current user, the response contains the rendered unsubscribe template
              with information about the user to unsubscribe from.
        """
        # Get the subscription with the specified ID
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            # If the subscription belongs to the current user, create the context data
            context = {'followed_user': subscription.followed_user}
            # Render the unsubscribe template with the context data
            return render(
                request,
                self.template,
                context=context,
            )

    def post(self, request, sub_id=None):
        """
        Handles POST requests to the unsubscribe view.

        Args:
            request (HttpRequest): The HTTP request object.
            sub_id (int, optional): The ID of the subscription to unsubscribe from.

        Returns:
        HttpResponse:
            - If the subscription belongs to the current user, the response redirects the user to the 'subscriptions' URL
              after deleting the subscription.
        """
        # Get the subscription with the specified ID
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            # If the subscription belongs to the current user, delete the subscription
            subscription.delete()
            # Redirect the user to the 'subscriptions' URL
            return redirect('subscriptions')
