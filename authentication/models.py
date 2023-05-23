from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by',
    )

    class Meta:
        unique_together = (
            'user',
            'followed_user',
        )

    def __str__(self) -> str:
        return (
            f"{self.user.username.lower()} follows "
            + f"{self.followed_user.username.lower()}"
        )
