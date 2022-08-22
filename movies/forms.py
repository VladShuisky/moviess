from dataclasses import fields
from socket import fromshare
from django import forms

from .models import Reviews

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя', 'class':'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'placeholder': 'Пароль', 'type':'password'})) 