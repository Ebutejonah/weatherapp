import datetime
import requests
from django.shortcuts import render

def indexview(request):
    API_KEY = ("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.get('city2', None)
    return render(request, 'index.html')

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    current_response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = current_response['coord']['lat'], current_response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()

    weather_data = {
        'city':city,
        'temperature':round(current_response(['main']['temp'] - 273.15, 2)),
        'description': current_response['weather'][0]['description'],
        'icon': current_response['weather'][0]['icon']
    }   

    daily_forecasts = []
    for daily_data in forecast_response:
        pass