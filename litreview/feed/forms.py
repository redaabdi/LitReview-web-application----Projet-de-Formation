from django import forms
from .models import Ticket, Review, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']