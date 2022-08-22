from dataclasses import fields
from logging import PlaceHolder
from re import L
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    password = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'placeholder': 'Пароль', 'type':'password'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})