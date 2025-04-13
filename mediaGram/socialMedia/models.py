from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True , null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts',blank=True)
    image = models.ImageField(upload_to="upload/post" ,null=True ,blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Comment by {self.user} on {self.post}" 

class CustomUser(AbstractUser):
    """
    Custom User Model which extends the bultin User Model of Django.
    """
    # Add any extra fields here
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10 , null=True , blank=True)
    image = models.ImageField(upload_to="upload/User" , blank=True , null=True)

    def __str__(self):
        return f"User Id :- {self.id} - Username :- {self.username}"

class Conversation(models.Model):
    """
    Represents a chat conversation between users.
    For a one-on-one chat, this model would include exactly two participants.
    For group chats, it can include more.
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"Conversation {self.pk} with {', '.join(user.username for user in self.participants.all())}"

class Message(models.Model):
    """
    Represents a message sent in a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    
