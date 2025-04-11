"""
URL configuration for mediaGram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import * 

urlpatterns = [
    path('',Home,name='home'),
    path('login/',loginUser,name='login'),
    path('register/',registerUser,name='register'),
    path('logout/',logoutUser,name="logout"),
    path('profile/',usereProfiile , name="profile"),
    path('verify_email/',verify_email, name="verify_email"),
]
