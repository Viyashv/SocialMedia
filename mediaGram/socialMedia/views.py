from smtplib import SMTPException
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , logout,login     
from .models import *
from django.db.models import Q
import requests
from django.contrib.auth.decorators import login_required
import random #To create random 5-digit code for email verification
from django.core.mail import send_mail # send mail to user for email verification
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
        print(f"email : {email}")
        uniquesUN = CustomUser.objects.filter(Q(username__iexact = userName) | Q(email__iexact = email)) #unique username
        # print(f"firstName = {firstName} , lastName = {lastName} , userName = {userName} , email = {email} , password = {password}")
        if uniquesUN.exists():
            messages.warning(request,f"username or email is alredy taken")
        else:
            # Generate a 5-digit verification code
            verification_code = random.randint(10000, 99999)            
            # Try to send the email
            try:
                send_mail(
                    'Email Verification Code',
                    f'Your verification code is: {verification_code}',
                    'your_email@gmail.com',  # Replace with your email
                    [email],
                    fail_silently=False  # Important: raises an exception if it fails
                )
            except SMTPException as e:
                # If sending the email fails at the SMTP level, show an error
                messages.error(request, 'Invalid or unreachable email address. Please try again.')
                print(f"Error 1 : {e}")
                return redirect("register")
            except Exception as e:
                # Catch-all for any other exceptions
                messages.error(request, 'An error occurred while sending the verification email.')
                print(f"Error 2 : {e}")
                return redirect("register")
            
            # Option 1: Save registration details in session
            request.session['registration_data'] = {
                'firstname': firstName,
                'lastname': lastName,
                'email': email,
                'username': userName,
                'password': password,
                'verification_code': verification_code,
            }
            
            # Option 2: Alternatively, create a temporary model instance to store these details
            
            # Redirect to a separate page where the user can enter the verification code
            return redirect('verify_email')  # Ensure you have a URL named 'verify_email'
    return render(request , 'register.html')


def verify_email(request):
    """
    This view handles the email verification process.
    It checks if the user has entered the correct verification code.
    If correct, it creates a new user instance and logs them in.
    """
    
    registration_data = request.session.get('registration_data')
    context = {}
    context["user_Email"] = registration_data.get("email")
    if request.method == 'POST':
        # Get the code entered by the user
        entered_code = request.POST.get('verification_code')
        # Retrieve the stored registration data

        if registration_data and str(registration_data.get('verification_code')) == entered_code:
            # If codes match, create the user
            user = CustomUser.objects.create_user(
                username=registration_data.get('username'),
                email=registration_data.get('email'),
                password=registration_data.get('password'),
                first_name=registration_data.get('firstname'),
                last_name=registration_data.get('lastname')
            )
            messages.success(request, 'Email verified and user registered successfully.')
            
            # Clear the temporary registration data
            del request.session['registration_data']
            
            return redirect('login')  # Change this to your desired route after registration.
        else:
            messages.error(request, 'Invalid verification code.')
    
    return render(request, 'verify_email.html',context)


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
def myProfiile(request):
    user_id = request.GET.get('User')
    print(f"User id :- {user_id}")
    user = CustomUser.objects.get(id = user_id)
    print(f"user instances :- {user}" )
    context ={}
    context["false_conversations_count"] = user.conversations.filter(status=False).count()
    context["true_conversations_count"] = user.conversations.filter(status=True).count()
    context["data"] = Post.objects.filter(user = user)
    context['user'] = user
    return render(request , "profile.html" , context)



def comment(request):
    if request.method == 'POST':
        post_id = request.GET.get('post_id')
        comment = request.POST.get('comment')
        user_userName = request.GET.get('username')
        print(f"Post ID = {post_id} , comment = {comment} , username = {user_userName}")
        return redirect('profile')