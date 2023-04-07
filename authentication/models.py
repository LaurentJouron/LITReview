from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from click import Group


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.user == self.creators:
    #         group = Group.objects.get(name='creators')
    #         group.user_set.add(self)
    #     elif self.UserFollows == self.subscribers:
    #         group = Group.objects.get(name='subscribers')
    #         group.user_set.add(self)


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

    def __str__(self):
        return f'{self.followed_user.username}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.user == self.creators:
    #         group = Group.objects.get(name='creators')
    #         group.user_set.add(self)
    #     elif self.UserFollows == self.subscribers:
    #         group = Group.objects.get(name='subscribers')
    #         group.user_set.add(self)

    class Meta:
        unique_together = (
            'user',
            'followed_user',
        )
