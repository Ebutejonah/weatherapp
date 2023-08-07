import datetime
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config

def indexview(request):
    API_KEY = config('API_KEY')
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    if request.method == "POST":
        try:
            city1 = request.POST['city1']
            city2 = request.POST.get('city2', None)

            weather_data1, daily_forecast1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

            if city2:
                weather_data2, daily_forecast2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
            else:
                weather_data2, daily_forecast2 = None, None
            context = {
                'weather_data1':weather_data1,
                'weather_data2':weather_data2,
                "daily_forecast2": daily_forecast2,
                "daily_forecast1": daily_forecast1,
            }
            return render(request, 'index.html', context)
        except KeyError:
            messages.info(request, 'Invalid Input')
            return redirect('/')
    return render(request, 'index.html')

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    try:
        response = requests.get(current_weather_url.format(city, api_key)).json()
        lat, lon = response['coord']['lat'], response['coord']['lon']
        forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()
    except requests.exceptions.RequestException as e:
        print('Error:', e)
    weather_data = {
        'city':city,
        'temperature':round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }   

    daily_forecasts = []
    try:
        for daily_data in forecast_response['daily'][:5]:
            
            daily_forecasts.append({
                'day':datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon']
            })
    except KeyError:
        print('Key Error')
    return weather_data, daily_forecasts