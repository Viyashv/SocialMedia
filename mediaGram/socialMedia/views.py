from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , logout,login     
from .models import *
from django.db.models import Q
import requests
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def Home(request):
    """Get all the user"""
    try:
        response = requests.get('https://dummyjson.com/posts?limit=20')
        response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx

        # Parse the JSON data
        data = response.json()
        posts = data['posts']
        # Print the data (or process it as needed)
        return render(request, 'home.html', {"posts":posts})
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return render(request, 'home.html', )


def registerUser(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        uniquesUN = CustomUser.objects.filter(Q(username__iexact = userName) | Q(email__iexact = email)) #unique username
        # print(f"firstName = {firstName} , lastName = {lastName} , userName = {userName} , email = {email} , password = {password}")
        if uniquesUN.exists():
            messages.warning(request,f"username or email is alredy taken")
        else:
            user = CustomUser.objects.create_user(first_name=firstName,last_name=lastName,username=userName,email=email,password=password)
            user.save()
            messages.success(request,f"User created successfully:- {userName}")
            return redirect('login')
    return render(request , 'register.html')


def loginUser(request):
    """Login user"""
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        print(f"username = {username} , password = {password}")
        user = authenticate(request, username=username, password=password)
        userName = CustomUser.objects.filter(username__exact = username)
        print(userName)
        if len(userName) > 0:
            if user is not None:
                login(request , user)
                messages.success(request , f"Successfully login {username} ")
                return redirect('home')
            messages.warning(request , "Wrong password")
        else:
            messages.warning(request , f"UserName does not exist = {username}")
    return render(request , 'login.html')


def logoutUser(request):
    """Logout the user"""
    messages.warning(request , "You are logout")
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def usereProfiile(request):
    user = request.user
    print(user)
    userPost = Post.objects.filter(user = user)
    print(f"Counts of lIkes in post 1 :- {userPost[0].likes.count()}")
    print(f"Counts of lIkes in post 2 :- {userPost[1].likes.count()}")
    return render(request , "profile.html")