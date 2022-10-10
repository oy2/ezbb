from django.contrib import admin

# Register your models here.
from .models import PrivateMessage, PrivateMessageReplies

admin.site.register(PrivateMessage)
admin.site.register(PrivateMessageReplies)