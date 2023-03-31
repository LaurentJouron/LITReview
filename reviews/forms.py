from dataclasses import field
from django import forms
from django.forms.widgets import RadioSelect

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'textbox form-textarea form-textarea-description',
                }
            ),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('headline', 'rating', 'body')
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}
        widgets = {
            'rating': forms.RadioSelect(
                choices=[
                    (0, '- 0'),
                    (1, '- 1'),
                    (2, '- 2'),
                    (3, '- 3'),
                    (4, '- 4'),
                    (5, '- 5'),
                ]
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'textbox form-textarea form-textarea-description',
                }
            ),
        }
