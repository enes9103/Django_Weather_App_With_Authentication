
from django.urls import path
from .views import register, user_login, user_logout

urlpatterns = [
    path("login/",user_login,name="user_login"),
    path("register/",register,name="register"),
    path("logout",user_logout,name="user_logout"),
]
