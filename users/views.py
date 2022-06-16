from django.shortcuts import redirect, render
from django.contrib.auth import login,logout
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm 
# Create your views here.

def register(request):
    form = UserForm()

    if request.method =="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)

            return redirect("home")
    context = {
        "form": form
    }
    return render(request, "users/register.html", context)


def user_login(request):
    form = AuthenticationForm(request,data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request,user)
        return redirect("home")
    
    return render(request, "users/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("index")