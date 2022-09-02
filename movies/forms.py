from dataclasses import fields
# from socket import fromshare
from django import forms

from .models import Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя', 'class':'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'placeholder': 'Пароль', 'type':'password'})) 