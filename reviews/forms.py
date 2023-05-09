from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre',
        }
        widget = forms.TextInput(
            attrs={
                'class': 'textbox textbox_title',
            }
        )


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
        }


class EditForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
