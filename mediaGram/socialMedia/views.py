from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request, 'home.html')


def registerUser(request):
    return render(request , 'register.html')


def loginUser(request):
    return render(request , 'login.html')