from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(
        max_length=128,
        help_text="Each ticket has a title wich is book title and author.",
    )
    description = models.TextField(
        max_length=2048,
        blank=True,
        help_text="Each note needs a description, it must describe the book.",
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Each ticket has been created by one user.",
    )
    image = models.ImageField(
        null=True,
        blank=True,
        help_text="Each ticket can have an image, but he can be blank.",
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text="ticket creation date is automatically filled in.",
    )
    has_review = models.BooleanField(
        default=False,
        help_text="True, if at least one review exists for this ticket",
    )

    IMAGE_MAX_SIZE = (300, 300)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        self.resize_image()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} - by {self.user}"


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        help_text="Each review is related to Ticket describing a book or an",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Each review has rating wich is an integer number between 0 an",
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=(""),
        related_name='user',
    )
    headline = models.CharField(
        max_length=128,
        help_text="The headline can't be blank. Headline max length 128.",
    )
    body = models.TextField(
        max_length=8192,
        blank=True,
        help_text="The body can be blank. Body max length is 8192.",
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def _get_word_count(self):
        return len(self.body.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.headline} - by {self.user} - "
            + f"related to ticket {self.ticket.title}"
        )
