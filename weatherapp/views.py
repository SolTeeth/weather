from django.shortcuts import render
from .forms import WeatherForm
import requests


def home(request):
    if request.method == 'GET':
        form = WeatherForm()
        return render(request, 'index.html', {'form': form})

    try:
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
        response = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=037025aea7c9ddf313bf42e7b3136b41').json()
        lat, lon = response[0]['lat'], response[0]['lon']
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&units=metric&appid=037025aea7c9ddf313bf42e7b3136b41').json()
        return render(request, 'index.html', {'response': response, 'form': form, 'city': city})
    except IndexError:
        return render(request, 'index.html', {'form': form, 'error': 'City you entered does not exist'})
