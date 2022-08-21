from dataclasses import fields
from socket import fromshare
from django import forms

from .models import Reviews

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')

        