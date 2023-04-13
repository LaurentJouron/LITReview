from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User

from authentication.forms import LoginForm, SignupForm, SubscriptionForm
from authentication.models import UserFollows


class LoginPage(View):
    form_class = LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request,
            self.template_name,
            context={'form': form, 'message': message},
        )

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            message = ''
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    message = 'Identifiants incorrects.'
            return render(
                request,
                self.template_name,
                context={'form': form, 'message': message},
            )


def signup_page(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request, 'authentication/signup.html', context={'form': form}
    )


def logout_user(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


class SubscriptionPage(View):
    template_name = 'authentication/subscription.html'
    form_class = SubscriptionForm

    def get(self, request):
        form = self.form_class()
        current_user = request.user
        subscriptions, subscribers = [], []
        for subscription in UserFollows.objects.all():
            if subscription.user == current_user:
                subscriptions.append(subscription)
            if subscription.followed_user == current_user:
                subscribers.append(subscription)

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'current_user': current_user,
                'subscriptions': subscriptions,
                'subscribers': subscribers,
            },
        )

    def post(self, request):
        form = self.form_class(request.POST)
        users = User.objects.all()
        if form.is_valid():
            entry = request.POST['username']
            user_to_follow = User.objects.get(username=entry)
            for user in users:
                if user.username == entry:
                    UserFollows.objects.create(
                        user=request.user, followed_user=user_to_follow
                    )
            return redirect('subscriptions')

        return render(request, self.template_name, {'form': form})


class Unsubscribe(View):
    template_name = ('authentication/unsubscribe.html',)

    def get(self, request, sub_id=None):
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            return render(
                request,
                self.template_name,
                {'followed_user': subscription.followed_user},
            )

    def post(self, request, sub_id=None):
        subscription = UserFollows.objects.get(id=sub_id)
        if subscription.user == request.user:
            subscription.delete()
            return redirect('subscriptions')
