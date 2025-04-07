from django.db import models
from django.conf import settings
from django.contrib.auth.models import User , AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Add any extra fields here
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """
    Represents a chat conversation between users.
    For a one-on-one chat, this model would include exactly two participants.
    For group chats, it can include more.
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    

   