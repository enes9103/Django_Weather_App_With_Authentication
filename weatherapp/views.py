from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import City
from decouple import config

# Create your views here.
def index(request):
    API_KEY = config("API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q=istanbul&appid={API_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()
    weather = {
        "city": data["name"],
        "temp": int(data["main"]["temp"]),
        "desc": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind": data["wind"]["speed"],
        "country": data["sys"]["country"],
        "humi": data["main"]["humidity"],
    }
    return render(request, "weatherapp/index.html",weather)


@login_required
def home(request):
    city = request.GET.get("city")
    API_KEY = config("API_KEY")

    if city:
        url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            my_city = data['name']

            if City.objects.filter(name=my_city,user=request.user):
                messages.info(request,f'{my_city} şehrinin hava durumu bilgilerine sahipsiniz.Lütfe başka bir şehir arayın😉":"You already know the weather for {my_city}, Please search for another city 😉')
            else:
                City.objects.create(name=my_city,user=request.user)
        else:
            messages.warning(request,f"{city} is not a valid city")
        return redirect("home")                 

    city_list = []
    cities = City.objects.filter(user=request.user)
    for i in cities:
        url =f'https://api.openweathermap.org/data/2.5/weather?q={i.name}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        content = response.json()
        data = {
            "city":content["name"],
            "id":i.id,
            "temp":int(content["main"]["temp"]),
            "desc":content["weather"][0]["description"],
            "icon":content["weather"][0]["icon"],
            "wind": content["wind"]["speed"],
            "humi": content["main"]["humidity"],
        }
        city_list.append(data)
    
    context = {
        "city_list":city_list,
    }

    return render(request,'weatherapp/home.html',context)

def delete_city(request,id):
    city = get_object_or_404(City,id=id,user=request.user)
    city.delete()
    messages.success(request, 'City successfully deleted!')
    return redirect("home")