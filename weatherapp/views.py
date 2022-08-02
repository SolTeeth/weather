from django.shortcuts import render, redirect
from .forms import WeatherForm,SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, forms

import requests


def home(request):
    if request.method == 'GET':
        form = WeatherForm()
        return render(request, 'index.html', {'form': form})

    try:
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
        response = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=037025aea7c9ddf313bf42e7b3136b41').json()[0]
        lat, lon = response['lat'], response['lon']
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&units=metric&appid=037025aea7c9ddf313bf42e7b3136b41').json()
        return render(request, 'index.html', {'response': response, 'form': form})
    except IndexError:
        return render(request, 'index.html', {'form': form, 'error': 'City you entered does not exist'})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': SignupForm()})
    if request.POST['password1'] != request.POST['password2']:
        context = {'form': SignupForm(request.POST)}
        return render(request, 'signup.html', context)
    else:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('home')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': forms.AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user:
        login(request, user)
        redirect('home')


