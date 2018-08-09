from django.shortcuts import render
import requests

from .models import City
from .forms import CityForm

# Create your views here.
def base(request):
	cities = City.objects.all()

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=cca47de49f2fcc141649e3bd19afdeb2'

	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()

	form = CityForm()
	weather_data = []

	for city in cities:
		city_weather = requests.get(url.format(city)).json()
		weather = {
			'city': city,
			'temperature': city_weather['main']['temp'],
			'description': city_weather['weather'][0]['description'],
			'icon': city_weather['weather'][0]['icon'],
			'wind': city_weather['wind']['speed'],
			'humidity': city_weather['main']['humidity']
		}

		weather_data.insert(0, weather)
	
		if len(weather_data) > 1:
			x=weather_data[1]
			weather_data.remove(x)

	context = {'weather_data': weather_data, 'form': form}

	return render(request, 'weather/base.html', context)