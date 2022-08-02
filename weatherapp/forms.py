from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class WeatherForm(forms.Form):
    city = forms.CharField(max_length=50, required=True, label='',
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Enter your city',
                               'style': 'width: 900px; height:50px;',
                               'class': 'form-control'
                           }))


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=32,
                               required=True,
                               label='',
                               widget=forms.TextInput(attrs={'class': 'signup', 'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=32,
                                required=True,
                                label='',
                                widget=forms.PasswordInput(attrs={'class': 'signup', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=32,
                                required=True,
                                label='',
                                widget=forms.PasswordInput(attrs={'class': 'signup', 'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
