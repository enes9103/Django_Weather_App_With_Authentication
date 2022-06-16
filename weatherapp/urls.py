from django.urls import path
from .views import home,delete_city, index

urlpatterns = [
    path("",index,name="index"),
    path("weather",home,name="home"),
    path("delete/<int:id>",delete_city,name="delete_city")
]
