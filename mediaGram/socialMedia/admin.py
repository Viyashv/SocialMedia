from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Followers)