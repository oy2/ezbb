from django.contrib import admin

# Register your models here.

from .models import Topic, Post, Comment

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)



