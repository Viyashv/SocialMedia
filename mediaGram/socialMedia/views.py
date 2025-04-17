from smtplib import SMTPException
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate , logout,login     
from .models import *
from django.db.models import Q
import requests
from django.contrib.auth.decorators import login_required
import random #To create random 5-digit code for email verification
from django.core.mail import send_mail # send mail to user for email verification
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timesince import timesince
from django.utils.timezone import localtime
# Create your views here.

@login_required(login_url="login")
def Home(request):
    """Get all the user"""
    try:
        context ={}
        response = requests.get('https://dummyjson.com/posts?limit=20')
        response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx

        # Parse the JSON data
        user = request.user
        # Get all follower records where the current user is the follower
        following_ids = Followers.objects.filter(user=user).values_list('follower__id', flat=True)
        allpost = Post.objects.filter(Q(user__in=following_ids) | Q(user=request.user)).order_by("-timestamp")
        data = response.json()
        context['posts'] = data['posts']
        context['allPosts'] = allpost
        # Print the data (or process it as needed)
        return render(request, 'home.html', context)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return render(request, 'home.html')


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
        # print(f"username = {username} , password = {password}")
        user = authenticate(request, username=username, password=password)
        userName = CustomUser.objects.filter(username__exact = username)
        # print(userName)
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
    # print(f"User id :- {user_id}")
    user = CustomUser.objects.get(id = user_id)
    # print(f"user instances :- {user}" )
    print(f"Login user :- {request.user.username} - Following :- {user.username}")
    is_following = Followers.objects.filter(user=request.user.id , follower = user.id).exists()
    print(is_following)
    context ={}
    context["followers"] = user.following.all()
    context["following"] = Followers.objects.filter(user = user)
    context["data"] = Post.objects.filter(user = user)
    context['user'] = user
    context['is_following'] = is_following
    return render(request , "profile.html",context)

    
@require_POST
@login_required
def likePost(request):
    """
    This is Used by Ajax to fetch and update the like count of a post.
    Function used to Like a post by the user and also to unlike the post if the user has already liked it.
    return the like count of the post.
    """
    post_id = request.POST.get("Post")
    user  = request.user
    # print(f'User id :- {user} , post id :- {post_id}')
    post_instance = get_object_or_404(Post, id=post_id) 
    # print(f"Post Id = {post_id} , Post Instance = {post_instance}")
    # Toggle the like status
    if user in post_instance.likes.all():
        post_instance.likes.remove(user)
        liked = False
    else:
        post_instance.likes.add(user)
        liked = True

    like_count = post_instance.likes.count()
    # Return JSON with updated like info
    return JsonResponse({'liked': liked, 'like_count': like_count})
    

@csrf_exempt
def add_comment(request):
    """
    This is used by ajax to add a comment to a post,
    and also to update the comment count of the post.
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        post_id = data.get('Post')
        user_id = data.get('User')
        comment_text = data.get('comment')
        # print(f"post id :- {post_id} , user id :- {user_id} , comment :- {comment_text}")

        # Perform validation and save the comment
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(CustomUser, id=user_id)
        comment=Comment.objects.create(post=post, user=user, content=comment_text)

        # Get the updated comment count
        comment_count = post.comments.count()
        context = {
            'success': True,
            'comment_text': comment_text,
            'username': comment.user.username,
            'user_id': comment.user.id,
            'user_image_url': comment.user.image.url if comment.user.image else "",
            'timestamp': localtime(comment.timestamp).strftime("%b %d"),
            'comment_count': comment_count  
        }

        return JsonResponse(context)
    return JsonResponse({'success': False}, status=400)

