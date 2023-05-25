from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import SignupForm, LoginForm, SubscriptionForm
from .models import User, UserFollows


class SignupView(View):
    """
    Create a user account on the first login.
    Upon validation, the redirect sends to the home page.
    """

    template = 'authentication/signup.html'
    form = SignupForm
    model = User()

    def get(self, request):
        form = self.form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template, {'form': form})


class LoginView(View):
    """
    Log in to the site after the user have created an account.
    """

    template = 'authentication/login.html'
    form = LoginForm

    def get(self, request):
        form = self.form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'].lower(),
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

        message = 'Identifiants incorrects'
        context = {'form': form, 'message': message}
        return render(
            request,
            self.template,
            context=context,
        )


def logout_user(request):
    """
    Allows the user to log out and return to the authentication page.
    """
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


class SubscriptionView(View):
    """
    Tracks other users to see which tickets they have written.
    """

    template = 'authentication/subscription.html'
    form = SubscriptionForm

    def get(self, request):
        form = self.form()
        current_user = request.user
        subscriptions = []
        subscribers = []
        for subscription in UserFollows.objects.all():
            if subscription.user == current_user:
                subscriptions.append(subscription)
            if subscription.followed_user == current_user:
                subscribers.append(subscription.user)
        context = {
            'form': form,
            'current_user': current_user,
            'subscriptions': subscriptions,
            'subscribers': subscribers,
        }
        return render(
            request,
            self.template,
            context=context,
        )

    def post(self, request):
        form = self.form(request.POST)
        users = User.objects.all()
        if form.is_valid():
            entry = request.POST['username'].lower()
            followed_user = User.objects.get(username=entry)
            for user in users:
                if user.username == entry:
                    if followed_user != request.user:
                        print(followed_user)
                        print(request.user)
                        UserFollows.objects.create(
                            user=request.user, followed_user=followed_user
                        )
            return redirect('subscriptions')
        return render(request, self.template, {'form': form})


class Unsubscribe(View):
    """
    Stops tracking selected users.
    """

    template = 'authentication/unsubscribe.html'

    def get(self, request, sub_id=None):
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            context = {'followed_user': subscription.followed_user}
            return render(
                request,
                self.template,
                context=context,
            )

    def post(self, request, sub_id=None):
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            subscription.delete()
            return redirect('subscriptions')
