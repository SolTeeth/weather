from django.shortcuts import render, redirect
from .models import Cities, UserInfo
from .forms import WeatherForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

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
        new_city = Cities.add(city=city)
        new_city.save()
        return render(request, 'index.html', {'response': response, 'form': form})
    except IndexError:
        return render(request, 'index.html', {'form': form, 'error': 'City you entered does not exist'})


def account(request):
    if request.method == 'GET':
        try:
            userinfo = UserInfo.objects.get(user=request.user)
            user_cities = list(userinfo.cities.values('city'))
            user_cities = [item['city'] for item in user_cities]
            form = WeatherForm()
            return render(request, 'account.html', {'cities': user_cities, 'form': form})
        except ObjectDoesNotExist:
            return render(request, 'account.html')

    try:
        city = request.POST.get('city_field')
        response = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=037025aea7c9ddf313bf42e7b3136b41').json()[0]
        userinfo = UserInfo.objects.get(user=request.user)

        try:
            # Добавляем новый город в список городов пользователя. Одновременно добавляем его и в общий список городов
            # Метод .create добавляет город в поле ManyToMany и одновременно добавляет его в модель на которую ссылается
            # поле ManyToMany
            userinfo.cities.create(city=city)
            userinfo.save()
        except IntegrityError:
            # В случае если в общем списке моделей уже есть такой город, получаем объект города из этой модели
            # и добавляем его в список городов пользователя
            new_city = Cities.objects.get(city=city)
            userinfo.cities.add(new_city)
            userinfo.save()

        user_cities = list(userinfo.cities.values('city'))
        user_cities = [item['city'] for item in user_cities]
        return render(request, 'account.html', {'cities': user_cities})
    except IndexError:
        return render(request, 'account.html', {'error': 'City you entered does not exist'})
    except KeyError:
        return redirect('account')


def delete_city(request, city):
    userinfo = UserInfo.objects.get(user=request.user)
    remove_city = Cities.objects.get(city=city)
    userinfo.cities.remove(remove_city)
    userinfo.save()
    return redirect('account')


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


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': forms.AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', {'form': forms.AuthenticationForm(request.POST)})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


