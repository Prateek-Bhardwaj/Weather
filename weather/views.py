import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForms

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e2ffad00401f329431db01a92c63085c'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForms(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name'].lower()
            count = City.objects.filter(name=new_city).count()
            if count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City Does not exist'
            else:
                err_msg = 'City already exist'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'
    forms = CityForms()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {'weather_data' : weather_data, 'forms':forms, 'message':message, 'message_class':message_class }
    return render(request,'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')