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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',Home,name='home'),
    path('login/',loginUser,name='login'),
    path('register/',registerUser,name='register'),
    path('logout/',logoutUser,name="logout"),
    path('profile/',myProfiile , name="profile"),
    path('verify_email/',verify_email, name="verify_email"),
    path('addcomment/',add_comment, name="addcomment"),
    path('like/',likePost, name="like"),
    # below is the urls for forget password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
