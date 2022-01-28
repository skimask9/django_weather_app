from django.shortcuts import redirect, render
from .models import City
from .forms import CityForm
import requests
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.



def index(request):
    #appid = yours api key form openweathermap
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    err_msg = ''
    ok_msg = ''
    
    if request.method == 'POST':
        
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            #filter on name of the city and count 
            existing_city_count = City.objects.filter(name=new_city).count()
            #if the city has count 0 == go get request
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                #checking if the name of the city existing cod = 200(cod is from openweathermap api) okay
                if r['cod'] == 200:
                    form.save()
                    ok_msg = 'Successfully added!'
                    #if the cod is not 200 error
                else:
                    err_msg = 'City does not exist in the world!'
            #if the count is more than 0 ( == 1), error
            else:
               err_msg = 'City already exists in the database!'
    #form not in else: cuz i want to have empty form with city name after submitting      
    form = CityForm()
    
    #query the cities and order them by reverse id so last added will be the first one
    cities = City.objects.all().order_by('-id')
    
    #epmty list where we will store all information about city
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        
        city_weather = {
            'city' : city.name,
            'temperature': int(r["main"]['temp']),
            'feels_like': int(r['main']['feels_like']),
            'pressure' : r['main']['pressure'],
            'temp_min' : r['main']['temp_min'],
            'temp_max' : r['main']['temp_max'],
            'visibility': r['visibility'],
            'clouds': str(r['clouds'])[1:-1],
            "wind": int(r['wind']['speed']),    
            "wind1": r['wind']["deg"],    
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'] ,
            #'coord': str(r['coord'])[1:-1]
            'coord_lon' : r['coord']['lon'],
            'coord_lat' : r['coord']['lat'],
        }
        #in our empty list append city_weather dict with api's info
        weather_data.append(city_weather)
    return render (request, 'weather/weather.html', {
        'weather_data': weather_data,
        'form' : form,
        'err_msg' : err_msg,
        "ok_msg" : ok_msg,
    })


#deleting 
def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')


