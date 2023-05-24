from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Model, ForeignKey, CASCADE


class User(AbstractUser):
    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username.capitalize()}'


class UserFollows(Model):
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='following',
    )
    followed_user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='followed_by',
    )

    class Meta:
        unique_together = (
            'user',
            'followed_user',
        )
