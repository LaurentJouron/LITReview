from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Model, ForeignKey, CASCADE


class User(AbstractUser):
    """
    Custom user model extending the AbstractUser model provided by Django.

    This model represents a user with additional customizations.

    Methods:
        save(*args, **kwargs): Overrides the save method to ensure that the username is always stored in lowercase.

    Attributes:
        username (str): The username of the user, stored in lowercase.
    """

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure that the username is always stored in lowercase.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The capitalized username of the user.
        """
        return f'{self.username.capitalize()}'


class UserFollows(Model):
    """
    Model class representing the relationship between users for tracking followers/following.

    This model is used to establish a relationship between users where one user follows another user.
    It represents the 'following' relationship between users.

    Attributes:
        user (ForeignKey): The user who is following another user.
        followed_user (ForeignKey): The user who is being followed by another user.
    """

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
