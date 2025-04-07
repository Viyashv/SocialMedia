from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , logout,login     
from .models import *
# Create your views here.

def Home(request):
    return render(request, 'home.html')


def registerUser(request):
    return render(request , 'register.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        print(f"username = {username} , password = {password}")
        user = authenticate(request, username=username, password=password)
        userName = CustomUser.objects.get(username = username)
        print(userName)
        if user is not None:
            login(request , user)
            return redirect('home')
        messages.warning(request , "Wrong username or password")
    return render(request , 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')